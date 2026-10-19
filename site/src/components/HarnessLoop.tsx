import { useEffect, useState } from 'react'
// 笔记库自迭代 harness 架构动画：Propose → Probe → 闸门 → Compose → 沉淀（回流）
const PHASES = [
  { label: 'Propose', desc: '汇总 checks 与经验，提 2–4 个候选改法（先查失败清单）' },
  { label: 'Probe', desc: '在 2–3 篇样本试行，跑 checks + RUBRIC 与基线对比' },
  { label: '闸门', desc: '公式零改动 · 检查不增 · 提升≥0.5 · 留出集不回退 · 独立审校' },
  { label: 'Compose', desc: '全过自动采纳并提交；否决记入失败清单；回退自动 revert' },
  { label: '沉淀', desc: '术语/经验/否决/变更四层回写，价值排序与站点数据刷新' },
]
export default function HarnessLoop() {
  const [i, setI] = useState(0)
  useEffect(() => {
    const t = setInterval(() => setI(v => (v + 1) % PHASES.length), 2400)
    return () => clearInterval(t)
  }, [])
  const R = 92, cx = 160, cy = 130
  return (
    <figure className="diagram">
      <svg viewBox="0 0 640 260" role="img" aria-label="自迭代 harness 循环动画图">
        <circle cx={cx} cy={cy} r={R} className="loop-ring" />
        {PHASES.map((p, k) => {
          const a = (k / PHASES.length) * Math.PI * 2 - Math.PI / 2
          const x = cx + R * Math.cos(a), y = cy + R * Math.sin(a)
          return (
            <g key={p.label} className={'node small' + (i === k ? ' node-on' : '')}>
              <circle cx={x} cy={y} r={30} />
              <text x={x} y={y + 4} className="node-title sm">{p.label}</text>
            </g>
          )
        })}
        <text x={cx} y={cy - 4} className="note-text">自迭代</text>
        <text x={cx} y={cy + 16} className="note-text">全自动</text>
        <text x={350} y={86} className="desc-title">{PHASES[i].label}</text>
        <foreignObject x={350} y={96} width={270} height={110}>
          <div className="svg-desc">{PHASES[i].desc}</div>
        </foreignObject>
      </svg>
      <figcaption>每周自动跑一轮：闸门全过才采纳，分数回退自动回滚；用户只看摘要。</figcaption>
    </figure>
  )
}
