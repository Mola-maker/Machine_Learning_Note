# molamaker-site — Learning Note

A personal study guide for *this* codebase and the systems it runs on. It ties
each fundamental (Node, npm, SQL, nginx, ECS, networking) to the actual files
where you use it, so the theory always has a concrete anchor.

> How to use this: read top-to-bottom once for the mental model, then keep it
> open as a reference. Every "→ see" points at a real file in this repo.

---

## 0. The one-paragraph mental model

A visitor's browser loads a **Next.js** app. Most pages are hosted on
**Vercel** (serverless). The app talks to two backends: **Supabase** (managed
Postgres, for blog/guestbook/workplace data) and an **Aliyun ECS** box (a
long-running Linux server that runs the **AstrBot** chatbot in Docker, behind
**nginx**). The browser never talks to ECS or Supabase service-role directly —
it always goes through a Next.js **API route** that adds auth, validation, and
rate-limiting. Everything is just **HTTP requests carrying JSON**, secured with
**TLS** and authenticated with **cookies, bearer keys, or HMAC signatures**.

```
                    ┌────────────────────── Vercel (serverless) ──────────────────────┐
  Browser  ──HTTPS─▶│  Next.js: pages (app/[locale]) + API routes (app/api/**)         │
  (React)           │   - validates, rate-limits, signs, proxies                       │
                    └───────┬───────────────────────────────────┬──────────────────────┘
                            │                                   │
                   HTTPS (anon/service key)            HTTPS (bearer key)
                            ▼                                   ▼
                    Supabase (Postgres+RLS)        Aliyun ECS  ── nginx ──▶ Docker
                    tables, RPC, auth              (persistent)            (AstrBot :6185
                                                                            + NapCat)
```

---

## 1. The request lifecycle (read this first)

Trace one real request end-to-end — it's the fastest way to understand the whole
app. Example: the **chat widget sending a message**.

1. **Browser** — `components/redesign/astrbot-chat.tsx` `send()` does
   `fetch('/api/astrbot/chat', { method:'POST', body: JSON })`.
2. **Next.js API route** — `app/api/astrbot/chat/route.ts` runs on the server:
   - `validateOrigin()` — rejects cross-site callers (CSRF defense).
   - `clientIp()` — reads the real IP from nginx headers (`lib/client-ip.ts`).
   - `checkRate()` — Postgres-backed limiter (`lib/rate-limit.ts`).
   - validates input with a zod schema (`lib/validation.ts`).
   - **waterfall**: tries AstrBot (ECS) → Coze → DeepSeek until one replies.
3. **Upstream** — `fetch('${ASTRBOT_URL}/api/v1/chat')` hits the ECS box over
   the internal network; nginx proxies to the Docker container on `:6185`.
4. **Response** — the route returns `{ data: { message, provider } }`; the
   browser appends it to the message list and re-renders.

Every feature in this repo is a variation on this loop. Internalize it and the
rest is detail.

---

## 2. Codebase map (where things live)

| Area | Entry points | Notes |
|---|---|---|
| **Routing & i18n** | `app/[locale]/`, `lib/supabase/middleware.ts`, `i18n/routing` | next-intl v4; pages are localized, API routes are not |
| **UI shell (the 6 variants)** | `components/redesign/root.tsx` | one big client component; variants: terminal/magazine/atlas/stream/workplace/notebook |
| **Design tokens** | `app/redesign-styles/*.css` | CSS custom properties: `--ink`, `--bg-elev`, `--accent`, `--rule` |
| **Blog** | `content/*.md`, `lib/posts` (gray-matter) | filesystem markdown, rendered at request time |
| **Site auth (admin)** | `lib/auth.ts`, `app/[locale]/login`, `app/auth/callback` | Supabase email magic-link |
| **Workplace auth (custom)** | `lib/workplace/session.ts`, `app/api/workplace/auth/*` | HMAC-signed cookie; phone OTP / WeChat / admin key |
| **Workplace backend** | `app/api/workplace/*`, `lib/workplace/*` | SSE bus, child_process, reverse proxy, kanban, math |
| **Chatbot** | `components/redesign/astrbot-chat.tsx`, `app/api/astrbot/chat/route.ts` | AstrBot→Coze→DeepSeek waterfall |
| **Data layer** | `lib/supabase/{client,server,service}.ts`, `supabase/migrations/*.sql` | three client types, SQL migrations |
| **Security utils** | `lib/rate-limit.ts`, `lib/client-ip.ts`, `lib/origin.ts`, `lib/validation.ts` | reuse these, don't reinvent |
| **Ops / deploy** | `deploy/astrbot/*`, `next.config.mjs` | ECS Docker + nginx setup |

---

## 3. Node.js (the runtime your server code runs on)

Your API routes and `lib/*` server code execute in Node. Core ideas, each with
a place you already use it:

- **Single thread + async I/O / event loop.** Node doesn't block on network or
  disk; it registers callbacks and moves on. That's why every upstream call is
  `await fetch(...)`. A slow Supabase call (you saw 24s once) doesn't freeze the
  process — it just keeps that one request pending.
- **`runtime = 'nodejs'` vs Edge.** Routes that use Node APIs (crypto,
  child_process, Buffer) **must** declare `export const runtime = 'nodejs'`.
  → see the top of `app/api/workplace/auth/phone/route.ts` and `claude/route.ts`.
- **Streams.** Server-Sent Events are built on `ReadableStream`.
  → `app/api/workplace/messages/route.ts` builds a stream and `enqueue()`s
  `data: ...\n\n` chunks.
- **child_process.** `spawn`/`execFile` launch external programs. This only
  works on a **persistent** host (ECS), never on Vercel.
  → `app/api/workplace/claude/route.ts` (`spawn('claude')`),
  `deploy/route.ts` (`execFile('git'…)`).
- **crypto.** `createHmac('sha256'|'sha1', key)` for signing.
  → `lib/workplace/session.ts` (cookie signing), `lib/workplace/sms.ts`
  (Aliyun request signing).
- **Environment variables.** `process.env.X`. Secrets live in `.env.local`
  (dev) or the host's env (Vercel/ECS), never in the repo.
- **`AbortSignal.timeout(ms)`.** Caps how long an upstream call can hang.
  → used in every provider call in `astrbot/chat/route.ts`.

**Learn next:** the event loop (macrotasks vs microtasks), `Promise.all` vs
sequential `await`, and why CPU-heavy work blocks Node (offload or stream it).

---

## 4. npm (how dependencies and scripts work)

- **`package.json`** — declares dependencies and the `scripts` you run:
  `npm run dev` (`next dev`), `npm run build`, `npm start`.
- **`package-lock.json`** — pins exact versions so every machine/CI installs the
  same tree. Commit it. Don't hand-edit it.
- **semver** — `^15.5.0` means "≥15.5.0, <16". Major = breaking, minor =
  features, patch = fixes.
- **`dependencies` vs `devDependencies`** — runtime needs vs build/test-only.
- **`npx`** — run a package binary without a global install (`npx tsc`,
  `npx eslint`).
- **`npm audit`** — lists known CVEs in your tree. Your `CLAUDE.md` requires
  running it before declaring a review done.
- **`node_modules`** — installed packages; never committed (in `.gitignore`).

**Learn next:** lockfile hygiene, `npm ci` (clean installs in CI), and the
difference between `npm install` and `npm update`.

---

## 5. SQL & Supabase (your data layer)

Supabase is hosted Postgres plus auth and an auto-generated REST/RPC layer.

- **Three client types — know which bypasses security:**
  - browser/anon (`lib/supabase/client.ts`) — subject to RLS.
  - server-with-cookies (`lib/supabase/server.ts`) — acts as the logged-in user.
  - **service-role** (`lib/supabase/service.ts`) — **bypasses RLS**, server-only,
    never sent to the browser.
- **RLS (Row Level Security)** — the most important security concept here.
  Postgres policies decide which rows each role can read/write. With RLS on,
  even a leaked anon key can't read other users' rows.
  → study `supabase/migrations/*_security_advisories.sql` and
  `*_indexes_rls.sql`.
- **Migrations** — ordered `.sql` files in `supabase/migrations/`. Each is a
  forward change (create table, add policy, add function). They run in filename
  order. → `20260528000000_workplace.sql` creates the workplace tables.
- **RPC (stored functions)** — server-side SQL functions called by name.
  → `check_rate` (the rate limiter) lives in a migration and is invoked via
  `supabase.rpc('check_rate', …)` in `lib/rate-limit.ts`.
- **The query builder is just SQL.** `.from('t').select('a').eq('x', y)` →
  `SELECT a FROM t WHERE x = y`. `.upsert(row, { onConflict: 'id' })` →
  `INSERT … ON CONFLICT (id) DO UPDATE`.
- **SQL basics to own:** `SELECT/INSERT/UPDATE/DELETE`, `WHERE`, `JOIN`,
  primary keys, indexes (why `*_indexes.sql` exists — speed), `NULL` handling,
  transactions, and `ON CONFLICT` (upsert).

**Learn next:** read one migration line-by-line, then write a tiny policy
yourself with the `/new-migration` helper. Understand why an index makes a query
fast (B-tree lookups vs full table scans).

---

## 6. nginx (the reverse proxy on ECS)

nginx sits in front of AstrBot on the ECS box. → `deploy/astrbot/SETUP.md` §5.

- **Reverse proxy** — nginx receives public HTTPS on 80/443 and forwards to a
  local app: `proxy_pass http://127.0.0.1:6185`. The app itself only listens on
  localhost, so it's not exposed to the internet directly.
- **`proxy_set_header`** — nginx must pass the real client info downstream:
  ```
  proxy_set_header X-Real-IP $remote_addr;
  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  ```
  This is exactly what `lib/client-ip.ts` reads. If nginx doesn't set it, your
  rate limiter sees nginx's IP for everyone.
- **TLS termination** — `certbot --nginx` provisions a free Let's Encrypt
  certificate and nginx decrypts HTTPS, so the app speaks plain HTTP locally.
- **Basic auth** — `auth_basic` + `htpasswd` gates the AstrBot admin panel.
- **`server` / `location` blocks** — virtual hosts by domain and path routing.
- **Workflow:** edit config → `sudo nginx -t` (syntax check) →
  `sudo systemctl reload nginx` (zero-downtime reload).

**Learn next:** the difference between `proxy_pass` with/without a trailing
slash, gzip, and how HTTP/2 + keep-alive reduce latency.

---

## 7. ECS & system arrangement (the Linux server)

ECS = Aliyun's "Elastic Compute Service" — a plain Ubuntu VM you fully control
(unlike Vercel). → `deploy/astrbot/SETUP.md` is the whole playbook.

- **Topology / where each process runs:**
  - Vercel: the Next.js site (serverless functions, no persistent state).
  - ECS: AstrBot + NapCat in **Docker Compose**, fronted by nginx.
  - Supabase: managed Postgres (you don't run it).
- **Docker / Docker Compose** — containers package an app + its deps. `docker
  compose up -d` starts the AstrBot + NapCat services defined in
  `deploy/astrbot/docker-compose.yml`. `docker compose logs <svc>` to debug.
- **Process supervision** — long-running services need a supervisor so they
  restart on crash/reboot: Docker's `restart: unless-stopped` for containers,
  **systemd** for nginx (`systemctl`), and **PM2** if you self-host the Next app
  (referenced in `lib/client-ip.ts`).
- **Users & permissions** — services run as a non-root user (`molabot`),
  secrets are `chmod 600 .env` (owner-only). Principle of least privilege.
- **Ports & binding** — `127.0.0.1:6185` (localhost only) vs `0.0.0.0:6185`
  (all interfaces, internet-exposed). The setup binds to localhost and lets only
  nginx reach it. Verify with `ss -tlnp`.
- **Firewall** — Aliyun security group + only 22/80/443 open. Everything else
  is closed at the cloud edge.

**Learn next:** systemd unit files, `journalctl` for logs, Docker networking
(why containers reach each other by service name), and SSH key auth.

---

## 8. Communication engineering (the networking layer)

Everything above is glued together by network protocols. The ones you actually
use:

- **DNS + ICP** — a domain resolves to the ECS IP; China requires an ICP filing
  for a public site (noted in the setup).
- **TCP & ports** — reliable byte streams; a "port" is just a number a process
  listens on (6185, 443). HTTP rides on TCP.
- **HTTP/1.1** — request line + headers + body; methods (`GET` safe/idempotent,
  `POST` creates/acts), status codes (2xx ok, 3xx redirect, 4xx caller error,
  5xx server error). You return these deliberately:
  `401` unauth, `403` forbidden, `429` rate-limited, `502` upstream failed,
  `503` not configured. → grep any route to see the pattern.
- **TLS/HTTPS** — encryption + server identity via certificates (certbot).
  Protects cookies and API keys in transit.
- **Headers that matter here:** `Authorization: Bearer <key>` (AstrBot, Coze,
  DeepSeek), `Content-Type: application/json`, `Set-Cookie` (sessions),
  `Retry-After` (429s), `X-Real-IP`/`X-Forwarded-For` (proxy chain).
- **Three ways to push data to the browser** — know when to use each:
  - **polling** — client re-requests on a timer (workflow status every 15s).
  - **SSE (Server-Sent Events)** — one long-lived response streaming `data:`
    lines, server→client only. → message bus, Claude terminal. Needs a
    persistent host.
  - **WebSocket** — full duplex (not used here, but the next step up).
- **OAuth 2.0 authorization-code flow** — the WeChat login: redirect user to
  provider → provider redirects back with a `code` → server exchanges `code`
  (+secret) for a token → fetch user info. → `auth/wechat/route.ts`.
- **HMAC** — prove a message wasn't tampered with, using a shared secret.
  Cookie integrity (`session.ts`) and Aliyun request signing (`sms.ts`).
- **Same-origin / CSRF** — `lib/origin.ts` rejects requests from other sites so
  a malicious page can't drive your API with the visitor's cookies.
- **Idempotency, timeouts, retries/backoff, rate limiting** — reliability
  patterns. You already do timeouts (`AbortSignal.timeout`), rate limiting
  (`check_rate`), and a retry-of-sorts via the provider waterfall.

**Learn next:** the TLS handshake steps, HTTP/2 multiplexing, and CORS vs
same-origin (when each applies).

---

## 9. Security ideas woven through the code

- **Defense in depth** — the deploy route validates the URL with a regex *and*
  uses `execFile` (no shell) *and* an allowlist. Layers, not one check.
- **Fail closed** — when a secret is missing, features disable themselves
  (admin key 503, rate limiter denies on DB error) rather than fall open.
- **Constant-time comparison** — `timingSafeEqual` for the admin key, so an
  attacker can't learn the key from response timing. → `auth/key/route.ts`.
- **Never trust upstream/page content** — treat scraped or user text as data,
  never as instructions; escape before reflecting into HTML (the proxy 502 page
  escapes the workflow id).

---

## 10. A study order that works

1. **Trace one request** (§1) in the debugger or with `console.log`.
2. **Node + HTTP** (§3, §8) — the runtime and the protocol.
3. **Supabase + SQL + RLS** (§5) — read one migration, write one policy.
4. **Auth** — follow a login cookie from `session.ts` to a protected route.
5. **nginx + ECS + Docker** (§6, §7) — stand up the AstrBot box from the setup.
6. **SSE + child_process** (§3) — the advanced workplace backend.

**Fastest way to make it click:** pick a feature, set a breakpoint at the API
route, and watch the data flow through each layer. Theory sticks when it's
attached to a request you can see.

---

*Anchored to the repo as of this writing. Cross-check `file:line` against
current code before relying on a citation — code drifts, this note doesn't.*
