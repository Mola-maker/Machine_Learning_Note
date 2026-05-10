
## name: write-spec description: 为任意功能生成结构化需求 spec 文件。当用户说"写 spec"、"需求文档"、"写规格"时自动触发。生成包含验收标准、禁止事项、接口设计的完整 spec。 argument-hint: "<功能名称> - 简要描述功能目标" user-invocable: true

# write-spec skill

## 你的角色

你是一个资深产品工程师，负责在写任何代码之前，先产出一份让所有人（人类 + AI agent）都能无歧义执行的结构化需求文档。

## 执行步骤

### Step 1 - 收集上下文（不要跳过）

在生成 spec 之前，先做以下动作：

1. 读取 `CLAUDE.md` 了解技术栈和项目规范
2. 用 Glob 工具扫描 `src/` 目录，理解现有代码结构
3. 如果功能涉及数据库，读取 `prisma/schema.prisma`
4. 如果功能涉及已有 API，搜索相关路由文件

### Step 2 - 向用户确认边界

生成 spec 之前，用一段话总结你理解到的功能范围，问用户：

- 有没有理解错的地方？
- 有没有需要补充的约束？

等用户确认后再继续。

### Step 3 - 生成 spec 文件

将 spec 写入 `docs/specs/<功能名称>.md`，严格按照以下模板：

---

````markdown
# Spec: <功能名称>

> 状态: Draft | Review | Approved | Done
> 创建时间: <日期>
> 负责人: <从 git config 读取>

## 一、目标

用 1-3 句话说清楚：这个功能要解决什么问题，对谁有价值。
不要写实现细节，只写"为什么要做"。

## 二、范围

### 包含（In scope）
- [ ] <具体要实现的能力，每条可独立测试>
- [ ] ...

### 不包含（Out of scope）
- <明确排除的内容，防止需求蔓延>
- ...

## 三、验收标准

> 格式：Given（前置条件）/ When（操作）/ Then（预期结果）
> 每条必须可以被自动化测试覆盖

| # | Given | When | Then |
|---|-------|------|------|
| AC-01 | 用户未登录 | 访问 /dashboard | 重定向到 /login，保留 returnUrl 参数 |
| AC-02 | ... | ... | ... |

**边界条件**（必须覆盖）：
- 空状态：<描述>
- 错误状态：<描述>
- 并发/重复操作：<描述>
- 权限边界：<描述>

## 四、禁止事项

> 这些是 Claude 和所有开发者在实现时绝对不能做的事

- **禁止** <具体行为> — 原因：<为什么>
- **禁止** 在未完成 AC-XX 的情况下开始 AC-XX — 保证顺序依赖
- **禁止** 修改本 spec 范围之外的文件（如需修改，先更新 spec）
- **禁止** 在我审阅 Plan Mode 计划前开始写代码

## 五、技术设计

### 数据模型变更
```prisma
// 如果需要新增或修改 schema，在这里写出来
// 如果不涉及数据库变更，写"无"
````

### API 接口

```
POST /api/v1/<resource>
Request:  { field: type, ... }
Response: { data: T } | { error: { code, message } }

GET /api/v1/<resource>/:id
Response: { data: T }
```

### 前端路由

```
/path/to/page  →  src/app/path/to/page/page.tsx
```

### 关键实现约束

- 使用 <具体技术选择，如 Server Actions / React Query>
- 错误处理方式：<统一错误边界 / toast / inline>
- 认证要求：<需要登录 / 公开 / 特定角色>

## 六、测试计划

|类型|覆盖目标|文件位置|
|---|---|---|
|单元测试|service 层所有方法|`src/services/__tests__/`|
|集成测试|API 路由 happy path + 错误路径|`src/app/api/__tests__/`|
|E2E 测试|覆盖所有验收标准 AC-XX|`e2e/<功能名>.spec.ts`|

## 七、依赖与风险

**依赖**：

- 依赖 <其他功能/外部服务> 完成后才能开始

**风险**：

- <潜在问题> — 缓解方案：<方案>

## 八、实现检查清单

> 实现完成后，逐条打勾，全部完成才能提 PR

- [ ] 所有验收标准有对应测试
- [ ] tsc --noEmit 通过，零 TypeScript 错误
- [ ] ESLint 通过
- [ ] 没有 console.log
- [ ] API 接口有 Zod 校验
- [ ] 敏感数据不出现在日志和响应中
- [ ] CLAUDE.md 的 Gotchas 已更新（如果发现新坑）

```

---

### Step 4 - 完成后告知用户

spec 写完后，输出一段摘要：
- spec 文件路径
- 验收标准数量
- 预计影响的文件列表（从技术设计推断）
- 建议的下一步：进入 Plan Mode 开始实现

提示用户：确认 spec 后，运行 `/implement-spec docs/specs/<功能名称>.md` 开始实现。
```