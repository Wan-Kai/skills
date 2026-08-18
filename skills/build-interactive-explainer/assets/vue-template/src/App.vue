<script setup lang="ts">
import SignalExperiment from './components/SignalExperiment.vue'
import { explainer } from './content'

const signalPath = [
  ['观察', '记录发生了什么'],
  ['基线', '描述随机起伏'],
  ['偏差', '比较结果与基线'],
  ['证据', '判断偏差是否意外'],
] as const
</script>

<template>
  <div class="page-shell">
    <header class="site-header">
      <a href="#main" class="skip-link">跳到正文</a>
      <div class="site-mark">EXPLAINER NOTES</div>
      <div class="site-purpose">机制解释 / 可操作证据</div>
    </header>

    <main id="main" tabindex="-1">
      <section class="hero">
        <div class="hero__copy">
          <p class="eyebrow">{{ explainer.eyebrow }}</p>
          <h1>{{ explainer.title }}</h1>
          <p class="tension">{{ explainer.tension }}</p>
          <p class="thesis">{{ explainer.thesis }}</p>
        </div>
        <aside class="hero-map" aria-label="从观察到证据的路径">
          <p class="hero-map__title">从一次结果走到可信判断</p>
          <ol>
            <li v-for="([title, description], index) in signalPath" :key="title">
              <span class="hero-map__index">{{ String(index + 1).padStart(2, '0') }}</span>
              <div><strong>{{ title }}</strong><span>{{ description }}</span></div>
            </li>
          </ol>
        </aside>
      </section>

      <section class="learning-contract" aria-labelledby="learn-title">
        <div>
          <p class="kicker">阅读目标</p>
          <h2 id="learn-title">读完后，你应该能独立判断</h2>
        </div>
        <ol>
          <li v-for="(question, index) in explainer.learningQuestions" :key="question">
            <span>{{ String(index + 1).padStart(2, '0') }}</span><p>{{ question }}</p>
          </li>
        </ol>
      </section>

      <article class="causal-spine">
        <section v-for="step in explainer.steps" :key="step.id" class="explanation-step">
          <div class="step-heading"><p class="kicker">{{ step.label }}</p><h2>{{ step.title }}</h2></div>
          <div class="step-body">
            <p class="one-idea">{{ step.oneIdea }}</p>
            <p>{{ step.body }}</p>
            <SignalExperiment v-if="step.id === 'accumulation'" />
          </div>
        </section>
      </article>

      <section class="derivation" aria-labelledby="evidence-title">
        <div><p class="kicker">完整推导</p><h2 id="evidence-title">为什么更多观察会让稳定偏差更显眼？</h2></div>
        <div class="derivation__content">
          <p>在 50% 基线下，可以把偏离程度写成：</p>
          <p class="formula">z = (命中数 - 0.5 × 观察数) / √(0.25 × 观察数)</p>
          <p>分子表示实际命中数比随机基线多多少；分母表示这组观察本来会有多大的随机起伏。观察数增加时，稳定偏差按观察数累积，而随机起伏只按观察数的平方根增长，所以偏差会逐渐更显眼。</p>
          <div class="evidence-note"><span class="evidence-badge">教学参数</span><p>本页的 62% 和 z = 2.5 用于展示关系，不代表任何真实产品阈值。</p></div>
        </div>
      </section>

      <section class="boundary">
        <p class="kicker">适用边界</p>
        <h2>这个演示没有证明什么？</h2>
        <p>{{ explainer.boundary }}</p>
      </section>
    </main>

    <footer><p>自包含交互式解释</p><p>离线可用</p><p>请在生成时替换日期</p></footer>
  </div>
</template>
