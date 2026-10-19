# 精读 30 篇选定 · 2026-10-19

由用户授权选定（原定用户亲自圈定 golden/heldout，用户改授代理选择）。
口径：72 篇地标中选 30 篇做精读——已完成精读笔记的 12 篇自动在列；新增 18 篇以路线图 ★ 最小路径为骨，
再按"对当前主线（自训 LLM + AI Infra 方向）的枢纽价值"取舍。阅读顺序沿路线图簇序。

## 已完成（12 篇，精读笔记已在库）
| # | 论文 | 簇 | 备注 |
|---|---|---|---|
| 1 | Backprop（Rumelhart 1986）★ | 1 地基 | golden |
| 2 | LeNet（LeCun 1998） | 1 地基 | heldout |
| 3 | LSTM（Hochreiter 1997） | 1 地基 | golden |
| 4 | DBN（Hinton 2006） | 1 地基 | 自由池 |
| 5 | Xavier 初始化（Glorot 2010） | 1 地基 | heldout |
| 6 | AlexNet（Krizhevsky 2012）★ | 2 工具箱 | golden |
| 7 | Dropout（Srivastava 2014） | 2 工具箱 | heldout |
| 8 | BatchNorm（Ioffe 2015）★ | 2 工具箱 | golden |
| 9 | Adam（Kingma 2014）★ | 2 工具箱 | golden |
| 10 | LayerNorm（Ba 2016） | 2 工具箱 | golden |
| 11 | VGG（Simonyan 2014） | 3 视觉 | heldout |
| 12 | GoogLeNet（Szegedy 2014） | 3 视觉 | heldout |

## 新增精读（18 篇，按阅读顺序）
| 序 | # | 论文 | 簇 | 为什么入选 |
|---|---|---|---|---|
| 1 | 13 | ResNet（He 2015）★ | 3 视觉 | 簇 3 收官；残差连接是后面一切深网络的默认件，VGG/GoogLeNet 都在前指它 |
| 2 | 22 | Bahdanau Attention（2014）★ | 4 序列 | 注意力的种子：先懂"对齐"再读 Transformer，事半功倍 |
| 3 | 24 | Attention Is All You Need（2017）★★ | 5 Transformer | 全路线图的枢纽，路线图要求读三遍；LayerNorm 的"延迟引爆"在此兑现 |
| 4 | 25 | BERT（Devlin 2018）★ | 5 Transformer | 预训练范式的另一半（双向编码），与 GPT 线对照读 |
| 5 | 28 | GPT-3（Brown 2020）★ | 5 Transformer | few-shot 与规模涌现的原点，现代 LLM 的起点叙事 |
| 6 | 31 | Scaling Laws（Kaplan 2020）★ | 6 规模 | 训 0.6B 的直接方法论：参数/数据/算力怎么配比 |
| 7 | 32 | Chinchilla（Hoffmann 2022）★ | 6 规模 | 对 Kaplan 的修正（compute-optimal），与上一篇对照读 |
| 8 | 34 | LLaMA（Touvron 2023）★ | 6 规模 | 开源现代 LLM 的工程范本，与自训项目同量级思路 |
| 9 | 40 | InstructGPT（Ouyang 2022）★ | 7 对齐 | RLHF 全流程的完整落地，理解"助手"如何炼成 |
| 10 | 43 | DPO（Rafailov 2023）★ | 7 对齐 | 把 RLHF 简化成分类损失，对齐方法的现代默认选项 |
| 11 | 44 | Chain-of-Thought（Wei 2022）★ | 8 推理 | 推理时计算的开山之作，篇幅短、影响大 |
| 12 | 46 | ReAct（Yao 2022）★ | 8 推理 | 推理+行动交错，Agent 范式的源头（与本库的 harness 主题互文） |
| 13 | 59 | DDPM（Ho 2020）★ | 10 生成 | 扩散模型的标准表述，生成线只需这一篇打底 |
| 14 | 61 | Latent Diffusion（Rombach 2021）★ | 10 生成 | Stable Diffusion 本体：把扩散搬进潜空间的工程关键 |
| 15 | 64 | ViT（Dosovitskiy 2020）★ | 11 多模态 | Transformer 吃掉视觉的起点，与簇 3 的 CNN 线对照 |
| 16 | 65 | CLIP（Radford 2021）★ | 11 多模态 | 图文对齐的范式，多模态一切工作的地基 |
| 17 | 72 | LoRA（Hu 2021）★ | 12 高效 | 微调的默认工具，参数高效方法的代表 |
| 18 | 73 | FlashAttention（Dao 2022） | 12 高效 | 路线图未标 ★ 但破格入选：AI Infra 的标志性工作——IO 感知的注意力实现，与职业主线直接相关 |

节奏参考：沿用路线图估算 ~3 篇/周，新增 18 篇约 6 周读完；每篇按"摘要→图→结论→引言→方法"读法，并按 ingest-note 技能落精读笔记。

## 备选梯队（下一批前 5）
19 Word2Vec（簇 4 开篇，词向量直觉）· 56 VAE（簇 10，扩散的前置数学）· 57 GAN（簇 10）· 52 PPO（簇 9，RLHF 的算法本体）· 39 Christiano 2017（簇 7，RLHF 思想源头）

## eval 标尺（从已完成 12 篇中划定，见 eval/golden 与 eval/heldout）
- golden（范文标尺 6 篇）：Adam 4.9 / Backprop 4.8 / BatchNorm 4.8 / LSTM 4.7 / AlexNet 4.6 / LayerNorm 4.6（分数为 runs/value-rank-2026-10-19.md 的五维评分）
- heldout（留出集 5 篇，自迭代永不触碰、只做回归对照）：Dropout 4.5 / LeNet 4.4 / Xavier 4.3 / GoogLeNet 4.2 / VGG 3.9
- 自由池：DBN（可被迭代优化，不作标尺）
