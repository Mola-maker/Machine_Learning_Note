import ArchDiagram from './components/ArchDiagram'
import HarnessLoop from './components/HarnessLoop'
import notesData from './data/notes.json'
import highlightsData from './data/highlights.json'

const CHAPTERS = [
  { n: '簇 1', t: '经典神经网络地基', d: '反向传播、LeNet、LSTM、DBN、Xavier 初始化——一切故事的源头' },
  { n: '簇 2', t: '训练工具箱', d: 'AlexNet、Dropout、批归一化、Adam、层归一化——让深网络训得动' },
  { n: '簇 3', t: '视觉 CNN 与检测', d: 'VGG、GoogLeNet、ResNet、DenseNet、EfficientNet、Faster R-CNN、YOLO、U-Net' },
  { n: '簇 4', t: '序列模型', d: 'Word2Vec、GloVe、Seq2Seq、注意力机制、GRU——语言开始有了形状' },
  { n: '簇 5', t: 'Transformer', d: 'Attention Is All You Need、BERT、GPT 系——现代 AI 的转折点' },
  { n: '簇 6', t: '缩放与现代 LLM', d: '缩放定律、Chinchilla、LLaMA、MoE——大力出奇迹的学问' },
  { n: '簇 7', t: '对齐与 RLHF', d: 'InstructGPT、RLHF、DPO、宪法 AI——让模型听话的方法论' },
  { n: '簇 8', t: '推理与 Agent', d: 'CoT、ReAct、Tree of Thoughts、Toolformer——让模型会想、会做' },
  { n: '簇 9', t: '强化学习', d: 'DQN、A3C、PPO、AlphaGo/Zero/MuZero——在试错里长本事' },
  { n: '簇 10', t: '生成模型', d: 'VAE、GAN、扩散模型、Stable Diffusion、DiT——从噪声里造世界' },
  { n: '簇 11', t: '视觉与多模态', d: 'ViT、CLIP、DALL·E、Flamingo、BLIP-2、SAM、Whisper' },
  { n: '簇 12', t: '效率与应用', d: '蒸馏、LoRA、FlashAttention、RAG、AlphaFold——把强大变便宜' },
]
type Note = { title: string; chapter: string; score: number; verdict: string }
type Hi = { title: string; from: string; type: string; why: string }

export default function App() {
  const notes = (notesData as { notes: Note[] }).notes
  const his = (highlightsData as { items: Hi[] }).items
  return (
    <main className="page">
      <header className="hero">
        <h1>机器学习笔记 · 教学站</h1>
        <p>论文不必硬啃：每篇都有人话导读，先讲直觉、再上公式。72 篇地标论文排成一条路，走完它，你会亲手摸过现代 AI 的每一块地基。</p>
      </header>

      <section>
        <h2>一、先看懂全局：机器学习系统架构（动画）</h2>
        <ArchDiagram />
      </section>

      <section>
        <h2>二、学习路径：72 篇论文，12 站</h2>
        <ol className="path">
          {CHAPTERS.map(c => (
            <li key={c.n}><span className="chip">{c.n}</span>
              <div><strong>{c.t}</strong><p>{c.d}</p></div></li>
          ))}
        </ol>
      </section>

      <section>
        <h2>三、先读哪篇最值：笔记价值排序</h2>
        <table className="rank">
          <thead><tr><th>#</th><th>笔记</th><th>章节</th><th>价值分</th><th>价值判断</th></tr></thead>
          <tbody>
            {notes.map((n, i) => (
              <tr key={i}><td>{i + 1}</td><td>{n.title}</td><td>{n.chapter}</td>
                <td>{n.score ? n.score.toFixed(1) : '—'}</td><td>{n.verdict}</td></tr>
            ))}
          </tbody>
        </table>
      </section>

      <section>
        <h2>四、最值得一看的直观讲解</h2>
        <div className="cards">
          {his.map((h, i) => (
            <article key={i} className="card">
              <span className="chip">{h.type}</span>
              <h3>{h.title}</h3>
              <p>{h.why}</p>
              <footer>出处：{h.from}</footer>
            </article>
          ))}
        </div>
      </section>

      <section>
        <h2>五、这套笔记如何自己越变越好（动画）</h2>
        <HarnessLoop />
      </section>
    </main>
  )
}
