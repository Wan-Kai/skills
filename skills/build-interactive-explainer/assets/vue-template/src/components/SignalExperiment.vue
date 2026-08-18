<script setup lang="ts">
import { computed, onBeforeUnmount, ref } from 'vue'

type SignalMode = 'signal' | 'baseline'

const sampleSize = ref(20)
const mode = ref<SignalMode>('signal')
const visibleCount = ref(0)
const isRunning = ref(false)
let timer: number | undefined

const targetRate = computed(() => (mode.value === 'signal' ? 0.62 : 0.5))

/**
 * 生成可复现的命中序列，使不同样本量之间可以公平比较。
 * length 与 probability 流入线性同余序列，布尔结果再由 visibleSequence 驱动计数、仪表和结论。
 * 若同一模式重跑得到不同结果，应检查种子或算法是否被改动；若比例偏差过大，应先检查教学参数而不是增加随机性。
 * 序列只服务于教学演示，不能替换成 Math.random；固定种子是保证样本量对照有效的前提。
 */
function createDeterministicSequence(length: number, probability: number): boolean[] {
  let seed = mode.value === 'signal' ? 20260815 : 8152026
  return Array.from({ length }, () => {
    seed = (seed * 1664525 + 1013904223) >>> 0
    return seed / 2 ** 32 < probability
  })
}

const sequence = computed(() => createDeterministicSequence(sampleSize.value, targetRate.value))
const visibleSequence = computed(() => sequence.value.slice(0, visibleCount.value))
const hits = computed(() => visibleSequence.value.filter(Boolean).length)
const rate = computed(() => (visibleCount.value ? hits.value / visibleCount.value : 0))
const zScore = computed(() => {
  if (!visibleCount.value) return 0
  return (hits.value - visibleCount.value * 0.5) / Math.sqrt(visibleCount.value * 0.25)
})
const isFlagged = computed(() => zScore.value >= 2.5)
const resultText = computed(() => {
  if (!visibleCount.value) return '等待运行。先预测：观察次数增加后，同样的轻微偏向会更容易还是更难被发现？'
  if (visibleCount.value < sampleSize.value) return `正在观察：${hits.value} 次命中，共 ${visibleCount.value} 次。`
  if (isFlagged.value) return `越过证据线：${hits.value}/${sampleSize.value} 次命中，偏差已经较难用随机波动解释。`
  return `尚未越过证据线：${hits.value}/${sampleSize.value} 次命中，这个结果仍可能由随机波动产生。`
})

function prefersReducedMotion(): boolean {
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches
}

/**
 * 逐步暴露观察结果，让读者看到证据如何累积；减少动效时直接抵达同一终态。
 * sampleSize 决定每次推进量，visibleCount 再驱动序列切片、统计量、仪表和 aria-live 结论。
 * 每次运行前清理旧计时器，避免连续点击造成并发更新和错误计数；若动画不停止，应检查终止比较是否仍使用 sampleSize。
 * 不能让减少动效分支产生不同结果，也不能在运行中重新生成随机序列，否则视觉对照与文字证据会失去一致性。
 */
function runExperiment(): void {
  window.clearInterval(timer)
  visibleCount.value = 0
  isRunning.value = true

  if (prefersReducedMotion()) {
    visibleCount.value = sampleSize.value
    isRunning.value = false
    return
  }

  const step = Math.max(1, Math.ceil(sampleSize.value / 32))
  timer = window.setInterval(() => {
    visibleCount.value = Math.min(sampleSize.value, visibleCount.value + step)
    if (visibleCount.value >= sampleSize.value) {
      window.clearInterval(timer)
      isRunning.value = false
    }
  }, 45)
}

function resetExperiment(): void {
  window.clearInterval(timer)
  visibleCount.value = 0
  isRunning.value = false
}

function selectSampleSize(size: number): void {
  sampleSize.value = size
  resetExperiment()
}

function selectMode(nextMode: SignalMode): void {
  mode.value = nextMode
  resetExperiment()
}

onBeforeUnmount(() => window.clearInterval(timer))
</script>

<template>
  <section class="experiment" aria-labelledby="experiment-title">
    <div class="experiment__heading">
      <div>
        <p class="kicker">可操作实验</p>
        <h3 id="experiment-title">同样的轻微偏向，观察多久才算证据？</h3>
      </div>
      <span class="evidence-badge">教学参数</span>
    </div>

    <div class="experiment__controls" aria-label="实验条件">
      <fieldset>
        <legend>生成规律</legend>
        <div class="segmented">
          <button type="button" :class="{ active: mode === 'signal' }" @click="selectMode('signal')">
            轻微偏向 / 62%
          </button>
          <button type="button" :class="{ active: mode === 'baseline' }" @click="selectMode('baseline')">
            随机基线 / 50%
          </button>
        </div>
      </fieldset>

      <fieldset>
        <legend>观察次数</legend>
        <div class="segmented">
          <button
            v-for="size in [20, 80, 160]"
            :key="size"
            type="button"
            :class="{ active: sampleSize === size }"
            @click="selectSampleSize(size)"
          >
            {{ size }} 次
          </button>
        </div>
      </fieldset>
    </div>

    <div class="signal-stage" aria-hidden="true">
      <div class="signal-stage__scale">
        <span>随机波动</span>
        <span class="threshold-label">证据线 z = 2.5</span>
      </div>
      <div class="meter">
        <div class="meter__threshold"></div>
        <div class="meter__fill" :style="{ width: `${Math.min(100, (zScore / 4) * 100)}%` }"></div>
      </div>
      <div class="observations">
        <span
          v-for="(hit, index) in visibleSequence"
          :key="index"
          class="observation"
          :class="{ hit }"
        ></span>
      </div>
    </div>

    <dl class="experiment__metrics">
      <div>
        <dt>当前命中率</dt>
        <dd>{{ visibleCount ? `${Math.round(rate * 100)}%` : '待运行' }}</dd>
      </div>
      <div>
        <dt>偏离基线</dt>
        <dd>{{ visibleCount ? `${zScore.toFixed(2)} z` : '待运行' }}</dd>
      </div>
      <div>
        <dt>当前判断</dt>
        <dd>{{ visibleCount === sampleSize && isFlagged ? '越过证据线' : '证据不足' }}</dd>
      </div>
    </dl>

    <p class="experiment__result" aria-live="polite">{{ resultText }}</p>

    <div class="experiment__actions">
      <button type="button" class="primary-action" :disabled="isRunning" @click="runExperiment">
        {{ isRunning ? '正在观察…' : '运行这组观察' }}
      </button>
      <button type="button" class="quiet-action" @click="resetExperiment">重置</button>
    </div>
  </section>
</template>
