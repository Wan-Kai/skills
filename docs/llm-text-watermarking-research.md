# 大模型文本水印：技术核验与交互式科普方法研究

> 研究日期：2026-08-14  
> 研究对象：[How AI text watermarking works](https://declaude.org/watermarking/)  
> 目标：追溯文章背后的原始论文、作者代码和官方资料，核验机制与证据边界，并提炼可复用的通俗解释和交互可视化方法。

## 结论先行

1. 这篇文章最值得复用的不是某个动画，而是一条完整的认知路径：**先让读者看见模型的随机选择，再展示密钥如何轻推选择，随后让读者亲手统计信号，最后通过编辑实验理解失效边界**。每一步只引入一个新概念，并始终复用同一段文本。
2. 文章主要用 Kirchenbauer 等人的 KGW 绿表/红表方案作为教学骨架。它适合解释“水印藏在 token 选择概率里”，但不能代表所有文本水印；SynthID-Text、Aaronson–Kirchner、context-free Unigram 和语义水印的数学结构及鲁棒性都不同。
3. 文本水印是**带密钥的统计归因信号**，不是根据文风猜测的通用“AI 检测器”。检测结果通常只能说明内容可能经过某个带水印生成器处理，不能证明思想、原文或作者身份。
4. 水印检测的核心矛盾是质量、可检测性、长度、鲁棒性和安全性之间的权衡。短文本、代码、固定引文、模板和事实性回答生成自由度低，往往更难嵌入和检测；彻底重写、翻译和跨来源混合会显著削弱多数 token 级水印。
5. 页面明确把动画参数称为教学参数；其“KGW/EXP AUC 从 0.99 降到约 0.5”“仅 0.5% 窗口存活”等数字是 declaude 自己的 known-key 实验，不是公开论文结果，也不能外推到 Claude。Anthropic 截至本次研究只公开了产品覆盖范围和限制，未公开 Claude 文本水印算法或检测器细节。[declaude 原文](https://declaude.org/watermarking/) · [Anthropic 官方说明](https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content)

## 一、技术机制：从生成到检测

### 1. KGW：给“绿色候选”增加一点胜率

Kirchenbauer 等人在 ICML 2023 提出的经典方案可以拆成四步：

1. 语言模型先根据上下文给出下一 token 的原始 logits。
2. 用前文 token、哈希函数和密钥伪随机地把词表划成绿色集合与红色集合；绿色比例记为 \(\gamma\)。
3. 给绿色 token 的 logit 加上偏置 \(\delta\)，再从修改后的分布采样。红色 token 没有被禁止，只是相对更不容易被选中。
4. 检测端用相同密钥重放每一步的划分，统计实际落入绿色集合的 token 数。

在无水印假设下，绿色命中数近似服从参数为 \(T,\gamma\) 的二项分布，常用统计量为：

\[
z=\frac{|s|_G-\gamma T}{\sqrt{T\gamma(1-\gamma)}}
\]

其中 \(T\) 是参与检测的 token 数，\(|s|_G\) 是绿色 token 数。原论文用 \(z>4\) 举例，对应单侧假阳性率约 \(3\times10^{-5}\)。这正是页面“错误密钥像抛硬币，正确密钥绿色偏多”的数学来源。[ICML 2023 论文页](https://proceedings.mlr.press/v202/kirchenbauer23a.html) · [论文 PDF](https://proceedings.mlr.press/v202/kirchenbauer23a/kirchenbauer23a.pdf) · [作者代码](https://github.com/jwkirchenbauer/lm-watermarking)

必须保留的技术边界：

- 文章演示使用 50/50 绿红划分，因此把零假设画成“抛硬币”；KGW 常见配置是 \(\gamma=0.25,\delta=2\)，零假设并不一定是 50%。
- 检测按模型 tokenizer 的 token 计数，不是按页面中可见的单词计数。
- 信号强度取决于生成分布的熵。高熵位置有多个合理候选，轻微偏置容易生效；低熵位置几乎只有一个合理续写，偏置要么不生效，要么损害质量。原论文和后续实验都观察到代码、模板化内容等场景水印更弱。[ICLR 2024 论文](https://proceedings.iclr.cc/paper_files/paper/2024/file/d78e9e4316e1714fbb0f20be66f8044c-Paper-Conference.pdf)
- 重复 n-gram 会破坏近似独立假设并可能虚增统计量。官方实现建议检测时忽略重复 n-gram；示例密钥也必须在真实部署中替换。[KGW 官方实现说明](https://github.com/jwkirchenbauer/lm-watermarking#how-to-watermark---a-short-guide-on-watermark-hyperparameters)

### 2. 为什么短文本难：微弱偏差要靠样本量积累

统计直觉不是“看到几个绿色词就确定”，而是观察到的偏差能否显著超过随机波动。若每 token 的平均信号强度近似不变，\(z\) 大致随 \(\sqrt{T}\) 增长；文本长度扩大四倍，统计证据约扩大两倍。

KGW 原论文在特定 OPT 模型、高熵文本和参数设置下报告过很短片段即可检出，也给出 \(z>4\) 的演示；这些是特定实验结果，不是任何模型、语言和文本类型都成立的通用长度下限。[ICML 2023 论文 PDF](https://proceedings.mlr.press/v202/kirchenbauer23a/kirchenbauer23a.pdf)

因此，面向普通读者更稳妥的说法是：

> 每一次 token 选择只留下极弱证据；足够多次选择都朝同一密钥指定的方向略微偏斜后，整体才不像巧合。

### 3. SynthID-Text：不只是“绿表加偏置”

Google DeepMind 的 SynthID-Text 也把信号嵌入采样过程，但其 non-distortionary 版本不是简单给一组 token 加固定 logit。论文描述的 tournament sampling 会从原模型分布抽取 \(2^m\) 个候选，并用由密钥和上下文生成的多层 g-value 进行淘汰赛选择；在对密钥随机性的平均意义下，它保持原模型预期的边缘 token 分布。另有 distortionary 版本，可用一定分布偏移换取更强检测能力。[Nature 论文](https://www.nature.com/articles/s41586-024-08025-4) · [开放全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC11499265/) · [Google DeepMind 代码](https://github.com/google-deepmind/synthid-text)

官方实现提供 Mean、Weighted Mean 和 Bayesian 等检测器。Bayesian 检测器要针对每套密钥训练，训练数据需独立且代表生产分布，检测阈值还要按目标假阳性率、假阴性率和文本长度校准。[Google DeepMind 代码](https://github.com/google-deepmind/synthid-text) · [Google AI 官方文档](https://ai.google.dev/responsible/docs/safeguards/synthid)

Nature 论文在接近 2,000 万条 Gemini 响应的线上实验中，报告有无水印组的点赞率相差 0.01%、点踩率相差 0.02%。这支持“该生产实验没有观察到用户感知的质量下降”，不等于所有任务、模型、语言和短文本都绝对无影响。[Nature 论文](https://www.nature.com/articles/s41586-024-08025-4)

### 4. Aaronson–Kirchner：让密钥决定随机数

Aaronson–Kirchner 方案不先划分绿表，而是让密钥 PRF 根据上下文生成采样随机性，使输出 token 与密钥之间留下可检测相关性，同时保持 token 的边缘分布。它主要来自 Scott Aaronson 的演讲、博客和 Hendrik Kirchner 的原型，不应写成正式同行评议论文，也没有部署到当时的 OpenAI 产品。Aaronson 当时明确承认，让另一个足够强的模型完整改写输出可以击败该方法。[作者博客](https://scottaaronson.blog/?p=6823) · [原始讲稿](https://www.scottaaronson.com/talks/watermark.ppt) · [作者后续说明](https://scottaaronson.blog/?p=9333)

### 5. 不依赖邻接上下文的 Unigram 水印

Unigram-Watermark 为每个 token 使用稳定的颜色，不随前文重新划分。它对插入、删除、替换和打乱更耐受：编辑一个位置不会连带改变后续窗口的颜色。但长期复用同一 token 的颜色也更容易被攻击者从大量输出中学习或逆向。这说明“更抗编辑”和“更难窃取”经常是相互冲突的目标。[ICLR 2024 论文](https://openreview.net/pdf?id=Bwz0fy9Hc9) · [作者代码](https://github.com/XuandongZhao/Unigram-Watermark)

### 6. 语义空间水印：把标记单位从 token 提升到句子

SemStamp 使用句向量和局部敏感哈希把语义空间划区，再通过 rejection sampling 生成落入有效区域的句子；检测端检查相邻句子的哈希区域序列并进行统计检验。它比表面 token 水印更能承受同义改写，但生成成本更高，而且攻击者也可以针对“保持语义、改变区域”进行优化。[NAACL 2024 论文](https://aclanthology.org/2024.naacl-long.226/) · [作者代码](https://github.com/abehou/SemStamp)

## 二、鲁棒性：哪些修改只是稀释，哪些会真正破坏

### 1. 轻度编辑和局部复制

KGW 的绿色集合由短上下文决定。以 \(h=1\) 的 LeftHash 为例，修改一个 token 会影响该 token 的命中状态和下一位置的绿色集合；更大的上下文宽度会让影响扩展到更长窗口。未改动的原始 n-gram 仍贡献相关信号，新写内容大体贡献随机噪声。

ICLR 2024 的后续研究显示：

- 未攻击文本在其实验设置中 AUC 高于 0.999。
- GPT-3.5 和 Dipper 全文改写后，约 200 token 时 AUC 仍高于 0.85，约 600 token 时高于 0.9。
- 强人工改写在假阳性率设为 \(10^{-5}\) 时，平均观察到约 800 token 后重新检出。
- Copy-paste 场景高度依赖检测器。将 150 个带水印 token 插入 600-token 人类文本时，窗口式 WinMax AUC 高于 0.95；普通全局统计在仅 25% 内容带水印时，200 token 的 AUC 低于 0.7，600 token 也低于 0.85。

这些结果支持“轻度或一次改写常常只是稀释信号，长度足够时统计功效会回来”，不能推导出“任何彻底重写都无法去除水印”。[ICLR 2024 论文](https://proceedings.iclr.cc/paper_files/paper/2024/file/d78e9e4316e1714fbb0f20be66f8044c-Paper-Conference.pdf) · [作者代码](https://github.com/jwkirchenbauer/lm-watermarking/tree/main/watermark_reliability_release)

### 2. 彻底重写、翻译和递归释义

Google 官方明确说明 SynthID 对裁剪、少量改词和轻度释义有一定鲁棒性，但彻底重写或翻译会显著降低检测置信度；事实性回答的生成自由度较低，水印也更弱。[Google AI 官方文档](https://ai.google.dev/responsible/docs/safeguards/synthid)

Sadasivan 等人在约 300-token 文本上使用递归释义，发现水印、神经分类器、零样本检测器和检索式检测都可被显著削弱，而文本质量只轻微下降；他们还展示了通过黑盒输出推断隐藏签名后伪造水印的风险。[论文](https://arxiv.org/abs/2303.11156) · [作者代码](https://github.com/vinusankars/Reliability-of-AI-text-detectors)

ACL Findings 2026 的 TSAPA 进一步用遗传算法和伪对数似然引导定向变异，在 Qwen3 1.7B/8B/32B 上攻击多种水印，报告总体攻击成功率超过 90%；在 Qwen3-32B、EXP、文章续写设置中接近 100% 攻击成功率，同时 BERTScore 约为 0.73–0.77。该结果说明更强的自适应攻击可以主动搜索“质量尚可但检测失败”的文本，而不只是随机替换。[ACL 2026 论文](https://aclanthology.org/2026.findings-acl.459.pdf)

### 3. 不能忽略的另一面：伪造与密钥窃取

鲁棒性不只包括“攻击者能否删掉真水印”，还包括：

- 能否把人类文本改造成误报为某供应商输出；
- 能否从大量查询中推断 token 偏好或密钥相关结构；
- 检测 API 是否泄露过多分数，帮助攻击者迭代规避；
- 公开检测器、半公开 API 和私有检测器之间如何权衡透明度与攻击面。

因此 declaude 的“只有密钥持有者能检查”只适用于私有方案。Google 官方明确列出 fully-private、semi-private API 和 public 三种验证模式；KGW 原论文也讨论了公开与私有检测模式。[Google AI 官方文档](https://ai.google.dev/responsible/docs/safeguards/synthid) · [ICML 2023 论文 PDF](https://proceedings.mlr.press/v202/kirchenbauer23a/kirchenbauer23a.pdf)

## 三、Claude 当前公开信息的准确边界

Anthropic 官方说明，截至本次研究：

- 2026 年 8 月 2 日及之后在欧盟发布的新模型会在发布时支持机器可读标记，已有模型处于迁移过程；支持的 Claude 文本输出会嵌入水印，支持的文件类型会附带签名溯源元数据。
- 文本标记位于文本本身，因此复制粘贴后仍会随文本传播，并可能承受部分编辑；文件标记遵循 C2PA 开放标准。
- 命中只表示内容**可能被 Claude 处理过**。校对、翻译、摘要、文件转换等处理也可能让原本人类创作的内容带上 Claude 标记。
- 未命中不能证明内容不是 AI 生成：旧模型、重度编辑、释义、翻译、混合其他文本、片段过短、文件重保存或截屏导致元数据丢失等都会造成漏检。
- Anthropic 尚未公开文本水印算法、密钥结构、统计量、阈值、检测器或真实鲁棒性数据，只说检测技术文档将后续发布。

因此，目前不能把 KGW、SynthID 或 declaude 的自测结果当成 Claude 生产水印的实现细节或性能指标。[Anthropic 官方说明](https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content)

## 四、declaude 的通俗解释结构

### 1. 用“反常识问题”建立学习动机

文章从“纯文本没有像素，也没有能在复制粘贴后保留的元数据，水印还能藏在哪里？”切入。它没有先给定义，而是先制造一个读者能理解的矛盾，再给出全文的核心答案：**水印不藏在字符里，而藏在词语选择之间**。[declaude 原文](https://declaude.org/watermarking/)

可复用公式：

> 看似不可能的现象 → 排除读者最自然的错误答案 → 给出一个能贯穿全文的新视角。

### 2. 五步链路，每步只承诺“一个想法”

每节标题下都有一句 “The one idea in this step”，形成稳定节奏：

1. 写作是许多微小选择；
2. 密钥轻推这些选择；
3. 持有密钥的人可以统计；
4. 编辑会破坏连续证据；
5. 实际含义是概率性的“被处理过”，不是作者身份。

这条顺序对应真实系统的因果链：**生成分布 → 嵌入 → 检测 → 攻击/编辑 → 产品解释**。读者不需要提前理解哈希、PRF、logit 或假设检验。[declaude 原文](https://declaude.org/watermarking/)

### 3. 同一实例贯穿，而不是每节换例子

前两节复用 “The results of the study were quite ___” 和四个候选词；第三、四节复用同一段 harbour 文本。这样每次视觉变化只对应一个新变量：概率、颜色、密钥、统计、编辑深度。读者无需同时理解新例子和新概念。

### 4. 先给直觉，再逐层补充技术分叉

主线始终使用“加权骰子—染色—数绿词—抛硬币”的低门槛比喻；SynthID 的 tournament、Aaronson 的密钥随机数、残余证据公式等被放在括号或文末专家说明中。这是一种有效的渐进披露：主线可独立完成理解，专业读者仍能继续下钻。

风险是：支线如果只写一句，容易让读者误以为不同方案只是同一算法的小变体。未来 Skill 应在主线后增加一个简短的“哪些地方只是共同直觉，哪些地方算法不同”的对照表。

### 5. 用对照实验替代抽象定义

页面不只告诉读者“错误密钥不会命中”，而是提供“正确密钥”和“错误密钥”两个按钮；本次实页检查中，同一 55 词教学样本的动画终态分别显示 38/55（69%）和 28/55（51%）绿色。数字是预设的教学数据，不是现场调用真实检测器，但对照让“相关信号”和“随机噪声”的差别立刻可见。[declaude 原文](https://declaude.org/watermarking/)

### 6. 主动写出认知边界

文章做了几件值得保留的事：明确 production mark 会比演示轻；明确动画使用 illustrative parameters；明确真实检测按 token 而非 word；明确 Anthropic 方案未公开；把“processed by”与“written by”区分开。

不足之处是多数论文只在文末列出题名，没有逐条可点击链接，也没有把论文结果、作者自测和教学参数在视觉上分成三类证据。研究型 Skill 应强制每个关键结论就近标注来源类型。

## 五、交互可视化模式拆解

本节来自 2026-08-14 对页面实际交互和内联页面源码的检查。[declaude 页面](https://declaude.org/watermarking/)

### 模式 A：概率分布的可操作抽样器

- 横条显示四个候选词的 40/30/20/10 权重。
- “roll once”用扫过候选、减速、落点的动画模拟抽样；“roll ×20”快速累积 tally dots。
- 单次抽样建立“每个答案都合理”的直觉，多次抽样让频率逐渐接近概率。

适用：解释采样、随机变量、蒙特卡洛、模型不确定性。  
关键原则：必须同时提供“慢速看过程”和“批量看分布”两种时间尺度。

### 模式 B：参数干预前后的同屏比较

- “apply the secret key”把条形宽度从原始概率切换到教学用的 53/14/28/5。
- 虚线轮廓保留旧概率，实体条显示新概率；候选同时显示 green/red 标签。
- 用户仍可继续投骰子，观察红词仍会偶尔胜出。

适用：解释正则化、重加权、干预、偏置、校准。  
关键原则：保留 before ghost，不要只展示 after；否则读者看不到“轻推了多少”。

### 模式 C：Small multiples 展示上下文依赖

页面把同一组候选放在六个不同前缀后，以小圆点阵列显示颜色随上下文重新洗牌。它用并列小图回答一个很容易误解的问题：“green 是单词的固定属性吗？”

适用：解释上下文哈希、条件概率、同一对象在不同状态下的分类。  
关键原则：保持候选不变，只改变上下文；让读者能做横向比较。

### 模式 D：逐 token 扫描的统计检测器

- 点击正确/错误密钥后，文本 chips 逐个变成绿色实心下划线或红色虚线轮廓。
- 计数器和比例条同步累积，阈值标记随文本长度变化。
- “same mark, ×4 the text”扩展样本量，展示相同微弱偏差如何因长度而越过阈值。
- 页面为 `aria-live` 提供终态文字，并尊重 `prefers-reduced-motion`。

适用：解释序贯统计、置信度、样本量、阈值。  
关键原则：动画必须最终落到可读的数值、阈值和结论，不能让运动本身替代解释。

### 模式 E：连续滑杆加语义预设

- 编辑深度滑杆只有五个离散状态，并配有 “fix typos / light touch / tighten / heavy edit / full rewrite” 语义标签。
- 相同文本实时变形，仍处于原始 5-token 窗口中的词被高亮；同时更新 surviving windows 百分比和结论。
- 读者既能拖动探索，也能直接点预设。

适用：解释扰动强度、鲁棒性曲线、消融实验。  
关键原则：滑杆刻度要用领域语言命名，数值只是辅助；变化、指标和结论必须同步。

### 模式 F：一致的视觉语法

- 绿色实心/下划线始终表示命中，红色虚线始终表示未命中，橙色只用于步骤编号和编辑高亮。
- 色彩之外还有边框、填充、下划线等冗余编码，降低仅靠颜色传达信息的风险。
- 控件都有清晰 focus 样式，页面对 reduced motion 关闭 transition/animation。

可复用原则：先定义一套跨图一致的视觉词汇，再做单个动画；同一语义不能在不同图里换颜色。

## 六、页面中需要纠偏或降级为“教学近似”的内容

| 页面表述 | 核验结论 | Skill 中应如何表达 |
|---|---|---|
| “green 应约占一半，像抛硬币” | 只对应页面的 \(\gamma=0.5\) 教学设置；常见 KGW 配置可为 \(\gamma=0.25\) | 先讲二项分布，再把硬币明确标成 50/50 特例 |
| “编辑只在连续窗口断裂处擦除水印” | 对依赖邻接上下文的 token 水印是有用近似；新文本仍进入统计并贡献噪声，不同 \(h\) 影响范围不同 | 标注“以 context-dependent token watermark 为例” |
| “只有密钥持有者能检查” | 私有检测是常见部署方式，但也可提供 API 或公开检测器 | 改为“检测权限取决于方案与部署模式” |
| “1,500 词时约 55% 绿色即可标记” | 页面用 \(z=4,\gamma=0.5\) 的教学参数投影，真实系统按 token、阈值和校准数据计算 | 数字旁固定显示“illustrative” |
| “0.5% 窗口、AUC 0.99→0.5” | declaude 自测，不是论文结果；没有公开实验配置和复现实验仓库 | 单列为“站点作者自测，待复现” |
| “完全重写即可去除这类标记” | 对许多 context-dependent token 水印成立，但 Unigram 和语义水印可能保留更多信号；自适应攻击与防御仍在演进 | 按水印家族分别说明，不给普遍保证 |
| Claude 使用上述机制 | Anthropic 未公开具体机制 | 只能讲官方覆盖范围和局限，不能反推算法 |

## 七、可沉淀为论文/概念解读 Skill 的方法

### 1. 建议的固定工作流

1. **定义学习目标**：读者读完后要能回答哪三个问题，而不是“总结全文”。
2. **追溯证据**：优先原论文、作者代码、官方文档；二手文章只作为讲解对象，不作为最终事实来源。
3. **抽取一条因果主线**：选择 3–6 个不可再少的步骤，每步只增加一个概念。
4. **选择贯穿实例**：尽量让同一个输入、句子或数据在各步骤持续演化。
5. **为每个抽象概念配一个动作**：概率→抽样，干预→开关，阈值→累计，鲁棒性→滑杆，对比→并列按钮。
6. **把数字分层**：论文报告、官方产品事实、作者自测、教学参数必须使用不同标签。
7. **补“哪里不成立”**：至少覆盖假设、适用域、失败模式、攻击面和未知项。
8. **回到现实决策**：结尾回答“能说明什么、不能说明什么、什么时候值得用”。

### 2. 建议的输出结构

```text
一个反常识问题
→ 一句话核心答案
→ 3–6 步因果链（每步：one idea + 解释 + 微交互）
→ 方法家族对照
→ 证据与实验数字
→ 失败模式 / 未知项
→ 实际判断清单
→ 可点击的一手来源
```

### 3. 证据标签建议

- **[论文结论]**：来自同行评议论文或预印本，附模型、数据集、样本量和指标。
- **[官方事实]**：来自产品或组织官方文档，只描述其真正公开的范围。
- **[代码事实]**：来自作者/官方实现，包括默认参数、接口和实现限制。
- **[作者自测]**：非论文实验，必须说明是否有代码、数据和复现条件。
- **[教学参数]**：只服务于可视化，不用于推断生产性能。
- **[解释性推断]**：由多份来源归纳，明确写成推断而非来源原话。

### 4. 交互是否值得做的判定

只有当用户操作能改变一个关键变量，并让结果关系比静态图更清楚时才做交互。优先级建议：

1. 对照开关：before / after；
2. 批量抽样：single / many；
3. 参数滑杆：弱 / 强及语义预设；
4. 错误路径：正确密钥 / 错误密钥；
5. 样本量控制：短文本 / 长文本；
6. 进阶公式：默认折叠，按需展开。

不要把纯装饰性动效当作解释。任何动画都应有即时文本反馈、可访问名称、键盘路径、reduced-motion 降级和稳定终态。

## 八、主要一手资料索引

### 生成与检测

- Kirchenbauer et al., *A Watermark for Large Language Models*: [PMLR](https://proceedings.mlr.press/v202/kirchenbauer23a.html) · [PDF](https://proceedings.mlr.press/v202/kirchenbauer23a/kirchenbauer23a.pdf) · [代码](https://github.com/jwkirchenbauer/lm-watermarking)
- Kirchenbauer et al., *On the Reliability of Watermarks for Large Language Models*: [ICLR PDF](https://proceedings.iclr.cc/paper_files/paper/2024/file/d78e9e4316e1714fbb0f20be66f8044c-Paper-Conference.pdf) · [代码](https://github.com/jwkirchenbauer/lm-watermarking/tree/main/watermark_reliability_release)
- Dathathri et al., *Scalable watermarking for identifying LLM outputs*: [Nature](https://www.nature.com/articles/s41586-024-08025-4) · [开放全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC11499265/) · [代码](https://github.com/google-deepmind/synthid-text) · [Google 官方文档](https://ai.google.dev/responsible/docs/safeguards/synthid)
- Aaronson & Kirchner: [作者博客](https://scottaaronson.blog/?p=6823) · [讲稿](https://www.scottaaronson.com/talks/watermark.ppt) · [未部署说明](https://scottaaronson.blog/?p=9333)
- Zhao et al., *Unigram-Watermark*: [OpenReview PDF](https://openreview.net/pdf?id=Bwz0fy9Hc9) · [代码](https://github.com/XuandongZhao/Unigram-Watermark)
- Hou et al., *SemStamp*: [ACL Anthology](https://aclanthology.org/2024.naacl-long.226/) · [代码](https://github.com/abehou/SemStamp)

### 攻击与局限

- Sadasivan et al., *Can AI-Generated Text be Reliably Detected?*: [arXiv](https://arxiv.org/abs/2303.11156) · [代码](https://github.com/vinusankars/Reliability-of-AI-text-detectors)
- Zhao et al., *The Mark Fades: Adaptive Evolutionary Paraphrase-based Attack*: [ACL 2026 PDF](https://aclanthology.org/2026.findings-acl.459.pdf)

### 产品公开信息与讲解对象

- [Anthropic：How Claude marks AI-generated content](https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content)
- [declaude：How AI text watermarking works](https://declaude.org/watermarking/)
- [MarkLLM 开源评估工具包](https://github.com/THU-BPM/MarkLLM)

