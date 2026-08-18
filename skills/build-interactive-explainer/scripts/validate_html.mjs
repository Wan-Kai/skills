#!/usr/bin/env node
import { readFileSync, statSync } from 'node:fs'
import { resolve } from 'node:path'

const inputPath = process.argv[2]

if (!inputPath) {
  console.error('用法: validate_html.mjs <explainer.html>')
  process.exit(2)
}

const filePath = resolve(inputPath)
const html = readFileSync(filePath, 'utf8')
const errors = []

/**
 * 记录违反单文件交付约束的问题，并在最后一次性输出，方便使用者集中修复。
 * condition 与 message 流入 errors 数组，主流程最终根据数组决定退出码；若漏报，应先检查调用处的正则是否覆盖构建产物。
 * 不能在这里直接退出，否则使用者一次只能发现一个问题，也不能把来源超链接误判为运行时依赖。
 */
function requireCondition(condition, message) {
  if (!condition) errors.push(message)
}

requireCondition(/<!doctype html>/i.test(html), '缺少 HTML doctype')
requireCondition(/<html[^>]+lang=["'][^"']+["']/i.test(html), '缺少页面语言 lang')
requireCondition(/<meta[^>]+name=["']viewport["']/i.test(html), '缺少移动端 viewport')
requireCondition(/<title>[^<]+<\/title>/i.test(html), '缺少页面标题')
requireCondition(/<script(?![^>]+src=)[^>]*>[\s\S]+<\/script>/i.test(html), '缺少内联运行时代码')
requireCondition(statSync(filePath).size > 10_000, '文件过小，可能没有内联应用代码')

const forbiddenPatterns = [
  [/<script[^>]+src=["'][^"']+["']/i, '存在外链或相邻脚本依赖'],
  [/<link[^>]+rel=["']stylesheet["'][^>]*>/i, '存在外部样式表依赖'],
  [/@import\s+(?:url\()?\s*["']?(?:https?:)?\/\//i, 'CSS 包含远程 @import'],
  [/url\(\s*["']?(?:https?:)?\/\//i, 'CSS 包含远程资源'],
  [/<(?:img|audio|video|source)[^>]+src=["'](?!data:)[^"']+["']/i, '媒体资源没有内联为 data URL'],
  [/<source[^>]+srcset=["'](?!data:)[^"']+["']/i, '响应式媒体资源没有内联'],
  [/(?:EXPLAINER_TODO|替换这里)/i, '仍包含未替换的占位内容'],
]

for (const [pattern, message] of forbiddenPatterns) {
  requireCondition(!pattern.test(html), message)
}

if (errors.length) {
  console.error(`HTML 验证失败：${filePath}`)
  for (const error of errors) console.error(`- ${error}`)
  process.exit(1)
}

console.log(`HTML 验证通过：${filePath}`)
console.log(`文件大小：${(statSync(filePath).size / 1024).toFixed(1)} KiB`)
