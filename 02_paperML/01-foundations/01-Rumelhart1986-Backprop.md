# 反向传播：让网络学会"表示"
**Learning representations by back-propagating errors**
Rumelhart, Hinton & Williams · *Nature* 323, 533–536 · 1986-10-09

---

## 一句话总结

这篇 4 页的 Nature Letter 不是"发明"反向传播——Werbos 1974 博士论文、Parker 1985、LeCun 1985 早已独立得到类似公式。它的真正贡献是**第一次清楚地展示：用最简单的链式法则梯度下降，多层网络的隐藏单元会自发学到对任务有意义的"分布式表示"**。从此"深度"不再只是一个想法——它变成一种可训练的对象。

> "Internal 'hidden' units which are not part of the input or output come to represent important features of the task domain, and the regularities in the task are captured by the interactions of these units."

整个深度学习时代的隐喻——"特征是学出来的，不是手工设计的"——就藏在这句话里。

---

## 1. 历史定位：为什么 1986 年这件事才被讲清楚

要理解这篇论文为什么是 landmark，必须把它放回 1969–1986 这 17 年的"AI 寒冬"。

**1958 · Rosenblatt 感知机**：单层线性分类器 + 阈值激活。能学，但只能解决线性可分问题。
**1969 · Minsky & Papert《Perceptrons》**：用 XOR 给感知机判了"死刑"。书的最后一章其实留了门缝——"如果加一层隐藏单元呢？"——但当时**没人知道怎么训练隐藏层**：因为隐藏单元没有"目标值"，无法直接定义误差。

整个 1970s 神经网络几乎死掉。同时期，三个人独立想到了答案：

| 人 | 时间 | 形式 |
|---|---|---|
| Paul Werbos | 1974 | 博士论文，几乎被遗忘 |
| David Parker | 1985 | 私下交流 + MIT 技术报告 |
| Yann LeCun | 1985 | *Proceedings of Cognitiva* 法语论文 |
| **Rumelhart, Hinton, Williams** | **1986** | **Nature，配上"它真的能学到有意义的东西"的实验** |

Rumelhart-Hinton-Williams 不是第一个，但他们做了一件之前几个人没做的事：**用实验证明这个算法不是数学玩具，而是能让网络学会"概念"**。这才让神经网络在 1980s 末迎来第一次复兴。

---

## 2. 待解问题：隐藏单元的"教师信号"从哪来？

回到最朴素的画面：

```
输入 x → [隐藏层 h] → 输出 y
            ↑
        谁来告诉它该输出什么？
```

输出层好办——我们有标签 d，可以算误差 (y - d)²。但隐藏单元 h 既不是输入也不是输出，它**没有标签**。怎么知道 h 应该是什么？

论文里这一句把问题点得很狠：

> "In perceptrons, there are 'feature analysers' between the input and output that are not true hidden units because their input connections are fixed by hand, so their states are completely determined by the input vector: they do not learn representations."

换句话说：**没有学习的"特征"不是真正的特征**。整个 1969 之后的工作（径向基函数、特征工程感知机……）都是在手工设计隐藏层。Rumelhart 等人要做的，是让隐藏层自己"长出来"。

---

## 3. 核心思想：把误差当成"反向流动的水"

技术上，整篇论文就是**多元函数链式法则**的一次精彩应用。但概念上的飞跃是：

> 误差 E 是网络所有权重的函数 E(w)。既然是函数，就能求偏导 ∂E/∂w。求偏导这件事可以**逐层倒着算**——后一层告诉前一层"你该往哪边调"。

直觉类比：你是一个工厂的生产线管理者，最终产品质量不达标（输出层误差）。你想知道每个工序（每个权重）该调整多少。你不需要重新跑无数遍生产线试错，**你只需从最后一道工序倒推：每往前一道，把"质量责任"按贡献比例分配给上一道**。这个"按贡献分配责任"的数学形式就是链式法则。

---

## 4. 算法推导：从前向到反向，6 个方程一气呵成

论文用 9 个公式讲完一切，下面对应着拆解。

### 4.1 前向传播

对每个单元 *j*，其净输入是上一层所有单元 *i* 的加权和：

$$x_j = \sum_i y_i \, w_{ji} \tag{1}$$

激活函数用 sigmoid：

$$y_j = \frac{1}{1 + e^{-x_j}} \tag{2}$$

论文特别强调："任何**有界导数**的输入-输出函数都行；用线性求和 + 非线性激活只是为了简化"。这句话其实预言了未来：tanh / ReLU / GELU 都满足这个抽象。

### 4.2 误差函数

对所有样本 *c* 和所有输出单元 *j*：

$$E = \tfrac{1}{2} \sum_c \sum_j (y_{j,c} - d_{j,c})^2 \tag{3}$$

这是最小平方误差 (MSE)。后来的交叉熵、Hinge loss 不过是替换这一项；**反向传播的骨架不变**。

### 4.3 输出层的"种子"梯度

对输出单元，直接对 (3) 求导（固定某个样本 c）：

$$\partial E / \partial y_j = y_j - d_j \tag{4}$$

非常优雅：误差关于输出的偏导就是**预测减真实**。这里的简洁性几乎是 MSE+sigmoid 组合的福报。

### 4.4 穿过 sigmoid

由链式法则：∂E/∂x_j = ∂E/∂y_j · dy_j/dx_j。把 (2) 求导得 dy_j/dx_j = y_j(1 - y_j)，所以：

$$\partial E / \partial x_j = \partial E / \partial y_j \cdot y_j (1 - y_j) \tag{5}$$

这里就埋下了 1990s 末"梯度消失"的祸根：y_j(1-y_j) 最大值才 0.25，每穿过一层 sigmoid 至少缩水 4 倍。15 年后 ReLU 才把它解开。

### 4.5 权重梯度

权重 w_ji 上的误差敏感度：

$$\partial E / \partial w_{ji} = \partial E / \partial x_j \cdot y_i \tag{6}$$

形式美得离谱——**"上游误差信号 × 下游激活值"**。这一个公式是所有现代深度学习框架自动微分的核心模式。

### 4.6 把误差送回上一层

对上一层单元 *i*，它通过所有连接 *w_ji* 影响误差：

$$\partial E / \partial y_i = \sum_j \partial E / \partial x_j \cdot w_{ji} \tag{7}$$

注意结构：**前向时 w_ji 把 y_i 送给 x_j，反向时 w_ji 把误差从 x_j 送回 y_i**——同一个权重在两个方向上都被复用。这就是为什么实现起来如此对称、如此自然。

### 4.7 权重更新

最朴素的批梯度下降：

$$\Delta w = -\varepsilon \, \partial E / \partial w \tag{8}$$

ε 是学习率。论文还提出**动量法**：

$$\Delta w(t) = -\varepsilon \, \partial E / \partial w(t) + \alpha \, \Delta w(t-1) \tag{9}$$

α 在 0 和 1 之间，控制"惯性"。1986 年这就是 PyTorch 里 `torch.optim.SGD(momentum=0.9)` 的雏形。

### 4.8 一张概念地图

```
前向：x → h → y
                ↓ 比对 d
                
                E
              ↙ ↓ ↘
反向：∂E/∂y_out → ∂E/∂x_out → ∂E/∂y_hidden → ∂E/∂x_hidden
                         ↓                       ↓
                      ∂E/∂w_out             ∂E/∂w_hidden
                         ↓                       ↓
                       更新                    更新
```

无论网络多深，这个流程都是**同一套规则的反复套用**。这就是"可扩展"在算法层面上的根本含义。

---

## 5. 三个实验：从"会算"到"会学概念"

论文的杀手锏不在数学（那只是 4 个公式），而在三个精心选择的实验任务。每一个都回答一个不同的疑问。

### 5.1 实验一：对称性检测——证明它真的能学

输入：6 个二值单元（64 种可能的输入模式）；任务：判断输入向量是否关于中心对称。
网络：6 输入 → 2 隐藏 → 1 输出。
训练：ε=0.1, α=0.9, 初始权重 U(-0.3, 0.3), 跑 1425 次扫描。

为什么这是个聪明的任务？因为**任一单个输入位都不能独立判断对称性**——必须比较成对的位置。如果没有隐藏层，根本无解（Minsky-Papert 已经证过类似的）。

学完后看 Fig 1：两个隐藏单元学到了**关于中心对称的权重**（|w₁|=|w₆|, |w₂|=|w₅|, |w₃|=|w₄|，且符号相反），权重大小比例 1:2:4。这样配置下，对称输入会让两个隐藏单元的净输入都为 0，从而 sigmoid 输出 0.5，加上正偏置，输出单元被激活；任何非对称输入都会让其中一个隐藏单元被强烈抑制，输出关闭。

**关键启发**：网络不只是"拟合"，它**发现了任务的数学结构**。

### 5.2 实验二：家族树——分布式表示的诞生

这是论文的灵魂实验。两个同构的家族树（一个英国家族 + 一个意大利家族），共有 104 个三元组 ⟨person1, relationship, person2⟩，如 ⟨Colin, has-aunt, Charlotte⟩。

网络结构：24 个 person1 输入 + 12 个关系输入 → 各自经一层 6 单元 → 中央 12 单元 → 倒数第二层 6 单元 → 24 个 person2 输出（参见 Fig 3）。

训练：104 个三元组里训练 100 个，测试 4 个。ε=0.005 + α=0.5（前 20 轮）然后 ε=0.01 + α=0.9，加 0.2%/轮的权重衰减（这是 weight decay 的早期出现！），1500 轮。

最震撼的结果在 Fig 4：**6 个表示 person1 的隐藏单元，每一个都自发学到了一个有语义的维度**：

- Unit 1：**国籍**——英国 vs 意大利
- Unit 2：**辈分**——属于家族的哪一代
- Unit 6：**家族分支**——树的左半还是右半

**没有人告诉网络"国籍"或"辈分"这些概念存在**。网络从 104 个三元组里**自发发现了任务的隐藏结构**。

这就是 Hinton 后来反复讲的"distributed representation"（分布式表示）思想的实证起点。一个概念不是由一个神经元负责，而是由**多个神经元上的激活模式**联合编码——这与符号 AI 的"一个变量等于一个概念"形成了根本性的范式对立。

而且：测试集 4 个未见过的三元组**正确泛化**。这是神经网络第一次明确展示"组合泛化"能力。

### 5.3 实验三：循环网络——把"时间"拉进来

Fig 5 展示了一个意思：一个循环网络运行 3 个时步，**展开后等价于一个 3 层前馈网络**，只不过每层共享同一份权重。所以反向传播能直接用——只需要在每层算梯度后，把对应权重的梯度**累加再更新**。

这就是后来被命名为 **BPTT (Backpropagation Through Time)** 的全部思想。LSTM、GRU、Transformer 训练的根本算法都没跳出这张图。

---

## 6. 代码骨架：30 行复现核心训练循环

下面是用纯 NumPy 实现的最小可运行 MLP，专门对照论文公式：

```python
import numpy as np

def sigmoid(x): return 1.0 / (1.0 + np.exp(-x))

class TinyMLP:
    def __init__(self, n_in, n_hid, n_out, seed=0):
        rng = np.random.default_rng(seed)
        # 论文 Fig 1: 初始权重 U(-0.3, 0.3)
        self.W1 = rng.uniform(-0.3, 0.3, (n_in,  n_hid))   # 输入→隐藏
        self.W2 = rng.uniform(-0.3, 0.3, (n_hid, n_out))   # 隐藏→输出
        self.dW1_prev = np.zeros_like(self.W1)             # 动量缓冲
        self.dW2_prev = np.zeros_like(self.W2)

    def forward(self, x):
        self.x = x
        self.h = sigmoid(x @ self.W1)        # eq (1)+(2): 隐藏层激活
        self.y = sigmoid(self.h @ self.W2)   # 输出层激活
        return self.y

    def backward(self, d, eps=0.1, alpha=0.9):
        # eq (4)(5): 输出层 dE/dx_out = (y-d) * y(1-y)
        delta_out = (self.y - d) * self.y * (1 - self.y)
        # eq (6): 输出层权重梯度
        dW2 = self.h.T @ delta_out
        # eq (7)(5): 隐藏层 dE/dx_hid = (delta_out · W2.T) * h(1-h)
        delta_hid = (delta_out @ self.W2.T) * self.h * (1 - self.h)
        # eq (6): 隐藏层权重梯度
        dW1 = self.x.T @ delta_hid
        # eq (9): 带动量的更新
        self.dW2_prev = -eps * dW2 + alpha * self.dW2_prev
        self.dW1_prev = -eps * dW1 + alpha * self.dW1_prev
        self.W2 += self.dW2_prev
        self.W1 += self.dW1_prev
```

把它对照公式编号读，论文的每一行数学都能落到代码上某一行。这是反向传播之所以变成"工程标准"的最深原因——**它写下来就是它**。

---

## 7. 为什么这篇 4 页论文如此重要

1. **算法层面**：反向传播 + 链式法则 = 自动微分的最早形态。今天 PyTorch 的 `autograd`、TensorFlow 的 `tf.GradientTape`，本质上是这套规则的工程化扩张。
2. **表示学习层面**：第一次实证"特征可以学习"。这一观念在 2006 年由 Hinton 自己的 DBN 论文推到深层网络，在 2012 年由 AlexNet 推到大规模视觉，在 2017 年由 Attention Is All You Need 推到大规模语言——但根都在这里。
3. **科学方法论层面**：三个实验从易到难（数学性质 → 概念结构 → 时间动力学），完整覆盖了"反向传播能学什么"的边界。这种实验设计本身是后来深度学习论文的范本。
4. **AI 哲学层面**：分布式表示对符号 AI 的对立。后来"connectionism vs symbolism"的全部争论，根都在这篇论文的 Fig 4 上。

---

## 8. 常见误解与澄清

| 误解 | 实情 |
|---|---|
| "Rumelhart 等人发明了反向传播" | 没有。Werbos 1974 已推导。但 Werbos 用的是控制论术语，没人意识到这就是 NN 学习算法。这篇论文的功劳是**让这个算法被神经网络社区接受**，并第一次展示其能学到 meaningful representation。 |
| "反向传播 = 神经网络学习的最终答案" | 论文最后一段自己就承认："The learning procedure, in its current form, is not a plausible model of learning in brains." 反向传播是工程上的成功，不是神经科学上的胜利。Hebbian、predictive coding、forward-forward 这些"生物合理"算法的研究一直没停。 |
| "梯度下降一定卡在局部最优" | 论文里有句话被后来 30 年的实验反复印证："In practice the network very rarely gets stuck in poor local minima." 高维空间里**鞍点比局部最小值多得多**，加上 SGD 的噪声，"卡死"是罕见事件。这一观察等了 30 年才被 Dauphin et al. 2014、Choromanska et al. 2015 用理论解释。 |
| "Sigmoid 是最佳激活函数" | 论文用 sigmoid 是历史选择。它最大梯度 0.25 是后来"梯度消失"的祸根。ReLU 2010、Swish/GELU 2017–2018 都是为了治这个病。 |
| "一定要批量更新" | 论文里同时讨论了两种方案：每个样本就更新（SGD 雏形）和累积后更新（batch GD）。"两者均可"——80 年代就在讨论 mini-batch 的取舍了。 |

---

## 9. 局限与后续 35 年的填坑

| 局限（1986 论文已暗示或忽略） | 后续解药 | 关键论文 |
|---|---|---|
| Sigmoid 梯度消失 | ReLU 族 + 残差连接 | Nair-Hinton 2010, He et al. 2015 (ResNet) |
| 局部最优担忧 | 高维"鞍点"理论 + SGD 噪声 | Dauphin et al. 2014 |
| 大批 batch size 的扩展 | mini-batch SGD + 动量自适应 | Adam (Kingma 2014) |
| 学习率难调 | 学习率调度 + 自适应方法 | RMSProp, Adam, AdamW |
| 内部协变量偏移 | BatchNorm / LayerNorm | Ioffe 2015, Ba 2016 |
| 隐藏单元的"分布式表示"难以解释 | 探针、可视化、机制可解释性 | Olah, Anthropic interpretability |
| 反向传播不能扩展到非常深的网络 | 残差连接 + 归一化 | ResNet 2015, Transformer 2017 |
| 反向传播生物不合理 | 局部学习、预测编码、前向-前向 | Hinton 2022 Forward-Forward |
| 离散决策无法反向 | Gumbel-Softmax, REINFORCE, RLHF | Maddison 2016; Christiano 2017 |

每一行都是后来一整个研究领域。整张表读完，你大致就有了"深度学习这 30 年到底在做什么"的地图。

---

## 10. 与本路线图后续论文的关联

读完这篇之后，你接下来的阅读路径上每一篇都在和它对话：

- **#5 Glorot 2010 (Xavier)**：解决"权重该怎么初始化"——本文用的 U(-0.3, 0.3) 是经验值，Xavier 给出理论。
- **#6 AlexNet 2012**：把反向传播扩展到 8 层 + GPU + ReLU 的工程胜利。
- **#8 BatchNorm 2015**：本文的 sigmoid 梯度消失问题的现代解药。
- **#9 Adam 2014**：本文 eq (9) 动量的现代后裔。
- **#13 ResNet 2015**：让 152 层的反向传播在工程上仍然可行。
- **#24 Transformer 2017**：每一层的反向传播仍然是这篇论文的链式法则，只是把"层"换成"自注意力块"。

换句话说，**整个深度学习的进步可以读成对这篇论文中某条隐含假设的修正**。

---

## 11. 延伸阅读

- **Rumelhart, Hinton, Williams · 1986 · PDP Chapter 8**：Nature 论文是 4 页的浓缩版，PDP 那本书的对应章节有完整版（~50 页），数学细节、收敛分析、更多实验都在里面。论文 reference 4 就是这章。
- **Werbos 1974 PhD thesis**：反向传播的"史前"出处。
- **LeCun 1985 (Cognitiva)**：法语原文，第一次在神经网络背景下推导出等价算法。
- **Goodfellow, Bengio, Courville · 2016 · *Deep Learning* · Chapter 6.5**：现代教科书对反向传播的形式化。
- **Andrej Karpathy · "Yes you should understand backprop" (Medium, 2016)**：现代 ML 工程师视角的"反向传播为什么仍然不能当黑盒"。

---

## 12. 自检清单（读完应当能回答）

- [ ] 为什么 1969 之后神经网络停滞了 17 年？这篇论文解决了什么本质难题？
- [ ] 写出公式 (4)–(7)，并解释每一项的几何含义。
- [ ] 不查代码，用 NumPy 30 行内实现一个能解 XOR 的 MLP。
- [ ] 解释家族树实验的 Fig 4 为什么是"分布式表示"诞生的标志。
- [ ] 反向传播的哪些假设在后来被打破或替换？至少举 3 个。
- [ ] 论文为什么说反向传播"在脑中不是生物合理的"？如果你来设计一个生物合理的替代，会从哪里入手？

---

*下一篇推荐继续读 LeNet（#2）——把这套反向传播放到二维卷积上，看看怎么一举把"图像识别"从科幻变成工程。*
