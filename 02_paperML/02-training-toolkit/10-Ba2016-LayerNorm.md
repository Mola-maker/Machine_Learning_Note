# 层归一化：把 BatchNorm 转置，造出 Transformer 时代的标准件
**Layer Normalization**
Ba, Kiros & Hinton · arXiv:1607.06450 · 2016

---

## 一句话总结

BatchNorm（#8）极好用，但有个死穴：它的统计量算在 **batch 维度**上——batch 小了统计量就不准，序列模型里更是没法用。LayerNorm 的解法简单到优雅：**把 BatchNorm 转置**。不再沿"一批样本"算均值方差，而是沿"一个样本内所有神经元"算。这一转，所有 BN 的麻烦全消失了——它不依赖 batch 大小、训练和推理行为完全一致、能直接用于 RNN。2016 年发表时它还只是个"给 RNN 用的小改进"，但 2017 年 Transformer 把它选作标准归一化层——从此 **LayerNorm 成为整个大模型时代每一个 Transformer 的标配**。BERT、GPT、LLaMA，全靠它。

> "We transpose batch normalization into layer normalization by computing the mean and variance used for normalization from all of the summed inputs to the neurons in a layer on a *single* training case."

---

## 1. 历史定位：一篇"延迟引爆"的论文

LayerNorm 的影响曲线很特别——发表时不温不火，一年后突然引爆：

- **2016 年**：作者 Ba（也是 Adam #9 的作者）、Kiros、Hinton 发表本文。定位很朴素——"BatchNorm 在 RNN 上不好用，我们给个替代品"。当时深度学习的主战场是卷积网络，而 BN 在卷积网络上表现优异，所以 LayerNorm 显得有点小众。
- **2017 年**：Transformer（#24）横空出世，选择 **LayerNorm 作为唯一的归一化层**（因为 Transformer 处理变长序列，BN 根本用不了）。
- **2018 年起**：BERT、GPT 系列全是 Transformer，于是 LayerNorm 随之成为**每一个大语言模型的标准组件**。

所以 LayerNorm 是典型的"睡美人论文"——它的真正价值要等到一个新架构（Transformer）出现才被完全释放。读这篇论文时要带着这个后见之明：你正在读的，是支撑起整个 LLM 时代的那块基石。

它和 BatchNorm 是一对——理解 LayerNorm 的最好方式，就是把它和 BN 逐条对照。

---

## 2. 待解问题：BatchNorm 的三宗罪

BatchNorm 在卷积网络上很成功，但它有三个结构性缺陷（#8 已埋下伏笔，这里展开）：

### 2.1 依赖 batch 大小

BN 的均值、方差是用当前 mini-batch 估计的。batch 大时估计准，batch 小时（比如 2、4）统计量噪声极大，性能崩溃。而很多场景**被迫用小 batch**：
- 超大模型，显存装不下大 batch；
- 高分辨率图像、长序列，单样本就很占显存。

极端情况 batch size = 1 时，BN 的方差直接没有定义——彻底失效。

### 2.2 训练和推理行为不一致

BN 训练时用 batch 统计量，推理时用滑动平均的总体统计量（#8 第 3.4 节）。这个不对称是 bug 的温床（忘记 `model.eval()`），也意味着训练和推理走的不是同一个函数。

### 2.3 没法用于 RNN

这是最致命的。RNN 处理变长序列——不同句子长度不同。BN 要为**每个时间步**单独存一套统计量。如果测试时遇到一个比所有训练序列都长的句子，那些靠后的时间步**根本没有统计量可用**。论文原话：把 BN 用于 RNN"似乎需要为不同时间步用不同的统计量",这在变长序列下无法干净地实现。

**根源**：BN 的统计量算在 batch 维度上，而 batch 维度恰恰是"最不稳定"的那个维度——它的大小可变、它和序列长度纠缠。

---

## 3. 核心思想：把归一化的维度转置

### 3.1 一张图看懂 BN 与 LN 的区别

把一层的激活想象成一个矩阵，行是 batch 里的不同样本，列是不同的神经元（特征）：

```
            神经元1  神经元2  神经元3  ...  神经元H
样本1         a11     a12     a13         a1H
样本2         a21     a22     a23         a2H
样本3         a31     a32     a33         a3H
...
样本m         am1     am2     am3         amH

BatchNorm：  ↑沿"列"归一化↑   ← 每个神经元，跨所有样本算 μ、σ
LayerNorm：  →沿"行"归一化→   ← 每个样本，跨所有神经元算 μ、σ
```

**BatchNorm 归一化每一列，LayerNorm 归一化每一行**。就这一个转置，全部三宗罪烟消云散。

### 3.2 LayerNorm 的公式

对第 $l$ 层、某个训练样本，设这一层有 $H$ 个神经元，$a_i^l$ 是第 $i$ 个神经元的净输入。LayerNorm 算（论文公式 3）：

$$\mu^l = \frac{1}{H}\sum_{i=1}^{H} a_i^l, \qquad \sigma^l = \sqrt{\frac{1}{H}\sum_{i=1}^{H}(a_i^l - \mu^l)^2}$$

注意求和下标是 $i=1\dots H$——**遍历这一层所有神经元**，而不是遍历 batch。关键性质：

- **同一层的所有神经元共享同一个 $\mu$、$\sigma$**；
- **不同训练样本有各自不同的 $\mu$、$\sigma$**。

这正好和 BN 反过来（BN 是同一神经元跨样本共享 μ、σ）。

然后和 BN 一样，归一化后接一对**可学习的增益 $g$ 和偏置 $b$**（论文公式 5）：

$$h_i = f\!\left(\frac{g_i}{\sigma}(a_i - \mu) + b_i\right)$$

$f$ 是激活函数。$g$、$b$ 把表达能力还回去——和 BN 的 γ、β 作用一样。

### 3.3 三宗罪如何被一举消灭

- **不依赖 batch**：$\mu$、$\sigma$ 只用一个样本内的 $H$ 个神经元算，和 batch 里有多少样本完全无关。**batch size = 1 也照常工作**，纯在线学习也行。
- **训练 = 推理**：既然统计量只依赖当前样本自己，训练和推理用的是**完全相同的计算**。没有滑动平均，没有 train/eval 切换的坑。
- **天然适配 RNN**：对 RNN，每个时间步就地算这一步激活的 $\mu$、$\sigma$（论文公式 4）：

$$\mathbf{h}^t = f\!\left[\frac{\mathbf{g}}{\sigma^t}\odot(\mathbf{a}^t - \mu^t) + \mathbf{b}\right], \quad \mathbf{a}^t = W_{hh}\mathbf{h}^{t-1} + W_{xh}\mathbf{x}^t$$

序列多长都行——每一步自给自足。论文指出：标准 RNN 里净输入的幅度会随时间步逐渐增大或缩小，导致梯度爆炸/消失；LayerNorm 让每一步的激活都被重新归一化，**隐藏状态动力学稳定得多**。

---

## 4. 不变性分析：LN 到底"对什么免疫"

论文 Section 5 做了一个漂亮的理论分析——比较 BN、WeightNorm、LayerNorm 对各种变换的不变性（Table 1）：

| | 权重矩阵缩放 | 权重矩阵平移 | 单个权重向量缩放 | 数据集缩放 | 数据集平移 | 单样本缩放 |
|---|---|---|---|---|---|---|
| BatchNorm | ✓ | ✗ | ✓ | ✓ | ✓ | ✗ |
| WeightNorm | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ |
| **LayerNorm** | ✓ | ✓ | ✗ | ✗ | ✗ | **✓** |

两个对 LayerNorm 独有的性质值得记：

- **对权重矩阵的"平移"不变**：给权重矩阵 $W$ 的所有入权重加同一个常向量，LayerNorm 的输出不变。论文公式 (6) 给了证明——平移被均值减法吸收掉了。BN 没有这个性质。
- **对"单个训练样本的整体缩放"不变**（公式 7）：把某个输入样本整体乘一个常数，LayerNorm 的预测不变。这是因为 LN 的 $\mu$、$\sigma$ 只依赖当前样本——样本缩放，$\mu$、$\sigma$ 同步缩放，约掉了。BN 反而没有这个性质（BN 对单样本缩放敏感）。

论文还分析（Section 5.2）：归一化里的 $\sigma$ 起到了"隐式降低学习率"的作用——权重范数变大时，$\sigma$ 也变大，对权重方向的更新被压小，相当于对权重向量做了隐式的"早停"，使学习更稳。

---

## 5. 代码骨架

```python
import torch, torch.nn as nn

# 手写 LayerNorm（论文公式 3 + 5）
class MyLayerNorm(nn.Module):
    def __init__(self, dim, eps=1e-5):
        super().__init__()
        self.g = nn.Parameter(torch.ones(dim))   # 增益（论文的 g）
        self.b = nn.Parameter(torch.zeros(dim))  # 偏置（论文的 b）
        self.eps = eps

    def forward(self, x):                         # x: [..., dim]
        mu  = x.mean(-1, keepdim=True)            # 沿特征维算均值（不是 batch！）
        var = x.var(-1, keepdim=True, unbiased=False)
        x_hat = (x - mu) / torch.sqrt(var + self.eps)
        return self.g * x_hat + self.b
        # 注意：无滑动平均、无 train/eval 区分——训练推理完全一致

# 框架内置：Transformer 里到处都是它
ln = nn.LayerNorm(512)
# 现代 LLM 常用简化变体 RMSNorm —— 去掉减均值，只做 RMS 缩放
# h = g * x / sqrt(mean(x²) + eps)         （LLaMA 等采用）
```

对照 BatchNorm 的代码（#8 第 5 节），最大区别就两处：(1) `mean`/`var` 沿 `-1`（特征维）而非 `0`（batch 维）；(2) **没有** `run_mean`/`run_var` 滑动缓冲，**没有** train/eval 分支。简洁本身就是它的优点。

---

## 6. 实验结果与意义

论文在 6 个任务上测试，**重点放在 RNN**：图文检索、问答（attentive reader）、skip-thought 句向量、DRAW 生成模型、手写序列生成、MNIST。

关键结果：
- **Attentive Reader（Figure 2）**：LN-LSTM 不仅训练更快，最终验证误差也低于普通 LSTM 和 BN-LSTM 变体。论文还指出 LN **对增益初始值不敏感**，而 recurrent BN 对此很敏感（要小心设成 0.1）。
- **手写序列生成（Figure 5）**：小 batch（8）+ 超长序列（约 700 步）——这是 BN 最难搞的场景，LayerNorm 收敛明显更快。
- **DRAW 生成模型**：LN 让收敛快近一倍。
- **置换不变 MNIST（Figure 6）**：在前馈网络上，小 batch（4）时 LayerNorm 明显比 BatchNorm 稳健。

一个诚实的负面结果（Section 6.7）：**在卷积网络上，BatchNorm 仍然胜过 LayerNorm**。原因——LayerNorm 假设"一层里所有神经元贡献相似"，这对全连接层成立，但对卷积层不成立：感受野靠近图像边界的神经元，统计特性和中心的神经元差异很大，强行用同一个 $\mu$、$\sigma$ 归一化不合适。

**意义分层**：

1. **直接结论**：一个不依赖 batch、训练推理一致、适配 RNN 的归一化方法。
2. **分工确立**：从此形成"卷积网络用 BN、序列模型用 LN"的格局。
3. **延迟引爆**：2017 年 Transformer 选它当标准件——这才是它真正的历史地位。今天每个 LLM 里都有几十上百个 LayerNorm。
4. **开启归一化家族**：BN、LN、之后的 GroupNorm、InstanceNorm、RMSNorm——本质都是"在哪个维度上算 μ、σ"的不同选择。LN 确立了"沿特征维"这一支。

---

## 7. 常见误解与澄清

| 误解 | 实情 |
|---|---|
| "LayerNorm 是 BatchNorm 的小改进" | 它在 2016 年看起来是。但 Transformer 选它当标准件后，它成了**整个大模型时代的基石**。影响力远超发表时的预期。 |
| "LayerNorm 在所有场景都优于 BatchNorm" | 不。论文自己承认：**卷积网络上 BN 更好**。LN 的"所有神经元贡献相似"假设在卷积层不成立。分工是：CNN→BN，RNN/Transformer→LN。 |
| "LayerNorm 有训练/推理两套行为" | 没有。这正是它相对 BN 的核心优势之一——LN 训练和推理**完全相同**，无滑动平均、无 `eval()` 坑。 |
| "LayerNorm 沿 batch 维归一化" | 恰恰相反。LN 沿**特征维**（一个样本内所有神经元）归一化，与 BN 正交。这个"转置"是全文的核心。 |
| "现代 Transformer 用的就是原版 LayerNorm" | 多数现代 LLM（LLaMA 等）用的是 **RMSNorm**——LayerNorm 的简化版，去掉减均值那一步，只保留 RMS 缩放，更快且效果相当。 |
| "LN 放在哪里无所谓" | 很有所谓。原始 Transformer 是 **Post-LN**（LN 在残差相加之后），现代 Transformer 多用 **Pre-LN**（LN 在子层之前）——Pre-LN 训练更稳，能去掉学习率 warmup。 |

---

## 8. 局限与后续填坑

| LayerNorm 的局限 | 后续解药 | 关键论文 |
|---|---|---|
| 卷积网络上不如 BN | GroupNorm（折中：分组通道归一化） | Wu & He 2018 |
| 减均值这一步其实可省 | RMSNorm（只做 RMS 缩放） | Zhang & Sennrich 2019 |
| Post-LN 放置导致训练不稳、需 warmup | Pre-LN 放置 | Xiong et al. 2020 |
| 计算上仍有开销 | RMSNorm 更快；融合算子 | LLaMA 等工程实现 |
| 风格迁移场景 | InstanceNorm（单样本单通道归一化） | Ulyanov et al. 2016 |
| 极深 Transformer 仍可能不稳 | DeepNorm、Sandwich-LN 等 | Wang et al. 2022 |

一句话：LayerNorm 确立的"沿特征维归一化"思路是永恒的，RMSNorm 只是把它做得更精简，Pre/Post-LN 之争只是放置位置之争——核心思想没变。

---

## 9. 与本路线图后续论文的关联

- **#8 BatchNorm**：LayerNorm 是它的"转置"——两篇必须对照着读，理解"沿哪个维度归一化"是关键。
- **#9 Adam**：同一作者 Ba。Adam 管步长、LayerNorm 管激活分布，是序列模型训练的两大支柱。
- **#3 LSTM**：LayerNorm 最初就是为稳定 RNN/LSTM 的隐藏状态动力学而设计的。
- **#24 Transformer**：Transformer 选 LayerNorm 作唯一归一化层——这才是 LayerNorm 真正的历史舞台。读 Transformer 时回看本篇，会明白它为什么不能用 BN。
- **#25 BERT / #28 GPT-3 / #34 LLaMA**：所有这些大模型里都有大量 LayerNorm（或 RMSNorm）。

---

## 10. 自检清单（读完应当能回答）

- [ ] BatchNorm 的三个结构性缺陷分别是什么？
- [ ] 用"矩阵的行 vs 列"说清楚 BN 和 LN 归一化维度的区别。
- [ ] 写出 LayerNorm 的 μ、σ 公式，指出求和遍历的是什么。
- [ ] 为什么 LayerNorm 训练和推理行为完全一致，而 BatchNorm 不是？
- [ ] 为什么 BatchNorm 没法干净地用于变长序列的 RNN，而 LayerNorm 可以？
- [ ] LayerNorm 独有的两个不变性是什么？为什么 BN 没有？
- [ ] 为什么卷积网络上 BN 仍然优于 LN？LN 的什么假设在卷积层失效了？
- [ ] RMSNorm 相比原版 LayerNorm 简化掉了哪一步？Pre-LN 和 Post-LN 有什么区别？

---

*Cluster 2（训练工具箱）到此全部读完——AlexNet → Dropout → BatchNorm → Adam → LayerNorm。加上 Cluster 1 的五篇基础，你现在已经备齐了走进现代深度学习的全部地基：会算梯度、能训深网、有正则化、有自适应优化、有归一化。接下来 Cluster 3 进入计算机视觉的黄金时代，从 VGG（#11）开始，看这些工具如何把网络一路推深到 152 层。*
