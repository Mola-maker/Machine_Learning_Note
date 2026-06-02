# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a structured AI/ML self-study repository — not a software project. It organizes **79 landmark papers** across 12 chronological clusters, paired with **24 reference implementations** in `github_projects/`.

The master reading plan is `AI_Reading_Roadmap.md`. Read it first before doing anything else.

## Repository structure

```
01-foundations/          # Cluster 1 — Classical Neural Networks (backprop, LeNet, LSTM, DBN, Xavier init)
02-training-toolkit/     # Cluster 2 — Training tricks (AlexNet, Dropout, BatchNorm, Adam, LayerNorm)
03-vision-cnns/          # Cluster 3 — CNN evolution + detection (VGG, ResNet, YOLO, U-Net, etc.)
04-sequence-models/      # Cluster 4 — RNNs and word embeddings (Word2Vec, Seq2Seq, Bahdanau attention)
05-transformers/         # Cluster 5 — Transformers (Attention Is All You Need, BERT, GPT-1/2/3, T5, RoBERTa)
06-llm-scaling/          # Cluster 6 — Scaling laws + modern LLMs (Chinchilla, LLaMA, GPT-4, MoE)
07-alignment-rlhf/       # Cluster 7 — Alignment (InstructGPT, RLHF, DPO, Constitutional AI)
08-reasoning-agents/     # Cluster 8 — Reasoning & agents (CoT, ReAct, Tree of Thoughts, Toolformer)
09-reinforcement-learning/ # Cluster 9 — RL core (DQN, A3C, PPO, AlphaGo/Zero/MuZero)
10-generative-models/    # Cluster 10 — VAEs, GANs, diffusion (DDPM, Stable Diffusion, DiT)
11-vision-multimodal/    # Cluster 11 — ViT, CLIP, DALL·E, Flamingo, BLIP-2, SAM, Whisper
12-efficiency-applications/ # Cluster 12 — Distillation, LoRA, FlashAttention, RAG, AlphaFold
github_projects/         # Cloned reference implementations (see github_projects/INDEX.md)
```

Each chapter directory contains PDFs and optional `.md` notes for each paper.

## github_projects organization

```
educational/          # nn-zero-to-hero, nanoGPT, minGPT, LLMs-from-scratch, d2l-en, llm-course, annotated-dl-papers
paper-implementations/ # vit-pytorch, x-transformers, denoising-diffusion-pytorch, CLIP, whisper, SAM
production-frameworks/ # transformers, diffusers, llama.cpp, llama
efficiency-tools/     # LoRA, flash-attention
reinforcement-learning/ # spinningup, stable-baselines3
awesome-lists/        # Awesome-LLM, Prompt-Engineering-Guide, applied-ml
```

See `github_projects/INDEX.md` for which repo pairs with which cluster/paper.

## Common commands

```bash
# Refresh all cloned repos (idempotent — skips already-cloned repos)
bash clone_repos.sh

# Update a specific repo to latest
cd github_projects/<category>/<repo> && git pull --depth 1

# Run MATLAB code (MATLAB must be running locally with the MCP server connected)
# Use the MATLAB MCP tools: evaluate_matlab_code, run_matlab_file, run_matlab_test_file
```

## Working with papers and code

- PDFs in chapter directories are the original papers. Paths follow the pattern `NN-AuthorYear-ShortName.pdf`.
- Some papers have accompanying `.md` notes (e.g., `01-foundations/01-Rumelhart1986-Backprop.md`). These are the user's personal reading notes.
- When asked about a paper, check both the PDF and any `.md` notes in its chapter directory.
- The `labmlai/annotated_deep_learning_paper_implementations` repo in `educational/` has 60+ paper implementations with side-by-side notes — it's the first place to look when the user wants to see code for a specific paper.
- `rasbt/LLMs-from-scratch` is the companion code for Sebastian Raschka's book — covers pretraining through DPO.

## Reading workflow (from AI_Reading_Roadmap.md)

1. Work through clusters in order (1 → 12). Each cluster builds on the previous.
2. For each paper: read abstract → figures → conclusion → intro → methods (not linearly).
3. Starred papers (★) form a ~25-paper "minimum viable" path.
4. Re-read foundational papers (Transformer, ResNet, DDPM, PPO) at least twice.

## MATLAB

MATLAB is available via MCP tools when a local MATLAB session is running. The `detect_matlab_toolboxes` tool can check available toolboxes. Use MATLAB for any `.m` or `.mlx` files in the repo.
