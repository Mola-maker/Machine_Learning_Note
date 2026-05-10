Q: 前端框架 A: React + Vite

Q: 后端 / 数据库 A: Node.js + PostgreSQL

Q: 部署平台 A: Vercel
关于claude的claude.md
# CLAUDE.md

> 本文件是项目的 AI 工作记忆。每次会话 Claude 必须先完整读取本文件再开始工作。 规则优先级：本文件 > 对话指令 > Claude 默认行为。

---

## 一、技术栈

### 前端

- **框架**：React 18 + Vite 5
- **语言**：TypeScript（严格模式，`strict: true`）
- **样式**：Tailwind CSS v3
- **路由**：React Router v6
- **状态管理**：Zustand（全局）/ React Query（服务端状态）
- **表单**：React Hook Form + Zod
- **HTTP 客户端**：axios（统一封装在 `src/lib/api.ts`）
- **测试**：Vitest + React Testing Library

### 后端

- **运行时**：Node.js 20 LTS
- **框架**：Express 5
- **语言**：TypeScript（严格模式）
- **ORM**：Prisma（schema 在 `prisma/schema.prisma`）
- **数据库**：PostgreSQL 16
- **认证**：JWT（access token 15min / refresh token 7d）
- **校验**：Zod（前后端共享 schema，放在 `packages/shared/`）
- **测试**：Vitest + Supertest

### 基础设施

- **部署**：Vercel（前端 + API Routes）
- **数据库托管**：Supabase / Railway PostgreSQL
- **环境变量**：`.env.local`（本地）/ Vercel Environment Variables（生产）
- **CI/CD**：GitHub Actions → Vercel 自动部署
- **包管理**：pnpm workspace（monorepo）

### 目录结构

```
/
├── apps/
│   ├── web/          # React + Vite 前端
│   └── api/          # Express 后端
├── packages/
│   └── shared/       # 共享类型、Zod schema、工具函数
├── prisma/
│   └── schema.prisma
├── .github/
│   └── workflows/
└── CLAUDE.md
```

---

## 二、编码规范

### 通用原则

- 所有文件使用 TypeScript，禁止 `any`，使用 `unknown` + 类型收窄
- 函数优先使用具名函数（`function foo()`），箭头函数用于回调和 React 组件
- 文件长度上限 300 行；超过则拆分模块
- 每个函数只做一件事，超过 40 行考虑拆分
- 注释只写"为什么"，不写"是什么"

### 命名约定

|类型|规则|示例|
|---|---|---|
|组件文件|PascalCase|`UserProfile.tsx`|
|工具函数|camelCase|`formatDate.ts`|
|类型/接口|PascalCase + 语义后缀|`UserDto`, `ApiResponse<T>`|
|常量|SCREAMING_SNAKE|`MAX_RETRY_COUNT`|
|环境变量|SCREAMING_SNAKE|`DATABASE_URL`|
|数据库表|snake_case 复数|`user_sessions`|
|API 路由|kebab-case 复数|`/api/user-sessions`|

### React / 前端规范

- 组件一律使用函数式组件 + hooks，禁止 class component
- props 用 `interface` 定义，命名为 `ComponentNameProps`
- 自定义 hook 放在 `src/hooks/`，文件名以 `use` 开头
- 全局状态只放"真正全局"的数据（用户信息、主题），UI 状态用 `useState`
- API 调用统一通过 React Query，禁止在组件内直接 `fetch`/`axios`
- 所有异步操作必须处理 loading / error 状态
- 图片使用 `loading="lazy"`，大列表使用虚拟滚动

```typescript
// ✅ 正确示例
interface UserCardProps {
  userId: string;
  onSelect: (id: string) => void;
}

function UserCard({ userId, onSelect }: UserCardProps) {
  const { data: user, isLoading } = useUser(userId);
  if (isLoading) return <Skeleton />;
  return <div onClick={() => onSelect(userId)}>{user?.name}</div>;
}

// ❌ 错误示例
const UserCard = (props: any) => { /* ... */ };
```

### Node.js / 后端规范

- 所有路由处理器用 `async/await`，必须 `try/catch` 或使用 `asyncHandler` 包装
- 错误统一通过 `next(error)` 传递给全局错误中间件
- 业务逻辑放在 `services/`，路由层只做参数校验和调用 service
- 数据库操作只在 `services/` 或 `repositories/` 内，禁止在路由层直接查库
- 所有入参用 Zod schema 校验，校验失败返回 `400`
- 敏感字段（密码、token）禁止出现在日志和 API 响应中

```typescript
// ✅ 正确的路由层
router.post('/users', asyncHandler(async (req, res) => {
  const body = CreateUserSchema.parse(req.body);  // Zod 校验
  const user = await userService.create(body);    // service 层
  res.status(201).json({ data: user });
}));
```

### 数据库 / Prisma 规范

- 所有 schema 变更通过 `prisma migrate dev` 生成迁移文件，禁止直接改数据库
- 迁移文件命名：`YYYYMMDD_描述`（例：`20240315_add_user_avatar`）
- 每张表必须有 `id`（uuid）、`createdAt`、`updatedAt`
- 软删除使用 `deletedAt: DateTime?`，不物理删除用户数据
- N+1 问题：Prisma 查询必须用 `include` 或 `select` 显式声明关联，禁止循环查询

### API 设计规范

- RESTful 风格，资源用复数名词
- 统一响应结构：
    
    ```typescript
    // 成功{ "data": T, "meta"?: PaginationMeta }// 错误{ "error": { "code": string, "message": string, "details"?: unknown } }
    ```
    
- 分页参数：`?page=1&limit=20`（limit 上限 100）
- 认证：`Authorization: Bearer <token>` header
- 版本：路由前缀 `/api/v1/`

### Git 规范

- commit 格式：`type(scope): subject`
    - type: `feat` / `fix` / `chore` / `refactor` / `test` / `docs`
    - 示例：`feat(auth): add refresh token rotation`
- 每个 PR 只做一件事，禁止混入不相关修改
- PR 合并前必须通过 CI（lint + type-check + test）
- 分支命名：`feat/功能名`、`fix/问题描述`、`chore/任务名`

### 测试规范

- 新功能必须附带单元测试，覆盖率不低于 70%
- 工具函数、service 层必须有测试
- 测试文件和源文件同目录，命名 `*.test.ts`
- 测试描述用中文（方便排查），断言使用 `expect`

---

## 三、禁止事项

### 安全红线（任何情况下不得违反）

- **禁止**将 `SECRET_KEY`、`DATABASE_URL`、API 密钥等硬编码在代码中
- **禁止**在日志中输出密码、token、个人敏感信息
- **禁止**在前端代码中放置后端密钥（即使是 `VITE_` 前缀的也要谨慎）
- **禁止**SQL 拼接字符串，必须使用 Prisma 或参数化查询
- **禁止**跳过 Zod 校验直接使用 `req.body`
- **禁止**在未授权情况下返回其他用户的数据（必须校验 userId 归属）

### 代码质量红线

- **禁止**提交包含 `console.log` 的代码（调试用 `logger.debug`）
- **禁止**提交 TypeScript 类型错误（`tsc --noEmit` 必须通过）
- **禁止**提交 ESLint 错误（警告可暂时保留但需注释说明原因）
- **禁止**注释掉大段代码后提交（删除或用 git stash 保存）
- **禁止**在 `main`/`master` 分支直接 push，必须走 PR

### 架构边界（不得随意打破）

- **禁止**前端直接连接数据库（Prisma client 只在后端使用）
- **禁止**在组件内部写业务逻辑超过 10 行，抽取到 hook 或 service
- **禁止**在 `packages/shared/` 中引入前端或后端专属依赖
- **禁止**绕过 React Query 缓存层直接调用 API（保持缓存一致性）
- **禁止**修改已有 Prisma 迁移文件（只能新增迁移）

### Claude 操作限制

- **禁止**在未确认当前 git 状态干净前修改多个文件
- **禁止**在我未明确要求时执行数据库迁移（`prisma migrate`）
- **禁止**在我未明确要求时执行 `git push` 或触发部署
- **禁止**删除或重命名现有 API 路由（可能破坏线上客户端）
- **禁止**在我未审阅 Plan 前切换到 auto-accept 模式执行多文件修改
- 遇到不确定的架构决策，**必须先问我**，不要自行假设

---

## 四、常用命令速查

```bash
# 开发
pnpm dev              # 同时启动前后端
pnpm dev:web          # 仅前端 (localhost:5173)
pnpm dev:api          # 仅后端 (localhost:3000)

# 类型检查 & Lint
pnpm typecheck        # tsc --noEmit (全项目)
pnpm lint             # ESLint
pnpm lint:fix         # 自动修复

# 测试
pnpm test             # 全部测试
pnpm test:watch       # 监听模式
pnpm test:coverage    # 覆盖率报告

# 数据库
pnpm db:migrate       # prisma migrate dev
pnpm db:studio        # Prisma Studio (localhost:5555)
pnpm db:seed          # 填充测试数据
pnpm db:reset         # 重置数据库（仅开发环境）

# 构建 & 部署
pnpm build            # 生产构建
pnpm preview          # 本地预览生产构建
```

---

## 五、已知问题 & Gotchas

> 此区域记录 Claude 曾经犯过的错误和项目特有的坑，每次 PR 后更新。

- [ ] _（第一条经验待记录）_

---

## 六、环境变量清单

```bash
# apps/api/.env.local
DATABASE_URL=postgresql://user:password@localhost:5432/myapp
JWT_SECRET=your-secret-here
JWT_REFRESH_SECRET=your-refresh-secret-here
NODE_ENV=development
PORT=3000

# apps/web/.env.local
VITE_API_BASE_URL=http://localhost:3000/api/v1
```

> 生产环境变量在 Vercel Dashboard → Settings → Environment Variables 中配置，不在代码库中存储。