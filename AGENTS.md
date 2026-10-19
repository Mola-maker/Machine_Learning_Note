# Machine Learning Note — Agent 工作守则

本仓库是 Obsidian 机器学习笔记库（中文为主），主线是 72 篇地标论文精读（02_paperML，12 个簇，脊柱为 AI_Reading_Roadmap.md）。
Agent 在此的一切工作目标：让笔记更准确、更一致、更好检索，且**不改变作者的技术结论与讲解顺序**。

## 动手前（技能路由）
- 先读 `INDEX.md` 定位目标笔记，只加载目标笔记及其一跳双链，不全库乱翻。
- 按任务查技能（`skills/`，描述即触发条件）：入库→ingest-note；语言→polish-language；
  链接→link-weaver；公式→formula-guard；审校→review-note；周迭代→weekly-evolve。
- 拿不准用哪个，先读 `skills/using-note-skills/SKILL.md`。

## 五条红线
1. 不改公式语义：公式字符串在修改前后必须可逐字 diff 为空集（排版空格除外需说明）。
2. 删正文须留痕可回滚：删减超过一句话的改动，必须先在 runs/ 留 proposal 与原文快照，
   且改后 checks 不增、RUBRIC 不降才可自动采纳；一旦后续检查回退，自动 revert 并记 FAILED_IDEAS。
3. 不编造引用：出处、数据、结论没有来源就不写；不确定的标注 `[待确认]`。
4. `eval/` 只读：golden 与 heldout 是标尺，任何优化不得针对其内容投机（RRSI 留出集纪律）。
5. 遇疑似密钥/隐私（token、密码、个人证件信息）立即停手报告，不复制不外传。

## 文风总则（用户 2026-10-19 指示）
- **平易近人，富有深度**：所有教学文案与展示流程先给直觉与生活化类比，再进入形式化；
  语言亲切好读，但不牺牲严谨——限定词、条件、边界一个不少。动画与页面文案同样适用。

## 写作规范（摘要，全文见 skills/polish-language）
- frontmatter 必备：title / tags / created / updated / status(draft|reviewed|mastered)。
- 全篇仅一个一级标题；术语首次出现给中英对照；译名以 `GLOSSARY.md` 为单一事实源。
- 中英文、中文与数字之间留空格；公式用 LaTeX；例题数字与引用不动。

## “完成”的定义
- `checks/` 五项检查全跑且问题数较修改前不增；
- 改动经 review-note 独立审校过目（只看 diff 挑错）；
- 结论写入 `runs/<日期-主题>/verdict.md`。

## 沉淀义务（每轮迭代结束必做）
- 新术语/译名决定 → `GLOSSARY.md`；踩坑与有效做法 → `EXPERIENCE.md`；
- 被否决的改法 → `FAILED_IDEAS.md`（防重复试错）；结构性变更 → `CHANGELOG.md`；
- 用户的修改意见 → polish-language 的风格附则（带置信度）。

## 自迭代纪律（Harness² 循环 + RRSI 刹车）
- 循环：Propose（2–4 个候选，通用/专用分路，避开 FAILED_IDEAS）→ Probe（2–3 篇样本试行，
  checks + RUBRIC 与基线对比）→ Compose（只采纳实测提升者）→ 回写四层沉淀。
- 刹车：单轮采纳 ≤3 个改法且多轮递减；RUBRIC 提升 <0.5 分视为噪声不采纳；
  只对评估篇目有效的改法一律否决；维护成本上涨须由实测收益买单；季度剪枝闲置技能与规则。
- 全自动（用户 2026-10-19 指示）：循环由定时任务自动触发，闸门全过即自动采纳并提交，
  不等人工确认；每轮结束只向用户推送摘要（采纳了什么、分数前后、回滚了什么）。
  自动采纳的硬前提：公式 diff 为空、五项 checks 不增、RUBRIC 提升达标、review-note 审校通过；
  任一不满足 → 自动否决并记录，不例外放行。
