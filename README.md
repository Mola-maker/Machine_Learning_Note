# Mola-maker's Study Vault

A public log of what I'm learning: math, ML, ADAS for two-wheelers, algorithms, and English (CET6).
Stu in JLU

## About me
Undergraduate student. Strong interest in math (October competition prep) and ML/LLM fundamentals.
Currently building an ADAS system for two-wheel vehicles.
Fervantly in learning everything about Coding 
## What's in this vault

- `daily/` — daily learning logs
- `00.Machine Learning Note/` —ML course notes, paper notes, fast.ai,Git usage 
- (waiting for establishment)
- `10-math/` — calculus, linear algebra, competition problems
- `20-code/` — Codeforces solutions, algorithms in C++/Python
- `30-ml/` — ML course notes, paper notes, fast.ai
- `40-adas/` — ADAS project log: design, bugs, decisions
- `50-cet6/` — CET6 vocab and timed-section practice
- `90-meta/` — weekly reviews, plans, reflections

## Current focus (May 2026)

- Math final on July 1
- Daily Codeforces in C++, no AI-generated code
- ADAS perception pipeline
- Python + NumPy fundamentals (CS231n)

## How to read this vault

Browse folders directly on GitHub, or clone and open in Obsidian for the full graph view and link navigation.

## Contact

Feel free to open an issue or fork. Always happy to talk to like-minded learners.

## Suggestion Claude gives 

### Python — skip the generic tutorials

You don't need another "Python basics" course. You need **Python for the things you'll actually do**. Two paths:

**For ML/scientific Python specifically — the gold standard:**

- **CS231n Python+NumPy tutorial** (Stanford, free): [https://cs231n.github.io/python-numpy-tutorial/](https://cs231n.github.io/python-numpy-tutorial/) — read in one sitting, then _type out every example yourself_. This is the single best resource for going from "knows Python" to "can do ML in Python."
- **NumPy official quickstart**: [https://numpy.org/doc/stable/user/quickstart.html](https://numpy.org/doc/stable/user/quickstart.html) — short, dense, official.

**For general Python depth (so you stop being scared of code):**

- **"Automate the Boring Stuff with Python"** (free online): [https://automatetheboringstuff.com/](https://automatetheboringstuff.com/) — this is the one to actually _do exercises from_, not just read.
- ### ML papers — the realistic beginner reading order

The Quora answer in my search is actually right that throwing papers at beginners often backfires. Papers assume context. So here's the order that works: [Quora](https://www.quora.com/What-are-some-must-read-papers-on-machine-learning-for-a-beginner)

**Step 0 (before any papers): one solid course**

- **Andrew Ng's "Machine Learning Specialization"** on Coursera (audit free) — still the best on-ramp.
- _Or_ **fast.ai's "Practical Deep Learning"** (free, [https://course.fast.ai/](https://course.fast.ai/)) if you prefer top-down/code-first. Given your "I can't read code" problem, **fast.ai is probably better for you** — you'll be reading and modifying real PyTorch from day one.
- **Step 1: foundational papers (read in this order)**

1. **"A Few Useful Things to Know About Machine Learning"** — Pedro Domingos. Not a research paper, more a wisdom dump. Domingos provides a comprehensive overview of essential machine learning concepts and common pitfalls — a great starting point for understanding the broader landscape of machine learning. Read this _first_. ~10 pages. [GeeksforGeeks](https://www.geeksforgeeks.org/machine-learning/10-must-read-machine-learning-research-papers/)
2. **LeNet-5** (LeCun et al., 1998) — birth of CNNs. LeNet-5 was the first architecture capable of learning features automatically, without manual feature engineering. [Medium](https://medium.com/illumination/5-ml-papers-you-need-to-read-for-beginners-9e409292d894)
3. **AlexNet** (Krizhevsky et al., 2012) — the paper that started the deep learning era.
4. **ResNet** (He et al., 2015) — introduced residual connections, allowing the training of extremely deep networks by mitigating the vanishing gradient problem. Still everywhere in modern architectures. [Jobs-in-data](https://jobs-in-data.com/blog/foundational-papers-in-machine-learning-ai)
5. **"Attention Is All You Need"** (Vaswani et al., 2017) — the Transformer. The single most important paper of the last decade. Don't read this until you've coded a small neural net first.
6. **Batch Normalization** (Ioffe & Szegedy, 2015) — short, you'll see it in every codebase.
7. **Step 2: directly relevant to ADAS (read after step 1)**

- **YOLO v1** (Redmon et al., 2016) — "You Only Look Once: Unified, Real-Time Object Detection." Since you mentioned YOLO, read the original first, then jump to whichever modern version your project uses.
- **U-Net** (Ronneberger et al., 2015) — for segmentation, useful for lane/road detection.

**Step 3: only after the above**

- Karpathy's "Let's build GPT" video series — code a transformer from scratch. _Then_ DeepSeek's papers and code will make sense.

**Where to find them:** all the above are free on **arxiv.org**. Just search the title.

**One curated GitHub list to bookmark (not read all of):**

- [https://github.com/hurshd0/must-read-papers-for-ml](https://github.com/hurshd0/must-read-papers-for-ml) — the "must read papers for Data Science, or Machine Learning / Deep Learning Engineer" list. Use as a reference, not a checklist. [GitHub](https://github.com/hurshd0/must-read-papers-for-ml)