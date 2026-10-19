---
name: using-note-skills
description: 会话开始或不确定该用哪个笔记技能时触发：先读本技能完成路由，再动手。任何笔记库任务的第一步。
---
# 入口路由
1. 读仓库根 `AGENTS.md` 与 `INDEX.md`，确认目标笔记与所属章节。
2. 按任务选技能：新材料入库→ingest-note；文字润色/规范→polish-language；
   断链/孤儿/索引→link-weaver；公式问题→formula-guard；交付前审校→review-note；
   周期性改进→weekly-evolve。
3. 动手前跑 `checks/run_all.sh` 记录基线问题数；完成后复跑，只降不升才算完成。
4. 结束时履行 AGENTS.md 的沉淀义务（术语/经验/否决/变更四去向）。
