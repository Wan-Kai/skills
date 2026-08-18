export interface ExplainerStep {
  id: string
  label: string
  title: string
  oneIdea: string
  body: string
}

export const explainer = {
  eyebrow: '交互式解释样例',
  title: '微弱信号如何变成证据？',
  tension: '一次多投中几次，也许只是运气。什么时候我们才有理由说：背后真的存在偏向？',
  thesis: '单次结果不能证明偏向；重复观察会让稳定的小偏差逐渐超过随机波动。',
  learningQuestions: [
    '为什么比例偏高仍可能只是巧合？',
    '样本量增加时，什么发生了变化？',
    '检测结论为什么必须带阈值和不确定性？',
  ],
  steps: [
    {
      id: 'choice',
      label: '区分结果与规律',
      title: '先区分结果和规律',
      oneIdea: '一个结果只告诉你发生了什么，许多结果才可能暴露生成规律。',
      body: '公平硬币也会连续出现正面。判断偏向时，我们比较的不是“有没有多出正面”，而是“多出的程度是否已经很难由随机波动解释”。',
    },
    {
      id: 'accumulation',
      label: '积累稳定偏差',
      title: '让同一种偏差重复出现',
      oneIdea: '偏差不必很大，只要方向稳定，就会随着观察次数积累。',
      body: '下面的实验固定每次命中的倾向，只改变观察次数。先预测短样本和长样本哪个更容易越过证据线，再运行它。',
    },
    {
      id: 'meaning',
      label: '解释证据阈值',
      title: '把“超过阈值”解释准确',
      oneIdea: '超过阈值表示结果与随机模型不太相容，不等于已经证明唯一原因。',
      body: '统计检验回答的是“如果没有偏向，这种结果有多意外”。它不会自动排除数据选择、模型假设错误或其他未观察因素。',
    },
  ] satisfies ExplainerStep[],
  boundary: '这个教学实验假设每次观察彼此独立、基线命中率为 50%。真实问题必须先验证这些假设。',
}
