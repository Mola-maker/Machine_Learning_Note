---
name: weekly-evolve
description: 每周定时或用户要求"自迭代/再优化一轮"时触发。全自动：Propose→Probe→闸门→自动采纳/否决→提交→摘要推送，不等人工确认。
---
# 周度自迭代（全自动版）
触发：定时任务（每周）自动运行；用户手动要求时立即运行一轮。
1. **Propose**：汇总 checks 清单、EXPERIENCE、FAILED_IDEAS（先排除已否决路线），提出 2–4 个候选；
   通用（规则/技能层）与专用（单篇）分路；每个候选写明预期收益与风险。
2. **Probe**：候选在 2–3 篇样本上试行，跑 checks + RUBRIC 与基线对比，产物入 runs/<日期-主题>/。
3. **闸门（全过才采纳，任一失败自动否决）**：
   - 公式字符串 diff 为空（保真）；
   - 五项 checks 问题数不增；
   - RUBRIC 总提升 ≥0.5（小于视为噪声）；
   - heldout 体检不回退（防只对评估篇目有效）；
   - review-note 独立审校通过。
4. **Compose（自动）**：通过者全量执行并 git commit（信息含 run 号与分数前后）；
   否决者连同数据记入 FAILED_IDEAS；单轮采纳 ≤3 个，多轮递减。
5. **回滚**：下一轮 checks 若发现已采纳改法导致回退，自动 git revert 并在 EXPERIENCE 记因。
6. **沉淀与推送**：术语→GLOSSARY、经验→EXPERIENCE、结构→CHANGELOG、价值排序刷新（note-value-rank）；
   向用户推送本轮摘要（采纳/否决/回滚/分数），只汇报不待批。季度执行一次剪枝。
