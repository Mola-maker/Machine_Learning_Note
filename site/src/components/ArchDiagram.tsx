import { useEffect, useState } from 'react'

// 机器学习系统架构动画：数据 → 特征 → 模型 → 评估 →（反馈回流）特征/模型
// 节点依次点亮，连接线用行军蚁虚线动画表示数据流动；自动播放，可暂停/单步。
const NODES = [
  { id: 'data', x: 70, label: '数据', sub: '样本与标签' },
  { id: 'feat', x: 230, label: '特征', sub: '缩放 · 映射' },
  { id: 'model', x: 390, label: '模型', sub: '假设集 + 学习算法' },
  { id: 'eval', x: 550, label: '评估', sub: '训练误差 / 泛化误差' },
]
const STEPS = [
  '先从数据开始：样本 x 是"题目"，标签 y 是"参考答案"——没有这两样，学习无从谈起。',
  '特征是把题目"翻译"成模型听得懂的样子：缩放、映射，就像把难题拆成小台阶。',
  '模型在假设集里挑一条最合适的规律：拟合不是背答案，而是找能推广的那条线。',
  '最后看泛化：考场上没见过的题也能做对，才算真学会；不行就沿虚线回去改特征、换模型。',
]
export default function ArchDiagram() {
  const [step, setStep] = useState(0)
  const [play, setPlay] = useState(true)
  useEffect(() => {
    if (!play) return
    const t = setInterval(() => setStep(s => (s + 1) % 4), 2200)
    return () => clearInterval(t)
  }, [play])
  return (
    <figure className="diagram">
      <svg viewBox="0 0 680 240" role="img" aria-label="机器学习系统架构动画图">
        <defs>
          <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M0,0 L10,5 L0,10 z" fill="#5b8def" />
          </marker>
        </defs>
        {NODES.slice(0, 3).map((n, i) => (
          <line key={i} x1={n.x + 56} y1={90} x2={NODES[i + 1].x - 56} y2={90}
            className={'flow' + (step === i ? ' flow-on' : '')} markerEnd="url(#arr)" />
        ))}
        <path d="M550,126 C550,205 230,205 230,132" className={'flow feedback' + (step === 3 ? ' flow-on' : '')} markerEnd="url(#arr)" />
        {NODES.map((n, i) => (
          <g key={n.id} className={'node' + (step === i ? ' node-on' : '')}>
            <rect x={n.x - 56} y={54} width={112} height={72} rx={12} />
            <text x={n.x} y={88} className="node-title">{n.label}</text>
            <text x={n.x} y={110} className="node-sub">{n.sub}</text>
          </g>
        ))}
        <text x={390} y={222} className="note-text">没学会 → 回去改特征 / 换模型，这就是迭代</text>
      </svg>
      <figcaption>
        <strong>第 {step + 1} 步：</strong>{STEPS[step]}
        <span className="controls">
          <button onClick={() => setPlay(p => !p)}>{play ? '暂停' : '播放'}</button>
          <button onClick={() => setStep(s => (s + 1) % 4)}>单步</button>
        </span>
      </figcaption>
    </figure>
  )
}
