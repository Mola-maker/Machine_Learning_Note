# 批归一化：把"方差守恒"从初始化扩展到训练全程
**Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift**
Ioffe & Szegedy (Google) · *ICML 2015* · arXiv:1502.03167

---

## 一句话总结

Xavier 初始化（#5）只保证**初始化那一刻**各层激活方差守恒——训练几步后权重一变，守恒就崩了。BatchNorm 给出彻底的解法：**在网络结构里插入一个归一化层，每个 mini-batch 都把激活强制拉回均值 0、方差 1**，再用两个可学习参数 γ、β 把表达能力还回去。效果近乎魔术——同一个 ImageNet 模型，BN 让它用 **1/14 的训练步数**就达到原精度，还能用大 30 倍的学习率不发散。从 2015 年起，BatchNorm 成为几乎每个卷积网络的标配，也是 ResNet 能堆到 152 层的前提。

> "Batch Normalization allows us to use much higher learning rates and be less careful about initialization. It also acts as a regularizer, in some cases eliminating the need for Dropout."

---

## 1. 历史定位：训练工具箱里承上启下的一环

把 Cluster 2 的脉络连起来看：

- **Xavier（#5，2010）**：诊断出"激活/梯度方差逐层失衡"，给出**初始化时刻**的解。
- **AlexNet（#6，2012）**：靠 ReLU 部分缓解梯度消失，但训练仍要手工调学习率、小心初始化。
- **Dropout（#7，2014）**：从正则化角度抗过拟合。
- **BatchNorm（#8，2015）**：把 Xavier"方差守恒"的思想从"初始化一刻"扩展到"训练全程"——而且不是被动地选好初值，而是**主动地在每一步把激活拉回标准分布**。

BatchNorm 出自 Google 的 Ioffe 和 Szegedy（Szegedy 也是 GoogLeNet/Inception 的作者）。它发表后影响极快——同年的 ResNet（#13）就把 BN 当作标准组件，没有 BN，152 层的网络根本训不动。可以说 BatchNorm 是连接"训练工具箱"和"超深网络时代"的关键一环。

---

## 2. 待解问题：内部协变量偏移

### 2.1 什么是"协变量偏移"

机器学习里，如果训练数据和测试数据的输入分布不一致，就叫"协变量偏移 (covariate shift)"——模型在一个分布上学的，到另一个分布上就不灵。

论文把这个概念**往网络内部延伸**：把深层网络看成一层套一层的子网络。第 $l$ 层的输入，是第 $l-1$ 层的输出。训练时，第 $l-1$ 层的参数一直在变，于是**第 $l$ 层看到的输入分布一直在漂移**。论文给它起名 **内部协变量偏移 (Internal Covariate Shift)**。

### 2.2 为什么它拖慢训练

每一层都得不停地去适应"脚下一直在移动的地面"。具体危害：

- **逼你用小学习率**：上层参数稍微一动，经过多层放大，下层输入分布剧变。要稳住就只能小步走。
- **逼你小心初始化**：初值不好，分布一开始就跑偏。
- **饱和非线性几乎没法用**：以 sigmoid 为例，$|x|$ 一大梯度就趋近 0（#5 讲过）。训练中分布漂移很容易把激活推进饱和区，越深越严重。

论文 Figure 1 给了直观证据：普通网络里某个 sigmoid 单元的输入分布，训练过程中均值和方差**剧烈漂移**；加了 BN 之后，分布**稳如磐石**。

### 2.3 为什么不能简单地"归一化一下"

最朴素的想法：每步训练后，把激活减去均值。论文 Section 2 指出这会**爆炸**。

假设某层加了偏置 $b$，再减去激活均值：$\hat{x} = x - \mathbb{E}[x]$，其中 $x = u + b$。如果梯度下降**忽略了 $\mathbb{E}[x]$ 对 $b$ 的依赖**，它会更新 $b \leftarrow b + \Delta b$。但代入后：

$$u + (b+\Delta b) - \mathbb{E}[u + (b+\Delta b)] = u + b - \mathbb{E}[u+b]$$

——层的输出**完全没变**，损失也没变。于是 $b$ 会无限增长，损失却纹丝不动，最终数值爆炸。

**教训**：归一化必须是网络结构的一部分，让反向传播**知道**它的存在、把梯度正确地传过它。这是 BatchNorm 设计的核心约束。

---

## 3. 核心思想：把归一化变成一个可微的层

### 3.1 BN 变换（论文 Algorithm 1）

对一个 mini-batch $\mathcal{B} = \{x_1,\dots,x_m\}$ 里某个标量激活，BN 做四步：

$$\mu_\mathcal{B} = \frac{1}{m}\sum_{i=1}^m x_i \qquad\text{（mini-batch 均值）}$$
$$\sigma^2_\mathcal{B} = \frac{1}{m}\sum_{i=1}^m (x_i - \mu_\mathcal{B})^2 \qquad\text{（mini-batch 方差）}$$
$$\hat{x}_i = \frac{x_i - \mu_\mathcal{B}}{\sqrt{\sigma^2_\mathcal{B} + \epsilon}} \qquad\text{（归一化：均值 0、方差 1）}$$
$$y_i = \gamma\,\hat{x}_i + \beta \qquad\text{（缩放 + 平移）}$$

前三步把激活拉成标准分布（$\epsilon$ 是防止除零的小常数）。第四步是**点睛之笔**。

### 3.2 γ 和 β：把表达能力还回去

为什么需要第四步？因为**强行归一化会损害网络的表达能力**。比如把 sigmoid 的输入硬拉到均值 0、方差 1，就等于把它锁死在 sigmoid 的近线性区——非线性没了。

解法：引入两个**可学习**参数 γ（缩放）和 β（平移）。关键性质——它们让 BN 层**能够表示恒等变换**：

$$\text{若 } \gamma = \sqrt{\text{Var}[x]},\ \beta = \mathbb{E}[x],\ \text{则 } y_i = x_i$$

也就是说，**如果"不归一化"才是最优的，网络可以通过学习 γ、β 把归一化效果完全抵消**。BN 不是强制约束，而是给网络多一个选择。每个激活只多 2 个参数，代价极小。

### 3.3 为什么用 mini-batch 统计量

理想情况是用整个训练集的均值方差，但那样每步都要扫全集，不可行。BN 的妙处：**直接用当前 mini-batch 的均值方差**。这样统计量本身是 batch 内数据的函数，**可以完全参与反向传播**——梯度能正确地穿过 μ、σ²。论文给出了完整的链式法则反传公式（对 $\hat{x}$、$\sigma^2_\mathcal{B}$、$\mu_\mathcal{B}$、$x_i$、γ、β 各有一项），证明 BN 是一个处处可微的变换。

### 3.4 训练与推理的不对称

这是 BN 最容易出 bug 的地方：

- **训练时**：用当前 mini-batch 的 μ、σ²。
- **推理时**：不能用 batch 统计量（推理希望输出只依赖单个输入、确定性）。改用**整个训练集的总体统计量**——实践中用训练时维护的**滑动平均 (moving average)**。方差用无偏估计 $\text{Var}[x] = \frac{m}{m-1}\mathbb{E}_\mathcal{B}[\sigma^2_\mathcal{B}]$。
- 推理时 μ、σ²、γ、β 全部固定，BN 退化成一个**固定的线性变换**，甚至可以和前面的卷积/全连接层**融合**成一个算子（部署优化常用）。

### 3.5 卷积层的 BN

对卷积层，要遵守"卷积特性"——同一个特征图、不同空间位置应被同样地归一化。所以 BN 对每个**特征图（通道）**算一组 μ、σ²、γ、β，统计量在 **batch 维 + 空间维**上联合求。一个 batch $m$、特征图 $p\times q$，有效样本数是 $m' = m\cdot p\cdot q$。

### 3.6 放在哪里

论文把 BN 放在**非线性之前**：$z = g(\text{BN}(Wu))$。理由：$Wu$ 比 $u$ 更可能是对称、非稀疏、"更高斯"的分布，归一化它更有效。另外既然要减均值，偏置 $b$ 就多余了——它的作用被 β 吸收。

---

## 4. 为什么 BN 让训练快这么多

### 4.1 对学习率尺度免疫

论文 Section 3.3 给了一个漂亮的证明。对任意标量 $a$：

$$\text{BN}(Wu) = \text{BN}((aW)u)$$

——把权重整体放大 $a$ 倍，BN 的输出**完全不变**（因为归一化会把缩放抵消掉）。由此可推出：

$$\frac{\partial\,\text{BN}((aW)u)}{\partial u} = \frac{\partial\,\text{BN}(Wu)}{\partial u}, \qquad \frac{\partial\,\text{BN}((aW)u)}{\partial(aW)} = \frac{1}{a}\cdot\frac{\partial\,\text{BN}(Wu)}{\partial W}$$

两个推论：(1) 权重尺度**不影响**梯度往下传——避免了"大权重放大梯度→爆炸"。(2) 权重越大，它收到的梯度反而越小（$1/a$）——这是一种**自动稳定机制**，权重不会无限膨胀。

正因如此，BN 网络可以用**激进得多的学习率**。论文实验里 BN-x30 用了 30 倍于原始 Inception 的学习率——原始网络用这个学习率会"参数冲到机器无穷大"。

### 4.2 让 Jacobian 奇异值接近 1

论文进一步猜想：BN 让相邻层之间变换的 Jacobian 奇异值接近 1。若 $\hat{z} = F(\hat{x}) \approx J\hat{x}$ 且 $\hat{x},\hat{z}$ 都是单位协方差，则 $I = \text{Cov}[\hat{z}] = J\,\text{Cov}[\hat{x}]\,J^T = JJ^T$，于是 $J$ 的所有奇异值都是 1——梯度反传时大小不变。这正是 Xavier（#5）追求的"方差守恒"，只是 BN 把它做到了**训练全程**。

### 4.3 顺带的正则化效果

因为每个样本的归一化依赖于它**碰巧同 batch 的其他样本**，同一个样本在不同 batch 里会被归一化得略有不同——这引入了**随机噪声**。这个噪声起到了类似 Dropout 的正则化作用。所以论文说"BN 在很多情况下可以省掉 Dropout"。

---

## 5. 代码骨架

```python
import torch, torch.nn as nn

# 手写 BatchNorm1d（论文 Algorithm 1 + 2）
class MyBatchNorm1d(nn.Module):
    def __init__(self, dim, eps=1e-5, momentum=0.1):
        super().__init__()
        self.gamma = nn.Parameter(torch.ones(dim))   # 可学习缩放
        self.beta  = nn.Parameter(torch.zeros(dim))  # 可学习平移
        self.register_buffer('run_mean', torch.zeros(dim))  # 推理用滑动均值
        self.register_buffer('run_var',  torch.ones(dim))   # 推理用滑动方差
        self.eps, self.momentum = eps, momentum

    def forward(self, x):
        if self.training:
            mu  = x.mean(0)                       # mini-batch 均值
            var = x.var(0, unbiased=False)        # mini-batch 方差
            # 更新滑动统计量（推理时用）
            self.run_mean = (1-self.momentum)*self.run_mean + self.momentum*mu
            self.run_var  = (1-self.momentum)*self.run_var  + self.momentum*var
        else:
            mu, var = self.run_mean, self.run_var # 推理：用总体统计量
        x_hat = (x - mu) / torch.sqrt(var + self.eps)   # 归一化
        return self.gamma * x_hat + self.beta            # 缩放 + 平移

# 框架内置：注意 train/eval 模式切换会改变 BN 行为！
net = nn.Sequential(nn.Linear(256,512), nn.BatchNorm1d(512), nn.ReLU())
net.train()   # BN 用 batch 统计量
net.eval()    # BN 用滑动统计量 —— 忘了切会得到错误结果
```

⚠️ 头号实战坑：忘记 `model.eval()`。推理时若还在 `train()` 模式，BN 会用当前 batch 的统计量——结果随 batch 内容乱跳，甚至 batch size=1 时直接崩。

---

## 6. 实验结果与意义

**MNIST sigmoid 网络**：Figure 1 显示 BN 让 sigmoid 单元的输入分布在训练全程保持稳定，测试精度更高、收敛更快。

**ImageNet（Inception 变体）**：

| 模型 | 达到 72.2% 所需步数 | 最高精度 |
|---|---|---|
| Inception（原始） | 31.0 × 10⁶ | 72.2% |
| BN-Baseline（只加 BN） | 13.3 × 10⁶ | 72.7% |
| BN-x5（学习率 ×5） | **2.1 × 10⁶（14 倍加速）** | 73.0% |
| BN-x30（学习率 ×30） | 2.7 × 10⁶ | **74.8%** |
| BN-x5-Sigmoid | — | 69.8% |

亮点：
- **BN-x5 用 1/14 的步数**追平原模型。
- **BN-x5-Sigmoid 达到 69.8%**——一个用 sigmoid 的深网竟然能训起来。对照组（不加 BN 的 Inception + sigmoid）**永远停在 1/1000 的随机水平**。这戏剧性地证明 BN 让"饱和非线性可用"。
- BN-Inception 集成在 ImageNet 上达到 top-5 错误率 **4.9%**，论文称已**超过人类标注者**。

意义分层：

1. **直接结论**：一个可微的归一化层，让训练快一个数量级、对学习率和初始化都不敏感。
2. **解放架构**：BN 让超深网络可训——ResNet（#13）直接把它当标准件。
3. **改变工作流**：调参从"小心翼翼"变成"可以激进"。初始化不再是玄学。
4. **正则化的换代**：BN 自带正则效果，卷积网络里 Dropout 逐渐退场（呼应 #7 的结论）。

---

## 7. 常见误解与澄清

| 误解 | 实情 |
|---|---|
| "BN 之所以有效，是因为它减少了内部协变量偏移" | **这个解释后来被推翻**。Santurkar et al. 2018《How Does Batch Normalization Help Optimization?》用实验证明：即使人为给 BN 后的激活注入协变量偏移，BN 照样有效。BN 的真正作用是**让损失landscape 更平滑**（梯度更 Lipschitz）。"内部协变量偏移"是论文给的*动机故事*，不是被证实的*机理*。 |
| "BN 训练和推理行为一样" | 完全不同。训练用 batch 统计量，推理用滑动平均的总体统计量。忘记 `model.eval()` 是头号 bug。 |
| "BN 对任何 batch size 都行" | 不行。BN 依赖 batch 内统计量，**小 batch（如 2、4）时统计量噪声极大**，性能崩。这是 GroupNorm、LayerNorm 出现的直接动机。 |
| "BN 适用于所有网络" | 不适用于 RNN/Transformer——序列长度可变、batch 统计量不稳定。Transformer 用的是 LayerNorm（#10）。 |
| "γ、β 让 BN 变复杂了，可以去掉" | 不能。没有 γ、β，BN 无法表示恒等变换，会损害表达能力（比如把激活锁进 sigmoid 线性区）。 |
| "BN 就是把数据标准化" | 关键区别在于：BN 是**网络结构的一部分**、参与反向传播。论文 Section 2 证明了"在梯度步之外做归一化"会数值爆炸。 |

---

## 8. 局限与后续填坑

| BatchNorm 的局限 | 后续解药 | 关键论文 |
|---|---|---|
| 依赖 batch size，小 batch 时崩 | GroupNorm（按通道分组，不依赖 batch） | Wu & He 2018 |
| 训练/推理统计量不一致 | LayerNorm（沿特征维归一化，无此问题） | Ba et al. 2016 (#10) |
| 不适用于 RNN / 变长序列 | LayerNorm | Ba et al. 2016 (#10) |
| 不适用于 Transformer | LayerNorm / RMSNorm | Transformer (#24) |
| "内部协变量偏移"机理解释不成立 | 平滑 landscape 的新解释 | Santurkar et al. 2018 |
| 与 Dropout 叠加会互相干扰 | 二选一 | Li et al. 2018 |
| 风格迁移里 BN 抹掉风格信息 | InstanceNorm | Ulyanov et al. 2016 |
| 分布式训练跨设备统计量不一致 | SyncBN | 各框架实现 |

整张表说明：BatchNorm 开创了"归一化层"这一整个家族——LayerNorm、GroupNorm、InstanceNorm、RMSNorm 都是它的变体，针对不同场景调整"在哪个维度上算均值方差"。BN 算 batch+空间维，LN 算特征维，GN 算分组通道维。归一化这件事本身留下了，BN 的具体做法只是其中一种。

---

## 9. 与本路线图后续论文的关联

- **#5 Xavier**：BN 把 Xavier 的"方差守恒"从初始化一刻扩展到训练全程——两篇连读能看清这条思想线。
- **#7 Dropout**：BN 自带正则，部分取代了 Dropout 在卷积网络里的角色。
- **#9 Adam**：BN 管"激活分布稳定"，Adam 管"梯度尺度自适应"——训练工具箱的两大支柱。
- **#10 LayerNorm**：直接为修复 BN 的缺陷而生（下一篇精讲）。
- **#13 ResNet**：BN 是 ResNet 能堆到 152 层的前提，残差连接 + BN 是超深网络的黄金组合。
- **#24 Transformer**：Transformer 用 LayerNorm 而非 BN——理解为什么，要先理解 BN 的局限。

---

## 10. 自检清单（读完应当能回答）

- [ ] 什么是"内部协变量偏移"？它从哪三个方面拖慢训练？
- [ ] 为什么"在梯度步之外做归一化"会导致偏置无限增长、数值爆炸？
- [ ] 写出 BN 变换的四个步骤。γ、β 的作用是什么？为什么说它们"把表达能力还回去"？
- [ ] BN 训练时和推理时分别用什么统计量？为什么不能一样？
- [ ] 用 $\text{BN}(Wu)=\text{BN}((aW)u)$ 证明 BN 对权重尺度免疫，并说明这为什么允许大学习率。
- [ ] 卷积层的 BN 在哪些维度上算均值方差？为什么是这些维度？
- [ ] "内部协变量偏移"这个解释后来被怎样质疑了？BN 起效的真正机理可能是什么？
- [ ] BN 为什么不适用于小 batch 和 Transformer？这分别催生了哪个后续方法？

---

*下一篇精讲 Adam（#9）——训练工具箱的另一根支柱。BN 让激活分布稳定，Adam 让每个参数的更新步长自适应。两者合起来，才有了"深度网络可以放心训练"的现代局面。*
