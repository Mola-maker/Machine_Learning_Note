# AI Reading Roadmap — 72 Landmark Papers with Original Sources

> Curated 2026-05-19. Every link points to the original preprint or journal version.
> Reading order is **top-to-bottom across clusters** — each cluster builds on the previous.
> If short on time, read the **starred (★)** papers first — that's a ~25-paper "minimum viable" path.

---

## How to use this roadmap

1. Work through clusters in order (1 → 12). Each cluster is a coherent topic; don't skip ahead until the prior cluster's starred papers feel intuitive.
2. For each paper: read **abstract → figures → conclusion → intro → methods**. Don't read linearly.
3. After each cluster, write a one-paragraph summary of *why each paper mattered* — that's the test of whether you actually absorbed it.
4. Re-read foundational papers (Transformer, ResNet, DDPM, PPO) at least twice across the journey — they get deeper.

Estimated time: 4–6 months at ~3 papers/week with implementation side-projects.

---

## Cluster 1 — Classical Neural Network Foundations

The pre-2012 ideas everything else stands on. Short cluster — read for context, not depth.

| # | Paper | Year | Original Source |
|---|---|---|---|
| 1 ★ | **Learning representations by back-propagating errors** — Rumelhart, Hinton, Williams | 1986 | https://www.nature.com/articles/323533a0 |
| 2 | **Gradient-Based Learning Applied to Document Recognition** (LeNet) — LeCun et al. | 1998 | http://yann.lecun.com/exdb/publis/pdf/lecun-98.pdf |
| 3 | **Long Short-Term Memory** — Hochreiter & Schmidhuber | 1997 | https://www.bioinf.jku.at/publications/older/2604.pdf |
| 4 | **A Fast Learning Algorithm for Deep Belief Nets** — Hinton, Osindero, Teh | 2006 | https://www.cs.toronto.edu/~hinton/absps/fastnc.pdf |
| 5 | **Understanding the difficulty of training deep feedforward networks** (Xavier init) — Glorot & Bengio | 2010 | https://proceedings.mlr.press/v9/glorot10a.html |

---

## Cluster 2 — Deep Learning Training Toolkit

The training tricks that made deep nets actually trainable. Short, dense, foundational.

| # | Paper | Year | Original Source |
|---|---|---|---|
| 6 ★ | **ImageNet Classification with Deep CNNs** (AlexNet) — Krizhevsky, Sutskever, Hinton | 2012 | https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html |
| 7 | **Dropout: A Simple Way to Prevent Neural Networks from Overfitting** — Srivastava et al. | 2014 | https://jmlr.org/papers/v15/srivastava14a.html |
| 8 ★ | **Batch Normalization** — Ioffe & Szegedy | 2015 | https://arxiv.org/abs/1502.03167 |
| 9 ★ | **Adam: A Method for Stochastic Optimization** — Kingma & Ba | 2014 | https://arxiv.org/abs/1412.6980 |
| 10 | **Layer Normalization** — Ba, Kiros, Hinton | 2016 | https://arxiv.org/abs/1607.06450 |

---

## Cluster 3 — Computer Vision: CNNs to Detection

Modern vision in 8 papers. Read in order — each fixes a flaw in the previous.

| # | Paper | Year | Original Source |
|---|---|---|---|
| 11 | **Very Deep Convolutional Networks** (VGG) — Simonyan & Zisserman | 2014 | https://arxiv.org/abs/1409.1556 |
| 12 | **Going Deeper with Convolutions** (GoogLeNet/Inception) — Szegedy et al. | 2014 | https://arxiv.org/abs/1409.4842 |
| 13 ★ | **Deep Residual Learning for Image Recognition** (ResNet) — He et al. | 2015 | https://arxiv.org/abs/1512.03385 |
| 14 | **Densely Connected Convolutional Networks** (DenseNet) — Huang et al. | 2016 | https://arxiv.org/abs/1608.06993 |
| 15 | **EfficientNet** — Tan & Le | 2019 | https://arxiv.org/abs/1905.11946 |
| 16 | **Faster R-CNN** — Ren, He, Girshick, Sun | 2015 | https://arxiv.org/abs/1506.01497 |
| 17 | **You Only Look Once (YOLO)** — Redmon et al. | 2015 | https://arxiv.org/abs/1506.02640 |
| 18 | **U-Net: Convolutional Networks for Biomedical Image Segmentation** — Ronneberger, Fischer, Brox | 2015 | https://arxiv.org/abs/1505.04597 |

---

## Cluster 4 — Sequence Models & Word Embeddings

The bridge between classical NLP and Transformers. Bahdanau's attention paper (#22) is the conceptual seed of everything in Cluster 5.

| # | Paper | Year | Original Source |
|---|---|---|---|
| 19 ★ | **Efficient Estimation of Word Representations in Vector Space** (Word2Vec) — Mikolov et al. | 2013 | https://arxiv.org/abs/1301.3781 |
| 20 | **GloVe: Global Vectors for Word Representation** — Pennington, Socher, Manning | 2014 | https://nlp.stanford.edu/pubs/glove.pdf |
| 21 | **Sequence to Sequence Learning with Neural Networks** — Sutskever, Vinyals, Le | 2014 | https://arxiv.org/abs/1409.3215 |
| 22 ★ | **Neural Machine Translation by Jointly Learning to Align and Translate** (Bahdanau attention) — Bahdanau, Cho, Bengio | 2014 | https://arxiv.org/abs/1409.0473 |
| 23 | **Learning Phrase Representations using RNN Encoder–Decoder** (GRU) — Cho et al. | 2014 | https://arxiv.org/abs/1406.1078 |

---

## Cluster 5 — Transformers & Pretraining

The pivot point of modern AI. Read #24 three times.

| # | Paper | Year | Original Source |
|---|---|---|---|
| 24 ★★ | **Attention Is All You Need** — Vaswani et al. | 2017 | https://arxiv.org/abs/1706.03762 |
| 25 ★ | **BERT: Pre-training of Deep Bidirectional Transformers** — Devlin et al. | 2018 | https://arxiv.org/abs/1810.04805 |
| 26 | **Improving Language Understanding by Generative Pre-Training** (GPT-1) — Radford et al. | 2018 | https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf |
| 27 | **Language Models are Unsupervised Multitask Learners** (GPT-2) — Radford et al. | 2019 | https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf |
| 28 ★ | **Language Models are Few-Shot Learners** (GPT-3) — Brown et al. | 2020 | https://arxiv.org/abs/2005.14165 |
| 29 | **Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer** (T5) — Raffel et al. | 2019 | https://arxiv.org/abs/1910.10683 |
| 30 | **RoBERTa: A Robustly Optimized BERT Pretraining Approach** — Liu et al. | 2019 | https://arxiv.org/abs/1907.11692 |

---

## Cluster 6 — Scaling Laws & Modern LLMs

Why bigger works, and how to build it cheaper.

| # | Paper | Year | Original Source |
|---|---|---|---|
| 31 ★ | **Scaling Laws for Neural Language Models** — Kaplan et al. | 2020 | https://arxiv.org/abs/2001.08361 |
| 32 ★ | **Training Compute-Optimal Large Language Models** (Chinchilla) — Hoffmann et al. | 2022 | https://arxiv.org/abs/2203.15556 |
| 33 | **PaLM: Scaling Language Modeling with Pathways** — Chowdhery et al. | 2022 | https://arxiv.org/abs/2204.02311 |
| 34 ★ | **LLaMA: Open and Efficient Foundation Language Models** — Touvron et al. | 2023 | https://arxiv.org/abs/2302.13971 |
| 35 | **Llama 2: Open Foundation and Fine-Tuned Chat Models** — Touvron et al. | 2023 | https://arxiv.org/abs/2307.09288 |
| 36 | **GPT-4 Technical Report** — OpenAI | 2023 | https://arxiv.org/abs/2303.08774 |
| 37 | **Switch Transformer: Scaling to Trillion Parameter Models** — Fedus, Zoph, Shazeer | 2021 | https://arxiv.org/abs/2101.03961 |
| 38 | **Mixtral of Experts** — Jiang et al. | 2024 | https://arxiv.org/abs/2401.04088 |

---

## Cluster 7 — Alignment, Instruction Tuning, RLHF

How raw pretrained models become useful assistants.

| # | Paper | Year | Original Source |
|---|---|---|---|
| 39 ★ | **Deep Reinforcement Learning from Human Preferences** — Christiano et al. | 2017 | https://arxiv.org/abs/1706.03741 |
| 40 ★ | **Training language models to follow instructions with human feedback** (InstructGPT) — Ouyang et al. | 2022 | https://arxiv.org/abs/2203.02155 |
| 41 | **Training a Helpful and Harmless Assistant with RLHF** — Bai et al. (Anthropic) | 2022 | https://arxiv.org/abs/2204.05862 |
| 42 | **Constitutional AI: Harmlessness from AI Feedback** — Bai et al. | 2022 | https://arxiv.org/abs/2212.08073 |
| 43 ★ | **Direct Preference Optimization** (DPO) — Rafailov et al. | 2023 | https://arxiv.org/abs/2305.18290 |

---

## Cluster 8 — Reasoning, Tools & Agents

Prompting and inference-time techniques.

| # | Paper | Year | Original Source |
|---|---|---|---|
| 44 ★ | **Chain-of-Thought Prompting Elicits Reasoning in Large Language Models** — Wei et al. | 2022 | https://arxiv.org/abs/2201.11903 |
| 45 | **Self-Consistency Improves Chain of Thought Reasoning** — Wang et al. | 2022 | https://arxiv.org/abs/2203.11171 |
| 46 ★ | **ReAct: Synergizing Reasoning and Acting in Language Models** — Yao et al. | 2022 | https://arxiv.org/abs/2210.03629 |
| 47 | **Tree of Thoughts** — Yao et al. | 2023 | https://arxiv.org/abs/2305.10601 |
| 48 | **Toolformer: Language Models Can Teach Themselves to Use Tools** — Schick et al. | 2023 | https://arxiv.org/abs/2302.04761 |

---

## Cluster 9 — Reinforcement Learning Core

Read alongside Cluster 7 — RLHF stands on PPO.

| # | Paper | Year | Original Source |
|---|---|---|---|
| 49 ★ | **Playing Atari with Deep Reinforcement Learning** (DQN) — Mnih et al. | 2013 | https://arxiv.org/abs/1312.5602 |
| 50 | **Human-level control through deep reinforcement learning** (DQN Nature) — Mnih et al. | 2015 | https://www.nature.com/articles/nature14236 |
| 51 | **Asynchronous Methods for Deep Reinforcement Learning** (A3C) — Mnih et al. | 2016 | https://arxiv.org/abs/1602.01783 |
| 52 ★ | **Proximal Policy Optimization Algorithms** (PPO) — Schulman et al. | 2017 | https://arxiv.org/abs/1707.06347 |
| 53 | **Mastering the game of Go with deep neural networks and tree search** (AlphaGo) — Silver et al. | 2016 | https://www.nature.com/articles/nature16961 |
| 54 | **Mastering Chess and Shogi by Self-Play** (AlphaZero) — Silver et al. | 2017 | https://arxiv.org/abs/1712.01815 |
| 55 | **Mastering Atari, Go, Chess and Shogi by Planning with a Learned Model** (MuZero) — Schrittwieser et al. | 2019 | https://arxiv.org/abs/1911.08265 |

---

## Cluster 10 — Generative Models: VAE, GAN, Diffusion

| # | Paper | Year | Original Source |
|---|---|---|---|
| 56 ★ | **Auto-Encoding Variational Bayes** (VAE) — Kingma & Welling | 2013 | https://arxiv.org/abs/1312.6114 |
| 57 ★ | **Generative Adversarial Nets** — Goodfellow et al. | 2014 | https://arxiv.org/abs/1406.2661 |
| 58 | **A Style-Based Generator Architecture for GANs** (StyleGAN) — Karras, Laine, Aila | 2018 | https://arxiv.org/abs/1812.04948 |
| 59 ★ | **Denoising Diffusion Probabilistic Models** (DDPM) — Ho, Jain, Abbeel | 2020 | https://arxiv.org/abs/2006.11239 |
| 60 | **Denoising Diffusion Implicit Models** (DDIM) — Song, Meng, Ermon | 2020 | https://arxiv.org/abs/2010.02502 |
| 61 ★ | **High-Resolution Image Synthesis with Latent Diffusion Models** (Stable Diffusion) — Rombach et al. | 2021 | https://arxiv.org/abs/2112.10752 |
| 62 | **Classifier-Free Diffusion Guidance** — Ho & Salimans | 2022 | https://arxiv.org/abs/2207.12598 |
| 63 | **Scalable Diffusion Models with Transformers** (DiT) — Peebles & Xie | 2022 | https://arxiv.org/abs/2212.09748 |

---

## Cluster 11 — Vision Transformers & Multimodal

| # | Paper | Year | Original Source |
|---|---|---|---|
| 64 ★ | **An Image is Worth 16x16 Words** (ViT) — Dosovitskiy et al. | 2020 | https://arxiv.org/abs/2010.11929 |
| 65 ★ | **Learning Transferable Visual Models From Natural Language Supervision** (CLIP) — Radford et al. | 2021 | https://arxiv.org/abs/2103.00020 |
| 66 | **Zero-Shot Text-to-Image Generation** (DALL·E) — Ramesh et al. | 2021 | https://arxiv.org/abs/2102.12092 |
| 67 | **Flamingo: a Visual Language Model for Few-Shot Learning** — Alayrac et al. | 2022 | https://arxiv.org/abs/2204.14198 |
| 68 | **BLIP-2: Bootstrapping Language-Image Pre-training** — Li et al. | 2023 | https://arxiv.org/abs/2301.12597 |
| 69 | **Segment Anything** (SAM) — Kirillov et al. | 2023 | https://arxiv.org/abs/2304.02643 |
| 70 | **Robust Speech Recognition via Large-Scale Weak Supervision** (Whisper) — Radford et al. | 2022 | https://arxiv.org/abs/2212.04356 |

---

## Cluster 12 — Efficient Models, Retrieval & Killer Applications

| # | Paper | Year | Original Source |
|---|---|---|---|
| 71 ★ | **Distilling the Knowledge in a Neural Network** — Hinton, Vinyals, Dean | 2015 | https://arxiv.org/abs/1503.02531 |
| 72 ★ | **LoRA: Low-Rank Adaptation of Large Language Models** — Hu et al. | 2021 | https://arxiv.org/abs/2106.09685 |
| 73 | **FlashAttention: Fast and Memory-Efficient Exact Attention** — Dao et al. | 2022 | https://arxiv.org/abs/2205.14135 |
| 74 | **QLoRA: Efficient Finetuning of Quantized LLMs** — Dettmers et al. | 2023 | https://arxiv.org/abs/2305.14314 |
| 75 ★ | **Retrieval-Augmented Generation for Knowledge-Intensive NLP** (RAG) — Lewis et al. | 2020 | https://arxiv.org/abs/2005.11401 |
| 76 ★ | **Highly accurate protein structure prediction with AlphaFold** — Jumper et al. | 2021 | https://www.nature.com/articles/s41586-021-03819-2 |
| 77 | **Evaluating Large Language Models Trained on Code** (Codex) — Chen et al. | 2021 | https://arxiv.org/abs/2107.03374 |
| 78 | **Competition-Level Code Generation with AlphaCode** — Li et al. | 2022 | https://arxiv.org/abs/2203.07814 |
| 79 | **RT-2: Vision-Language-Action Models** — Brohan et al. | 2023 | https://arxiv.org/abs/2307.15818 |

---

## Reading Order Summary (the 25-paper minimum path)

If you can only read 25, this order is self-contained:

1. Rumelhart 1986 (backprop)
2. AlexNet
3. BatchNorm
4. Adam
5. ResNet
6. Word2Vec
7. Bahdanau attention
8. **Attention Is All You Need** (×2)
9. BERT
10. GPT-3
11. Scaling Laws (Kaplan)
12. Chinchilla
13. LLaMA
14. Christiano 2017 (RLHF foundation)
15. InstructGPT
16. DPO
17. Chain-of-Thought
18. ReAct
19. DQN (Mnih 2013)
20. PPO
21. VAE
22. GAN
23. DDPM
24. Latent Diffusion
25. ViT + CLIP (read as a pair)
26. LoRA
27. RAG
28. AlphaFold

---

## Where to find papers when a link breaks

- **arXiv** (https://arxiv.org/) — primary source for almost everything post-2014
- **Papers with Code** (https://paperswithcode.com/) — paper + code in one place
- **Semantic Scholar** (https://www.semanticscholar.org/) — better citation graph navigation
- **Google Scholar** — last resort for hard-to-find PDFs
- **OpenReview** — for ICLR/NeurIPS reviewed versions with discussion

For Nature/Science papers behind paywalls (AlphaGo, AlphaFold), search the same title on arXiv — most have a preprint version.
