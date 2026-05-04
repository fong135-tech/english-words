# -*- coding: utf-8 -*-
import os

html_content = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>英语单词乐园</title>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  background: linear-gradient(135deg, #eef2ff 0%, #f8f0ff 100%);
  color: #2d3436;
  min-height: 100vh;
  display: flex; flex-direction: column;
}
.header { background: white; border-bottom: 1px solid #dfe6e9; position: sticky; top: 0; z-index: 100; box-shadow: 0 2px 12px rgba(91,141,238,0.08); }
.header-inner { max-width: 1100px; margin: 0 auto; padding: 0 24px; display: flex; align-items: center; justify-content: space-between; height: 60px; }
.logo { font-size: 1.25rem; font-weight: 900; background: linear-gradient(135deg, #5b8dee, #a55eea); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.nav { display: flex; gap: 4px; }
.nav-btn { padding: 8px 16px; border: none; border-radius: 10px; background: transparent; cursor: pointer; font-size: 0.88rem; font-weight: 600; color: #636e72; font-family: inherit; transition: all 0.15s; }
.nav-btn:hover { background: #f0f4ff; color: #5b8dee; }
.nav-btn.active { background: linear-gradient(135deg, #5b8dee, #a55eea); color: white; box-shadow: 0 2px 8px rgba(91,141,238,0.3); }
.main { max-width: 1100px; margin: 0 auto; padding: 28px 24px; width: 100%; flex: 1; }
.page { display: none; }
.page.active { display: block; }
.page-header { margin-bottom: 20px; }
.page-header h2 { font-size: 1.5rem; font-weight: 800; color: #2d3436; }
.subtitle { font-size: 0.9rem; color: #636e72; margin-top: 4px; }
.card { background: white; border-radius: 16px; padding: 20px 24px; box-shadow: 0 4px 20px rgba(91,141,238,0.08); border: 1px solid #e8ecff; }
.btn { display: inline-flex; align-items: center; justify-content: center; gap: 6px; padding: 10px 20px; border: none; border-radius: 12px; font-size: 0.9rem; font-weight: 700; cursor: pointer; font-family: inherit; transition: all 0.15s; }
.btn-primary { background: linear-gradient(135deg, #5b8dee, #a55eea); color: white; box-shadow: 0 2px 8px rgba(91,141,238,0.3); }
.btn-primary:hover { transform: translateY(-1px); box-shadow: 0 4px 16px rgba(91,141,238,0.4); }
.btn-secondary { background: #f0f4ff; color: #5b8dee; border: 1.5px solid #c8d6ff; }
.btn-secondary:hover { background: #e0eaff; }
.btn-danger { background: #fff0f0; color: #ff5e57; border: 1.5px solid #ffd6d6; }
.btn-sm { padding: 6px 14px; font-size: 0.82rem; border-radius: 8px; }
.btn-lg { padding: 14px 32px; font-size: 1rem; }
input[type="text"], textarea, select { padding: 10px 14px; border: 1.5px solid #dfe6e9; border-radius: 10px; font-size: 0.92rem; font-family: inherit; transition: border-color 0.15s; background: white; }
input[type="text"]:focus, textarea:focus, select:focus { outline: none; border-color: #5b8dee; box-shadow: 0 0 0 3px rgba(91,141,238,0.12); }
#wordbank-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 14px; margin-top: 16px; }
.wb-card { background: white; border-radius: 14px; padding: 16px 14px; box-shadow: 0 2px 12px rgba(91,141,238,0.08); border: 1.5px solid #e8ecff; position: relative; text-align: center; transition: all 0.15s; }
.wb-card:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(91,141,238,0.15); }
.wb-del { position: absolute; top: 6px; right: 6px; background: #fff0f0; border: none; border-radius: 50%; width: 22px; height: 22px; font-size: 11px; cursor: pointer; color: #ff5e57; display: none; }
.wb-card:hover .wb-del { display: block; }
.wb-en { font-size: 1.15rem; font-weight: 800; color: #2d3436; }
.wb-phonetic { font-size: 0.78rem; color: #5b8dee; margin-top: 2px; }
.wb-zh { font-size: 0.8rem; color: #636e72; margin-top: 4px; }
.wb-actions { display: flex; gap: 6px; margin-top: 10px; justify-content: center; }
.week-nav { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; justify-content: center; }
.week-nav button { padding: 6px 14px; border: 1.5px solid #dfe6e9; border-radius: 10px; background: white; cursor: pointer; font-size: 0.88rem; font-family: inherit; font-weight: 600; color: #5b8dee; transition: all 0.15s; }
.week-nav button:hover { background: #f0f4ff; border-color: #5b8dee; }
.week-label { font-size: 0.92rem; font-weight: 700; color: #2d3436; min-width: 180px; text-align: center; }
#learn-word-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 14px; }
.learn-card { background: white; border-radius: 14px; padding: 20px 16px; text-align: center; cursor: pointer; box-shadow: 0 2px 12px rgba(91,141,238,0.08); border: 1.5px solid #e8ecff; transition: all 0.15s; }
.learn-card:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(91,141,238,0.15); border-color: #5b8dee; }
#story-word-checkboxes { display: flex; flex-direction: column; gap: 6px; max-height: 400px; overflow-y: auto; margin-bottom: 12px; padding-right: 4px; }
#story-word-checkboxes label:hover { border-color: #5b8dee; background: #f8faff; }
#story-output { margin-top: 16px; }
#story-text mark { background: linear-gradient(135deg, #ffe066, #ffd43b); padding: 1px 4px; border-radius: 4px; font-weight: 700; }
.quiz-card { margin-bottom: 16px; }
.choice-btn:hover { border-color: #5b8dee !important; background: #f8faff !important; }
.choice-btn.correct { border-color: #26de81 !important; background: #e8fff3 !important; }
.choice-btn.wrong { border-color: #ff5e57 !important; background: #fff0f0 !important; }
#toast { position: fixed; bottom: 80px; left: 50%; transform: translateX(-50%); background: #2d3436; color: white; padding: 10px 22px; border-radius: 24px; font-size: 0.93rem; font-weight: 600; z-index: 9999; pointer-events: none; box-shadow: 0 4px 16px rgba(0,0,0,0.2); transition: opacity 0.3s; opacity: 0; }
footer { background: white; border-top: 1px solid #dfe6e9; padding: 14px 24px; display: flex; align-items: center; justify-content: space-between; font-size: 0.85rem; color: #636e72; margin-top: auto; }
.modal-overlay { display: none; position: fixed; inset: 0; z-index: 200; background: rgba(0,0,0,0.45); align-items: center; justify-content: center; }
.modal-overlay.show { display: flex; }
.modal-box { background: white; border-radius: 16px; padding: 28px 32px; max-width: 560px; width: 92%; max-height: 85vh; overflow-y: auto; position: relative; }
.modal-close { position: absolute; top: 12px; right: 14px; background: #f5f5f5; border: none; border-radius: 50%; width: 32px; height: 32px; font-size: 16px; cursor: pointer; display: flex; align-items: center; justify-content: center; }
</style>
</head>
<body>

<header class="header">
  <div class="header-inner">
    <div class="logo">英语单词乐园</div>
    <nav class="nav">
      <button class="nav-btn active" data-page="wordbank">单词库</button>
      <button class="nav-btn" data-page="learn">学习</button>
      <button class="nav-btn" data-page="story">故事</button>
      <button class="nav-btn" data-page="quiz">测验</button>
    </nav>
  </div>
</header>

<main class="main">

  <!-- 单词库 -->
  <section id="page-wordbank" class="page active">
    <div class="page-header">
      <h2>我的单词库</h2>
      <p class="subtitle">按周分类管理你的单词</p>
    </div>
    <div class="week-nav" id="wordbank-week-nav">
      <button onclick="weekNavigate(-1)">上周</button>
      <span class="week-label" id="wordbank-week-label">本周</span>
      <button onclick="weekNavigate(1)">下周</button>
    </div>
    <div class="card" style="margin-bottom:16px">
      <h3 style="margin-bottom:10px">添加新单词</h3>
      <div style="display:flex;gap:10px;margin-bottom:12px">
        <input id="input-word" type="text" style="flex:1" placeholder="输入英文单词，如: adventure">
        <button id="btn-add-word" class="btn btn-primary">添加</button>
      </div>
      <div style="display:flex;gap:10px;align-items:flex-start">
        <textarea id="input-batch" style="flex:1" placeholder="批量添加：每行一个单词"></textarea>
        <button id="btn-batch-add" class="btn btn-secondary">批量添加</button>
      </div>
    </div>
    <div id="wordbank-grid"></div>
    <div id="wordbank-empty" style="display:none;text-align:center;padding:60px 20px;color:#636e72">
      <p>还没有单词，先添加几个吧！</p>
    </div>
  </section>

  <!-- 学习 -->
  <section id="page-learn" class="page">
    <div class="page-header">
      <h2>单词学习</h2>
      <p class="subtitle">点击单词查看释义，播放发音</p>
    </div>
    <div style="margin-bottom:16px">
      <input id="learn-search" type="text" style="max-width:360px;width:100%" placeholder="搜索单词...">
    </div>
    <div id="learn-word-list"></div>
    <div id="modal-word-detail" class="modal-overlay">
      <div class="modal-box">
        <button class="modal-close" onclick="closeWordDetail()">X</button>
        <div id="word-detail-content"></div>
      </div>
    </div>
    <div id="modal-word-edit" class="modal-overlay">
      <div class="modal-box">
        <button class="modal-close" onclick="closeWordEdit()">X</button>
        <h3 style="margin-bottom:16px">编辑单词信息</h3>
        <div id="word-edit-form"></div>
        <div style="display:flex;gap:10px;margin-top:16px;justify-content:flex-end">
          <button class="btn btn-primary" onclick="saveWordEdit()">保存</button>
          <button class="btn btn-secondary" onclick="closeWordEdit()">取消</button>
        </div>
      </div>
    </div>
  </section>

  <!-- 故事 -->
  <section id="page-story" class="page">
    <div class="page-header">
      <h2>AI 故事生成</h2>
      <p class="subtitle">系统自动推荐单词 - 复制提示词 - 粘贴 AI 回复</p>
    </div>
    <div style="background:#f0f4ff;border:2px solid #c8d6ff;border-radius:16px;padding:20px 24px;margin-bottom:20px">
      <h3 style="color:#5b8dee;margin-bottom:10px">如何使用？</h3>
      <ol style="padding-left:20px;font-size:0.92rem;line-height:2">
        <li>系统已自动勾选：<strong>本周新词</strong>、<strong>需复习词</strong>、<strong>错题</strong></li>
        <li>点击「复制提示词」按钮</li>
        <li>把内容发给 WorkBuddy</li>
        <li>我把故事写好后，你粘贴到文本框</li>
        <li>点击「导入故事」就完成了！</li>
      </ol>
    </div>
    <div style="display:grid;grid-template-columns:320px 1fr;gap:20px">
      <div class="card" style="height:fit-content">
        <h3>选择单词 <span id="story-count" style="background:#5b8dee;color:white;border-radius:12px;padding:1px 10px;font-size:0.8rem">0</span></h3>
        <div id="story-word-checkboxes"></div>
        <div style="display:flex;flex-direction:column;gap:10px;margin-top:12px">
          <label style="font-size:0.9rem;font-weight:600">
            故事风格：
            <select id="story-style" style="width:100%;padding:8px 12px;border:1.5px solid #dfe6e9;border-radius:8px;font-size:0.9rem;margin-top:4px;font-family:inherit">
              <option value="adventure">冒险故事</option>
              <option value="fairy">童话故事</option>
              <option value="funny">搞笑故事</option>
              <option value="science">科学探索</option>
              <option value="daily">日常生活</option>
            </select>
          </label>
          <label style="font-size:0.9rem;font-weight:600">
            故事长度：
            <select id="story-length" style="width:100%;padding:8px 12px;border:1.5px solid #dfe6e9;border-radius:8px;font-size:0.9rem;margin-top:4px;font-family:inherit">
              <option value="short">短篇（约100词）</option>
              <option value="medium" selected>中篇（约200词）</option>
              <option value="long">长篇（约300词）</option>
            </select>
          </label>
        </div>
        <button id="btn-copy-story-prompt" class="btn btn-secondary" style="width:100%;margin-top:12px;justify-content:center">复制提示词给 AI</button>
      </div>
      <div class="card" style="min-height:360px">
        <div id="story-placeholder" style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:300px;color:#636e72;gap:10px">
          <p>复制提示词 - 发给 AI - 粘贴回复到这里</p>
        </div>
        <div id="story-paste-area" style="display:none">
          <h4 style="font-size:0.92rem;color:#5b8dee;margin-bottom:8px">粘贴 AI 回复的故事（JSON格式）</h4>
          <textarea id="story-paste-input" style="width:100%;min-height:150px;font-size:0.9rem;padding:10px 14px;border:1.5px solid #dfe6e9;border-radius:10px;font-family:inherit;resize:vertical"></textarea>
          <div style="display:flex;gap:10px;margin-top:10px">
            <button class="btn btn-primary" onclick="importStory()">导入故事</button>
            <button class="btn btn-secondary" onclick="clearStoryPaste()">清空</button>
          </div>
        </div>
        <div id="story-output" style="display:none">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px;flex-wrap:wrap">
            <h3 id="story-title" style="flex:1;font-size:1.15rem;color:#5b8dee"></h3>
            <button class="btn btn-sm btn-primary" onclick="readStory()">朗读</button>
            <button class="btn btn-sm btn-secondary" onclick="editStory()">编辑</button>
          </div>
          <div id="story-text" style="font-size:1rem;line-height:1.9;color:#2d3436;white-space:pre-wrap;background:#fafbff;padding:16px;border-radius:10px;border:1px solid #dfe6e9"></div>
          <div style="margin-top:16px">
            <h4 style="font-size:0.9rem;color:#636e72;margin-bottom:10px">故事中出现的单词：</h4>
            <div id="story-used-words" style="display:flex;flex-wrap:wrap;gap:8px"></div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 测验 -->
  <section id="page-quiz" class="page">
    <div class="page-header">
      <h2>英语测验</h2>
      <p class="subtitle">多种题型，系统自动推荐本周重点单词</p>
    </div>
    <div id="quiz-auto-hint" style="display:none;background:#e8fff3;border:1.5px solid #26de81;border-radius:12px;padding:12px 16px;margin-bottom:16px;font-size:0.88rem;color:#27ae60"></div>
    <div class="card" style="margin-bottom:20px">
      <div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:16px">
        <label style="flex:1;min-width:140px;font-size:0.9rem;font-weight:600">
          题型：
          <select id="quiz-type" style="width:100%;padding:8px 12px;border:1.5px solid #dfe6e9;border-radius:8px;font-size:0.9rem;margin-top:4px;font-family:inherit">
            <option value="fill">填空题</option>
            <option value="choice">选择题</option>
            <option value="sort">句子排序</option>
            <option value="cloze">完形填空</option>
          </select>
        </label>
        <label style="flex:1;min-width:140px;font-size:0.9rem;font-weight:600">
          题目数量：
          <select id="quiz-count" style="width:100%;padding:8px 12px;border:1.5px solid #dfe6e9;border-radius:8px;font-size:0.9rem;margin-top:4px;font-family:inherit">
            <option value="5">5 题</option>
            <option value="8" selected>8 题</option>
            <option value="10">10 题</option>
          </select>
        </label>
        <label style="flex:1;min-width:140px;font-size:0.9rem;font-weight:600">
          难度：
          <select id="quiz-difficulty" style="width:100%;padding:8px 12px;border:1.5px solid #dfe6e9;border-radius:8px;font-size:0.9rem;margin-top:4px;font-family:inherit">
            <option value="easy">简单（给中文提示）</option>
            <option value="medium" selected>中等（给词性提示）</option>
            <option value="hard">困难（给首字母提示）</option>
          </select>
        </label>
      </div>
      <button id="btn-copy-quiz-prompt" class="btn btn-secondary">复制提示词给 AI</button>
      <div id="quiz-paste-area" style="display:none;margin-top:16px">
        <h4 style="font-size:0.92rem;color:#5b8dee;margin-bottom:8px">粘贴 AI 回复的题目（JSON数组格式）</h4>
        <textarea id="quiz-paste-input" style="width:100%;min-height:150px;font-size:0.9rem;padding:10px 14px;border:1.5px solid #dfe6e9;border-radius:10px;font-family:inherit;resize:vertical"></textarea>
        <div style="display:flex;gap:10px;margin-top:10px">
          <button class="btn btn-primary" onclick="importQuiz()">导入题目</button>
          <button class="btn btn-secondary" onclick="clearQuizPaste()">清空</button>
        </div>
      </div>
    </div>
    <div id="quiz-questions" style="display:flex;flex-direction:column;gap:20px"></div>
    <div id="quiz-footer" style="display:none;gap:14px;justify-content:center;margin-top:28px">
      <button id="btn-check-quiz" class="btn btn-primary btn-lg" onclick="checkQuiz()">提交答案</button>
      <button id="btn-retry-quiz" class="btn btn-secondary btn-lg" onclick="retryQuiz()" style="display:none">重新作答</button>
    </div>
    <div id="quiz-result" style="display:none;background:white;border-radius:16px;padding:28px;text-align:center;box-shadow:0 4px 20px rgba(91,141,238,0.12);margin-top:24px"></div>
  </section>

</main>

<div id="toast"></div>
<footer>
  <span>英语单词乐园 - 纯离线可用 - 让学英语更有趣</span>
</footer>

<script src="app.js"></script>
</body>
</html>"""

js_content = r"""/* 英语单词乐园 - 离线版 v2.0 */
var STORAGE_KEY = 'wordpal_words';
var STORY_KEY   = 'wordpal_story';
var QUIZ_LOG_KEY = 'wordpal_quizlog';

var wordBank   = [];
var lastStory  = '';
var lastStoryWords = [];
var lastStoryTitle = '';
var quizData   = [];
var quizAnswers = {};
var currentEditWordId = null;
var currentWeekOffset = 0;

var REVIEW_INTERVALS = [1, 3, 7, 14, 30];

/* ========== 工具函数 ========== */
function formatDate(d) {
  var y = d.getFullYear();
  var m = ('0' + (d.getMonth() + 1)).slice(-2);
  var day = ('0' + d.getDate()).slice(-2);
  return y + '-' + m + '-' + day;
}

function todayStr() {
  return formatDate(new Date());
}

function escHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

var toastTimer = null;
function showToast(msg) {
  var toast = document.getElementById('toast');
  if (!toast) return;
  toast.textContent = msg;
  toast.style.opacity = '1';
  clearTimeout(toastTimer);
  toastTimer = setTimeout(function() { toast.style.opacity = '0'; }, 2800);
}

/* ========== 记忆曲线 ========== */
function buildReviewPlan(addDateStr) {
  var d = new Date(addDateStr);
  var plan = [];
  for (var i = 0; i < REVIEW_INTERVALS.length; i++) {
    var r = new Date(d);
    r.setDate(r.getDate() + REVIEW_INTERVALS[i]);
    plan.push({ date: formatDate(r), done: false });
  }
  return plan;
}

function getWeekRange(offset) {
  var now = new Date();
  now.setDate(now.getDate() + offset * 7);
  var day = now.getDay();
  var diff = now.getDate() - day + (day === 0 ? -6 : 1);
  var monday = new Date(now);
  monday.setDate(diff);
  monday.setHours(0,0,0,0);
  var sunday = new Date(monday);
  sunday.setDate(sunday.getDate() + 6);
  sunday.setHours(23,59,59,999);
  return { start: monday, end: sunday };
}

function getWeekLabel(offset) {
  var range = getWeekRange(offset);
  var s = range.start;
  var e = range.end;
  var sStr = (s.getMonth()+1) + '/' + s.getDate();
  var eStr = (e.getMonth()+1) + '/' + e.getDate();
  if (offset === 0) return '本周 ' + sStr + '-' + eStr;
  if (offset === -1) return '上周 ' + sStr + '-' + eStr;
  if (offset === 1) return '下周 ' + sStr + '-' + eStr;
  return sStr + '-' + eStr;
}

/* ========== 三类单词获取 ========== */
function getThisWeekWords() {
  var range = getWeekRange(0);
  var result = [];
  for (var i = 0; i < wordBank.length; i++) {
    var w = wordBank[i];
    if (!w.addDate) continue;
    var d = new Date(w.addDate);
    if (d >= range.start && d <= range.end) result.push(w);
  }
  return result;
}

function getWrongWords() {
  var result = [];
  for (var i = 0; i < wordBank.length; i++) {
    if (wordBank[i].wrongCount > 0 && !wordBank[i].mastered) {
      result.push(wordBank[i]);
    }
  }
  result.sort(function(a, b) { return b.wrongCount - a.wrongCount; });
  return result;
}

function getReviewWords() {
  var today = todayStr();
  var result = [];
  for (var i = 0; i < wordBank.length; i++) {
    var w = wordBank[i];
    if (w.mastered) continue;
    if (!w.reviewPlan) continue;
    for (var j = 0; j < w.reviewPlan.length; j++) {
      var rp = w.reviewPlan[j];
      if (!rp.done && rp.date <= today) {
        result.push(w);
        break;
      }
    }
  }
  return result;
}

function markWordCorrect(wordId) {
  for (var i = 0; i < wordBank.length; i++) {
    if (String(wordBank[i].id) === String(wordId)) {
      wordBank[i].wrongCount = Math.max(0, (wordBank[i].wrongCount || 0) - 1);
      if (!wordBank[i]._recentCorrects) wordBank[i]._recentCorrects = 0;
      wordBank[i]._recentCorrects++;
      if (wordBank[i]._recentCorrects >= 3) wordBank[i].mastered = true;
      saveWords();
      return;
    }
  }
}

function markWordWrong(wordId) {
  for (var i = 0; i < wordBank.length; i++) {
    if (String(wordBank[i].id) === String(wordId)) {
      wordBank[i].wrongCount = (wordBank[i].wrongCount || 0) + 1;
      wordBank[i].lastWrong = todayStr();
      wordBank[i]._recentCorrects = 0;
      wordBank[i].mastered = false;
      saveWords();
      return;
    }
  }
}

/* ========== Storage ========== */
function saveWords() {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(wordBank)); } catch(e) {}
}

function loadWords() {
  try {
    var raw = localStorage.getItem(STORAGE_KEY);
    wordBank = raw ? JSON.parse(raw) : [];
    for (var i = 0; i < wordBank.length; i++) {
      var w = wordBank[i];
      if (!w.addDate) w.addDate = '';
      if (!w.reviewPlan) w.reviewPlan = [];
      if (w.wrongCount === undefined) w.wrongCount = 0;
      if (!w.lastWrong) w.lastWrong = '';
      if (w.mastered === undefined) w.mastered = false;
    }
  } catch(e) { wordBank = []; }
}

function saveStory() {
  try {
    localStorage.setItem(STORY_KEY, JSON.stringify({
      title: lastStoryTitle, text: lastStory, words: lastStoryWords
    }));
  } catch(e) {}
}

function loadStory() {
  try {
    var raw = localStorage.getItem(STORY_KEY);
    if (!raw) return;
    var d = JSON.parse(raw);
    lastStoryTitle = d.title || '';
    lastStory     = d.text  || '';
    lastStoryWords = d.words || [];
  } catch(e) {}
}

function saveQuizLog(log) {
  try {
    var arr = JSON.parse(localStorage.getItem(QUIZ_LOG_KEY) || '[]');
    arr.push(log);
    if (arr.length > 500) arr = arr.slice(arr.length - 500);
    localStorage.setItem(QUIZ_LOG_KEY, JSON.stringify(arr));
  } catch(e) {}
}

/* ========== Navigation ========== */
document.querySelectorAll('.nav-btn').forEach(function(btn) {
  btn.addEventListener('click', function() {
    document.querySelectorAll('.nav-btn').forEach(function(b) { b.classList.remove('active'); });
    document.querySelectorAll('.page').forEach(function(p) { p.classList.remove('active'); });
    btn.classList.add('active');
    var pageId = 'page-' + btn.dataset.page;
    document.getElementById(pageId).classList.add('active');
    if (btn.dataset.page === 'learn')  renderLearnPage();
    if (btn.dataset.page === 'wordbank') renderWordBank();
    if (btn.dataset.page === 'story') { renderStoryCheckboxes(); tryShowSavedStory(); }
    if (btn.dataset.page === 'quiz')   renderQuizPage();
  });
});

/* ========== Word Bank ========== */
function renderWordBank() {
  var grid  = document.getElementById('wordbank-grid');
  var empty = document.getElementById('wordbank-empty');
  var weekNav = document.getElementById('wordbank-week-nav');
  var weekLabel = document.getElementById('wordbank-week-label');

  if (weekLabel) weekLabel.textContent = getWeekLabel(currentWeekOffset);

  var range = getWeekRange(currentWeekOffset);
  var weekWords = [];
  for (var i = 0; i < wordBank.length; i++) {
    var w = wordBank[i];
    if (!w.addDate) { weekWords.push(w); continue; }
    var d = new Date(w.addDate);
    if (d >= range.start && d <= range.end) weekWords.push(w);
  }

  if (wordBank.length === 0) {
    grid.innerHTML = '';
    empty.style.display = 'block';
    if (weekNav) weekNav.style.display = 'none';
    return;
  }
  empty.style.display = 'none';
  if (weekNav) weekNav.style.display = 'flex';

  if (weekWords.length === 0) {
    grid.innerHTML = '<div style="text-align:center;padding:40px 20px;color:#636e72;grid-column:1/-1"><p>这一周还没有添加单词</p></div>';
  } else {
    var html = '';
    for (var j = 0; j < weekWords.length; j++) {
      var w = weekWords[j];
      var badge = '';
      if (w.mastered) {
        badge = '<span style="background:#26de81;color:white;font-size:0.7rem;padding:2px 8px;border-radius:10px;margin-left:6px">已掌握</span>';
      } else if (w.wrongCount > 0) {
        badge = '<span style="background:#ff5e57;color:white;font-size:0.7rem;padding:2px 8px;border-radius:10px;margin-left:6px">需复习</span>';
      }
      html += '<div class="wb-card" data-id="' + w.id + '">'
        + '<button class="wb-del" data-id="' + w.id + '" title="删除">X</button>'
        + '<div class="wb-en">' + escHtml(w.word) + badge + '</div>';
      if (w.phonetic) html += '<div class="wb-phonetic">' + escHtml(w.phonetic) + '</div>';
      if (w.zh) {
        html += '<div class="wb-zh">' + escHtml(w.zh) + '</div>';
      } else {
        html += '<div class="wb-zh" style="color:#bbb">未填写释义</div>';
      }
      if (w.addDate) {
        html += '<div style="font-size:0.72rem;color:#aaa;margin-top:4px">' + escHtml(w.addDate) + '</div>';
      }
      html += '<div class="wb-actions">'
        + '<button class="btn btn-sm btn-primary wb-learn" data-id="' + w.id + '">发音</button>'
        + '<button class="btn btn-sm btn-secondary wb-edit" data-id="' + w.id + '">编辑</button>'
        + '</div></div>';
    }
    grid.innerHTML = html;
  }

  grid.querySelectorAll('.wb-del').forEach(function(b) {
    b.addEventListener('click', function(e) { e.stopPropagation(); deleteWord(b.dataset.id); });
  });
  grid.querySelectorAll('.wb-learn').forEach(function(b) {
    b.addEventListener('click', function(e) { e.stopPropagation(); speakWordById(b.dataset.id); });
  });
  grid.querySelectorAll('.wb-edit').forEach(function(b) {
    b.addEventListener('click', function(e) { e.stopPropagation(); openWordEdit(b.dataset.id); });
  });
}

function weekNavigate(dir) {
  currentWeekOffset += dir;
  renderWordBank();
}

function addWordToBank(wordStr) {
  var word = wordStr.trim().toLowerCase();
  if (!word) return false;
  for (var i = 0; i < wordBank.length; i++) {
    if (wordBank[i].word.toLowerCase() === word) return false;
  }
  var today = todayStr();
  wordBank.push({
    id: Date.now() + Math.random(),
    word: word, zh: '', phonetic: '',
    definitions: [], examples: [], etymology: '',
    addDate: today,
    reviewPlan: buildReviewPlan(today),
    wrongCount: 0, lastWrong: '', mastered: false
  });
  saveWords();
  renderWordBank();
  return true;
}

function deleteWord(id) {
  var filtered = [];
  for (var i = 0; i < wordBank.length; i++) {
    if (String(wordBank[i].id) !== String(id)) filtered.push(wordBank[i]);
  }
  wordBank = filtered;
  saveWords();
  renderWordBank();
}

document.getElementById('btn-add-word').addEventListener('click', function() {
  var input = document.getElementById('input-word');
  var parts = input.value.split(/[,\uff0c;\uff1b\s]+/);
  var added = 0;
  for (var i = 0; i < parts.length; i++) { if (addWordToBank(parts[i])) added++; }
  if (added > 0) { input.value = ''; showToast('已添加 ' + added + ' 个单词'); }
  else showToast('单词已存在或输入为空');
});

document.getElementById('input-word').addEventListener('keydown', function(e) {
  if (e.key === 'Enter') document.getElementById('btn-add-word').click();
});

document.getElementById('btn-batch-add').addEventListener('click', function() {
  var ta = document.getElementById('input-batch');
  var lines = ta.value.split('\n');
  var added = 0;
  for (var i = 0; i < lines.length; i++) { if (addWordToBank(lines[i])) added++; }
  if (added > 0) { ta.value = ''; showToast('批量添加了 ' + added + ' 个单词'); }
  else showToast('单词已全部存在或输入为空');
});

/* ========== TTS ========== */
function speakWord(word) {
  if (!('speechSynthesis' in window)) { showToast('浏览器不支持语音合成'); return; }
  window.speechSynthesis.cancel();
  var utter = new SpeechSynthesisUtterance(word);
  utter.lang = 'en-US';
  utter.rate = 0.85;
  var voices = window.speechSynthesis.getVoices();
  for (var i = 0; i < voices.length; i++) {
    if (voices[i].lang.indexOf('en') === 0) { utter.voice = voices[i]; break; }
  }
  window.speechSynthesis.speak(utter);
}

function speakWordById(id) {
  for (var i = 0; i < wordBank.length; i++) {
    if (String(wordBank[i].id) === String(id)) { speakWord(wordBank[i].word); return; }
  }
}

/* ========== Learn Page ========== */
function renderLearnPage() {
  var list   = document.getElementById('learn-word-list');
  var search = (document.getElementById('learn-search').value || '').toLowerCase();
  var filtered = [];
  for (var i = 0; i < wordBank.length; i++) {
    var w = wordBank[i];
    if (w.word.toLowerCase().indexOf(search) >= 0 || (w.zh && w.zh.indexOf(search) >= 0)) {
      filtered.push(w);
    }
  }
  if (filtered.length === 0) {
    list.innerHTML = '<div style="text-align:center;padding:50px 20px;color:#636e72;grid-column:1/-1"><p>'
      + (wordBank.length === 0 ? '请先添加单词' : '没有找到匹配的单词') + '</p></div>';
    return;
  }
  var html = '';
  for (var j = 0; j < filtered.length; j++) {
    var w = filtered[j];
    var badge = '';
    if (w.mastered) badge = ' 已掌握';
    else if (w.wrongCount > 0) badge = ' 需复习';
    html += '<div class="learn-card" data-id="' + w.id + '">'
      + '<div style="font-size:1.3rem;font-weight:800;color:#2d3436">' + escHtml(w.word) + badge + '</div>';
    if (w.phonetic) html += '<div style="font-size:0.8rem;color:#5b8dee;margin-top:4px">' + escHtml(w.phonetic) + '</div>';
    var zhShort = (w.zh || '').split(';')[0] || w.zh || '';
    if (zhShort) {
      html += '<div style="font-size:0.8rem;color:#636e72;margin-top:6px">' + escHtml(zhShort) + '</div>';
    }
    html += '</div>';
  }
  list.innerHTML = html;
  list.querySelectorAll('.learn-card').forEach(function(card) {
    card.addEventListener('click', function() { openWordDetail(card.dataset.id); });
  });
}

document.getElementById('learn-search').addEventListener('input', renderLearnPage);

/* ========== Word Detail ========== */
function openWordDetail(id) {
  var word = null;
  for (var i = 0; i < wordBank.length; i++) {
    if (String(wordBank[i].id) === String(id)) { word = wordBank[i]; break; }
  }
  if (!word) return;
  document.getElementById('modal-word-detail').classList.add('show');
  renderWordDetailContent(word);
}

function renderWordDetailContent(word) {
  var c = document.getElementById('word-detail-content');
  var defsHtml = '';
  if (word.definitions && word.definitions.length > 0) {
    for (var i = 0; i < word.definitions.length; i++) {
      var d = word.definitions[i];
      defsHtml += '<div style="background:#f8f9ff;border-left:3px solid #5b8dee;padding:8px 12px;border-radius:0 8px 8px 0;margin-bottom:8px;font-size:0.93rem">'
        + (d.pos ? '<span style="font-weight:700;color:#a55eea;font-size:0.8rem">' + escHtml(d.pos) + ' </span>' : '')
        + escHtml(d.en || '')
        + (d.zh ? '<br><span style="color:#636e72;font-size:0.88rem">' + escHtml(d.zh) + '</span>' : '')
        + '</div>';
    }
  } else {
    defsHtml = '<div style="color:#999;padding:8px 0">暂无释义，请点击编辑按钮填写</div>';
  }
  var exHtml = '';
  if (word.examples && word.examples.length > 0) {
    for (var j = 0; j < word.examples.length; j++) {
      exHtml += '<div style="font-size:0.9rem;font-style:italic;color:#636e72;background:#fffbf0;padding:6px 10px;border-radius:8px;border-left:3px solid #ff9f43;margin-bottom:6px">' + escHtml(word.examples[j]) + '</div>';
    }
  }
  var etHtml = '';
  if (word.etymology) {
    etHtml = '<div style="margin-top:18px"><div style="font-size:0.85rem;color:#636e72;margin-bottom:8px">词源</div>'
      + '<div style="background:#f0fff8;padding:10px 14px;border-radius:8px;font-size:0.9rem;color:#27ae60;border-left:3px solid #26de81">' + escHtml(word.etymology) + '</div></div>';
  }
  var reviewHtml = '';
  if (word.mastered) {
    reviewHtml = '<div style="margin-top:14px;padding:10px 14px;background:#e8fff3;border-radius:8px;border-left:3px solid #26de81;font-size:0.88rem;color:#27ae60">已掌握！无需再复习</div>';
  } else if (word.reviewPlan && word.reviewPlan.length > 0) {
    var rpHtml = '';
    for (var k = 0; k < word.reviewPlan.length; k++) {
      var rp = word.reviewPlan[k];
      var icon = rp.done ? '完成' : (rp.date < todayStr() ? '待复习' : '未到');
      rpHtml += '<div style="font-size:0.82rem;color:#636e72;padding:2px 0">' + icon + ' ' + rp.date + '</div>';
    }
    reviewHtml = '<div style="margin-top:14px"><div style="font-size:0.85rem;color:#636e72;margin-bottom:8px">复习计划</div>'
      + '<div style="background:#f8f9ff;padding:10px 14px;border-radius:8px;border-left:3px solid #5b8dee;font-size:0.85rem">' + rpHtml + '</div>'
      + (word.wrongCount ? '<div style="font-size:0.82rem;color:#ff5e57;margin-top:6px">累计答错 ' + word.wrongCount + ' 次</div>' : '')
      + '</div>';
  }

  c.innerHTML = ''
    + '<div style="font-size:2rem;font-weight:900;color:#5b8dee">' + escHtml(word.word) + '</div>'
    + (word.phonetic ? '<div style="font-size:1rem;color:#636e72;font-style:italic;margin-top:2px">' + escHtml(word.phonetic) + '</div>' : '')
    + '<button style="display:inline-flex;align-items:center;gap:6px;margin-top:12px;padding:8px 20px;background:linear-gradient(135deg,#5b8dee,#a55eea);color:white;border:none;border-radius:24px;cursor:pointer;font-size:0.95rem;font-weight:700;font-family:inherit" onclick="speakWord(\'' + word.word.replace(/'/g, '\\'') + '\')">播放发音</button>'
    + '<button style="display:inline-flex;align-items:center;gap:6px;margin-top:10px;padding:8px 20px;background:#f0f4ff;color:#5b8dee;border:1.5px solid #5b8dee;border-radius:24px;cursor:pointer;font-size:0.95rem;font-weight:700;font-family:inherit;width:100%;justify-content:center" onclick="closeWordDetail();openWordEdit(\'' + word.id + '\')">编辑单词信息</button>'
    + '<div style="margin-top:18px"><div style="font-size:0.85rem;color:#636e72;margin-bottom:8px">释义</div><div>' + defsHtml + '</div></div>'
    + (exHtml ? '<div style="margin-top:18px"><div style="font-size:0.85rem;color:#636e72;margin-bottom:8px">例句</div><div>' + exHtml + '</div></div>' : '')
    + etHtml
    + reviewHtml;
}

function closeWordDetail() {
  document.getElementById('modal-word-detail').classList.remove('show');
}

/* ========== Word Edit ========== */
function openWordEdit(id) {
  var word = null;
  for (var i = 0; i < wordBank.length; i++) {
    if (String(wordBank[i].id) === String(id)) { word = wordBank[i]; break; }
  }
  if (!word) return;
  currentEditWordId = id;
  document.getElementById('modal-word-edit').classList.add('show');

  var defsHtml = '';
  if (!word.definitions) word.definitions = [];
  for (var i = 0; i < word.definitions.length; i++) {
    var d = word.definitions[i];
    defsHtml += '<div style="display:flex;gap:6px;align-items:center;margin-bottom:6px">'
      + '<input type="text" value="' + escHtml(d.pos || '') + '" placeholder="词性" style="width:60px;padding:6px 8px;border:1.5px solid #dfe6e9;border-radius:6px;font-size:0.85rem">'
      + '<input type="text" value="' + escHtml(d.en  || '') + '" placeholder="英文释义" style="flex:1;padding:6px 8px;border:1.5px solid #dfe6e9;border-radius:6px;font-size:0.85rem">'
      + '<input type="text" value="' + escHtml(d.zh  || '') + '" placeholder="中文" style="flex:1;padding:6px 8px;border:1.5px solid #dfe6e9;border-radius:6px;font-size:0.85rem">'
      + '<button data-idx="' + i + '" class="btn btn-sm btn-danger del-def">X</button>'
      + '</div>';
  }

  var form = document.getElementById('word-edit-form');
  form.innerHTML = ''
    + '<div style="margin-bottom:10px"><span style="font-size:0.85rem;font-weight:700;color:#636e72">英文单词</span>'
    + '<input id="ef-word" type="text" value="' + escHtml(word.word) + '" style="width:100%;padding:8px 12px;border:1.5px solid #dfe6e9;border-radius:8px;font-size:0.95rem;margin-top:4px"></div>'
    + '<div style="margin-bottom:10px"><span style="font-size:0.85rem;font-weight:700;color:#636e72">音标</span>'
    + '<input id="ef-phonetic" type="text" value="' + escHtml(word.phonetic || '') + '" placeholder="如: /adventur/" style="width:100%;padding:8px 12px;border:1.5px solid #dfe6e9;border-radius:8px;font-size:0.95rem;margin-top:4px"></div>'
    + '<div style="margin-bottom:10px"><span style="font-size:0.85rem;font-weight:700;color:#636e72">中文释义</span>'
    + '<input id="ef-zh" type="text" value="' + escHtml(word.zh || '') + '" placeholder="逗号分隔多个意思" style="width:100%;padding:8px 12px;border:1.5px solid #dfe6e9;border-radius:8px;font-size:0.95rem;margin-top:4px"></div>'
    + '<div style="margin-bottom:10px"><span style="font-size:0.85rem;font-weight:700;color:#636e72">释义列表</span>'
    + '<div id="ef-defs">' + defsHtml + '</div>'
    + '<button class="btn btn-sm btn-secondary" id="ef-add-def" style="margin-top:6px">+ 添加释义</button></div>'
    + '<div style="margin-bottom:10px"><span style="font-size:0.85rem;font-weight:700;color:#636e72">例句（每行一条）</span>'
    + '<textarea id="ef-examples" style="width:100%;min-height:70px;padding:8px 12px;border:1.5px solid #dfe6e9;border-radius:8px;font-size:0.9rem;font-family:inherit;resize:vertical">' + (word.examples || []).join('\n') + '</textarea></div>'
    + '<div style="margin-bottom:10px"><span style="font-size:0.85rem;font-weight:700;color:#636e72">词源（中文）</span>'
    + '<textarea id="ef-etymology" style="width:100%;min-height:60px;padding:8px 12px;border:1.5px solid #dfe6e9;border-radius:8px;font-size:0.9rem;font-family:inherit;resize:vertical">' + escHtml(word.etymology || '') + '</textarea></div>';

  form.querySelectorAll('.del-def').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var idx = parseInt(this.dataset.idx);
      word.definitions.splice(idx, 1);
      openWordEdit(id);
    });
  });

  document.getElementById('ef-add-def').addEventListener('click', function() {
    if (!word.definitions) word.definitions = [];
    word.definitions.push({ pos: '', en: '', zh: '' });
    openWordEdit(id);
  });
}

function closeWordEdit() {
  document.getElementById('modal-word-edit').classList.remove('show');
}

function saveWordEdit() {
  if (!currentEditWordId) return;
  var word = null;
  for (var i = 0; i < wordBank.length; i++) {
    if (String(wordBank[i].id) === String(currentEditWordId)) { word = wordBank[i]; break; }
  }
  if (!word) return;
  word.word     = (document.getElementById('ef-word').value || '').trim();
  word.phonetic = (document.getElementById('ef-phonetic').value || '').trim();
  word.zh       = (document.getElementById('ef-zh').value || '').trim();
  word.definitions = [];
  var defsDiv = document.getElementById('ef-defs');
  if (defsDiv) {
    var rows = defsDiv.children;
    for (var r = 0; r < rows.length; r++) {
      var inputs = rows[r].querySelectorAll('input');
      if (inputs.length >= 3) {
        var pos = (inputs[0].value || '').trim();
        var en  = (inputs[1].value || '').trim();
        var zh  = (inputs[2].value || '').trim();
        if (en || zh) word.definitions.push({ pos: pos, en: en, zh: zh });
      }
    }
  }
  var exVal = document.getElementById('ef-examples').value || '';
  word.examples = exVal.split('\n').map(function(l){ return l.trim(); }).filter(function(l){ return l.length > 0; });
  word.etymology = (document.getElementById('ef-etymology').value || '').trim();
  saveWords();
  renderWordBank();
  closeWordEdit();
  showToast('单词信息已保存');
}

/* ========== Story Page ========== */
function renderStoryCheckboxes() {
  var thisWeek = getThisWeekWords();
  var wrong   = getWrongWords();
  var review  = getReviewWords();
  var idMap = {};
  var combined = [];
  function addList(list) {
    for (var i = 0; i < list.length; i++) {
      if (!idMap[list[i].id]) { idMap[list[i].id] = true; combined.push(list[i]); }
    }
  }
  addList(thisWeek);
  addList(wrong);
  addList(review);

  var container = document.getElementById('story-word-checkboxes');
  if (combined.length === 0 && wordBank.length === 0) {
    container.innerHTML = '<div style="color:#999;font-size:0.9rem;padding:10px 0">请先添加单词</div>';
    return;
  }

  var html = '';
  if (thisWeek.length > 0) {
    html += '<div style="font-size:0.82rem;font-weight:700;color:#5b8dee;margin-bottom:6px;margin-top:4px">本周新学 (' + thisWeek.length + ')</div>';
    html += buildCheckboxGroup(thisWeek);
  }
  if (review.length > 0) {
    html += '<div style="font-size:0.82rem;font-weight:700;color:#ff9f43;margin-bottom:6px;margin-top:10px">本周需复习 (' + review.length + ')</div>';
    html += buildCheckboxGroup(review);
  }
  if (wrong.length > 0) {
    html += '<div style="font-size:0.82rem;font-weight:700;color:#ff5e57;margin-bottom:6px;margin-top:10px">错题本 (' + wrong.length + ')</div>';
    html += buildCheckboxGroup(wrong);
  }
  var remaining = [];
  for (var i = 0; i < wordBank.length; i++) {
    if (!idMap[wordBank[i].id]) remaining.push(wordBank[i]);
  }
  if (remaining.length > 0) {
    html += '<div style="font-size:0.82rem;font-weight:700;color:#636e72;margin-bottom:6px;margin-top:10px">其他单词</div>';
    html += buildCheckboxGroup(remaining);
  }
  container.innerHTML = html;

  container.querySelectorAll('input[type="checkbox"]').forEach(function(cb) {
    cb.checked = true;
    cb.addEventListener('change', updateStoryCount);
  });
  updateStoryCount();
}

function buildCheckboxGroup(words) {
  var html = '';
  for (var i = 0; i < words.length; i++) {
    var w = words[i];
    html += '<label style="display:flex;align-items:center;gap:10px;padding:8px 12px;border-radius:10px;border:1.5px solid #dfe6e9;cursor:pointer;transition:all 0.15s;font-size:0.9rem">'
      + '<input type="checkbox" value="' + w.id + '" style="accent-color:#5b8dee;width:16px;height:16px;cursor:pointer">'
      + '<span style="font-weight:700">' + escHtml(w.word) + '</span>'
      + (w.zh ? '<span style="color:#636e72;font-size:0.8rem">' + escHtml(w.zh.split(';')[0]) + '</span>' : '')
      + '</label>';
  }
  return html;
}

function updateStoryCount() {
  var checked = document.querySelectorAll('#story-word-checkboxes input:checked');
  var cnt = document.getElementById('story-count');
  if (cnt) cnt.textContent = checked.length;
}

document.getElementById('btn-copy-story-prompt').addEventListener('click', function() {
  var checked = document.querySelectorAll('#story-word-checkboxes input:checked');
  if (checked.length < 3) { showToast('请至少选择 3 个单词'); return; }
  var wordList = [];
  var zhList = [];
  checked.forEach(function(cb) {
    for (var i = 0; i < wordBank.length; i++) {
      if (String(wordBank[i].id) === String(cb.value)) {
        wordList.push(wordBank[i].word);
        zhList.push(wordBank[i].zh ? wordBank[i].word + '(' + wordBank[i].zh + ')' : wordBank[i].word);
        break;
      }
    }
  });
  var styleMap = { adventure: '冒险故事', fairy: '童话故事', funny: '搞笑故事', science: '科学探索故事', daily: '日常生活故事' };
  var lenMap   = { short: '约100词', medium: '约200词', long: '约300词' };
  var style = styleMap[document.getElementById('story-style').value] || '有趣的故事';
  var len   = lenMap[document.getElementById('story-length').value] || '约200词';
  var prompt = '请用英文给6-12岁孩子写一个' + style + '（' + len + '）。\n'
    + '要求：\n1. 必须自然使用以下所有单词：' + wordList.join(', ') + '\n'
    + '2. 每个单词至少出现1次，用**加粗**标注\n'
    + '3. 返回严格JSON格式：{"title":"标题","story":"正文，目标单词用**加粗**标注"}\n'
    + '4. 只返回JSON，不要用markdown包裹\n'
    + '参考中文：' + zhList.join('、');
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(prompt).then(function() {
      showToast('提示词已复制！请粘贴给 WorkBuddy');
      document.getElementById('story-paste-area').style.display = 'block';
    }).catch(function() { showToast('自动复制失败，请手动复制'); });
  } else { showToast('浏览器不支持自动复制'); }
});

function importStory() {
  var raw = (document.getElementById('story-paste-input').value || '').trim();
  if (!raw) { showToast('请先粘贴内容'); return; }
  var data = null;
  var jsonMatch = raw.match(/\{[\s\S]*\}/);
  if (jsonMatch) { try { data = JSON.parse(jsonMatch[0]); } catch(e) {} }
  if (!data || !data.story) data = { title: '我的故事', story: raw };
  lastStoryTitle = data.title || '我的故事';
  lastStory     = data.story || '';
  lastStoryWords = [];
  var checked = document.querySelectorAll('#story-word-checkboxes input:checked');
  checked.forEach(function(cb) {
    for (var i = 0; i < wordBank.length; i++) {
      if (String(wordBank[i].id) === String(cb.value)) { lastStoryWords.push(wordBank[i]); break; }
    }
  });
  saveStory();
  displayStory();
  showToast('故事已导入！');
}

function clearStoryPaste() {
  document.getElementById('story-paste-input').value = '';
  document.getElementById('story-paste-area').style.display = 'none';
}

function displayStory() {
  document.getElementById('story-placeholder').style.display = 'none';
  document.getElementById('story-paste-area').style.display  = 'none';
  document.getElementById('story-output').style.display     = 'block';
  document.getElementById('story-title').textContent = lastStoryTitle;
  var highlighted = escHtml(lastStory);
  for (var i = 0; i < lastStoryWords.length; i++) {
    var w = lastStoryWords[i];
    var escaped = w.word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    var regex = new RegExp('\\b(' + escaped + ')\\b', 'gi');
    highlighted = highlighted.replace(regex, '<mark>$1</mark>');
  }
  highlighted = highlighted.replace(/\*\*(.*?)\*\*/g, '<mark>$1</mark>');
  document.getElementById('story-text').innerHTML = highlighted;
  var tagsHtml = '';
  for (var j = 0; j < lastStoryWords.length; j++) {
    tagsHtml += '<span style="background:linear-gradient(135deg,#5b8dee,#a55eea);color:white;padding:4px 12px;border-radius:20px;font-size:0.82rem;font-weight:700">' + escHtml(lastStoryWords[j].word) + '</span>';
  }
  document.getElementById('story-used-words').innerHTML = tagsHtml;
}

function tryShowSavedStory() {
  if (lastStory) displayStory();
}

function readStory() {
  if (!lastStory) return;
  if (window.speechSynthesis && window.speechSynthesis.speaking) { window.speechSynthesis.cancel(); return; }
  var utter = new SpeechSynthesisUtterance(lastStory);
  utter.lang = 'en-US'; utter.rate = 0.8;
  var voices = window.speechSynthesis.getVoices();
  for (var i = 0; i < voices.length; i++) {
    if (voices[i].lang.indexOf('en') === 0) { utter.voice = voices[i]; break; }
  }
  window.speechSynthesis.speak(utter);
  showToast('正在朗读故事');
}

function editStory() {
  document.getElementById('story-paste-input').value = lastStory;
  document.getElementById('story-output').style.display      = 'none';
  document.getElementById('story-paste-area').style.display = 'block';
}

/* ========== Quiz Page ========== */
function renderQuizPage() {
  quizData = [];
  quizAnswers = {};
  var qsEl  = document.getElementById('quiz-questions');
  var resEl = document.getElementById('quiz-result');
  var footEl = document.getElementById('quiz-footer');
  var pasteEl = document.getElementById('quiz-paste-area');
  if (qsEl) qsEl.innerHTML = '';
  if (resEl) resEl.style.display = 'none';
  if (footEl) footEl.style.display = 'none';
  if (pasteEl) pasteEl.style.display = 'none';
  var autoWords = getAutoQuizWords();
  var hintEl = document.getElementById('quiz-auto-hint');
  if (hintEl) {
    if (autoWords.length > 0) {
      hintEl.innerHTML = '系统推荐单词（' + autoWords.length + '个）：'
        + autoWords.map(function(w){ return escHtml(w.word); }).join('、');
      hintEl.style.display = 'block';
    } else {
      hintEl.style.display = 'none';
    }
  }
}

function getAutoQuizWords() {
  var thisWeek = getThisWeekWords();
  var wrong   = getWrongWords();
  var review  = getReviewWords();
  var idMap = {};
  var combined = [];
  function addList(list) {
    for (var i = 0; i < list.length; i++) {
      if (!idMap[list[i].id]) { idMap[list[i].id] = true; combined.push(list[i]); }
    }
  }
  addList(thisWeek); addList(wrong); addList(review);
  return combined;
}

document.getElementById('btn-copy-quiz-prompt').addEventListener('click', function() {
  var qType  = document.getElementById('quiz-type').value;
  var qCount = parseInt(document.getElementById('quiz-count').value) || 8;
  var diff   = document.getElementById('quiz-difficulty').value;
  var autoWords = getAutoQuizWords();
  var wordList = [];
  if (autoWords.length > 0) {
    for (var i = 0; i < autoWords.length; i++) wordList.push(autoWords[i].word);
  } else {
    for (var j = 0; j < Math.min(wordBank.length, 20); j++) wordList.push(wordBank[j].word);
  }
  var typeNames = { fill: '填空题', choice: '选择题', sort: '句子排序', cloze: '完形填空' };
  var diffDesc  = { easy: '简单（给中文提示）', medium: '中等（给词性提示）', hard: '困难（给首字母提示）' };
  var prompt = '给6-12岁孩子出 ' + qCount + ' 道英语' + (typeNames[qType] || '练习题') + '。\n';
  prompt += '目标单词（尽量使用）：' + wordList.join(', ') + '\n';
  prompt += '难度：' + (diffDesc[diff] || '') + '\n\n';
  if (qType === 'fill') {
    prompt += '题型：填空题（挖空用___表示）\n返回JSON数组，每题格式：{"type":"fill","sentence":"句子，挖空处用___表示","answer":"正确答案","hint":"提示","translation":"中文翻译"}\n';
  } else if (qType === 'choice') {
    prompt += '题型：选择题（4个选项选1个正确答案）\n返回JSON数组，每题格式：{"type":"choice","sentence":"句子，挖空处用___表示","answer":"正确答案","options":["A","B","C","D"],"hint":"提示","translation":"中文翻译"}\n注意：options是4个选项的数组，answer是其中一个选项。\n';
  } else if (qType === 'sort') {
    prompt += '题型：句子排序（把打乱的单词重新组成正确句子）\n返回JSON数组，每题格式：{"type":"sort","words":["word1","word2","word3"],"answer":"正确句子","hint":"提示","translation":"中文翻译"}\n注意：words是打乱顺序的单词数组，answer是正确句子（小写，空格分隔）。\n';
  } else if (qType === 'cloze') {
    prompt += '题型：完形填空（一段短文中挖空1-2个单词）\n返回JSON数组，每题格式：{"type":"cloze","text":"短文内容，挖空处用___表示","answer":"正确答案","hint":"提示","translation":"中文翻译"}\n';
  }
  prompt += '只返回JSON数组，不要用markdown或代码块包裹。';
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(prompt).then(function() {
      showToast('提示词已复制！请粘贴给 WorkBuddy');
      document.getElementById('quiz-paste-area').style.display = 'block';
    }).catch(function() { showToast('自动复制失败，请手动复制'); });
  } else { showToast('浏览器不支持自动复制'); }
});

function importQuiz() {
  var raw = (document.getElementById('quiz-paste-input').value || '').trim();
  if (!raw) { showToast('请先粘贴内容'); return; }
  var data = null;
  var jsonMatch = raw.match(/\[[\s\S]*\]/);
  if (jsonMatch) { try { data = JSON.parse(jsonMatch[0]); } catch(e) { showToast('JSON解析失败: ' + e.message); return; } }
  if (!data || !Array.isArray(data) || data.length === 0) { showToast('无法解析题目'); return; }
  quizData = data;
  quizAnswers = {};
  renderQuizQuestions();
  document.getElementById('quiz-questions').style.display = 'flex';
  document.getElementById('quiz-footer').style.display    = 'flex';
  document.getElementById('quiz-result').style.display    = 'none';
  document.getElementById('btn-retry-quiz').style.display = 'none';
  document.getElementById('btn-check-quiz').style.display = 'inline-flex';
  showToast('已导入 ' + data.length + ' 道题目！');
}

function clearQuizPaste() {
  document.getElementById('quiz-paste-input').value = '';
  document.getElementById('quiz-paste-area').style.display = 'none';
}

function renderQuizQuestions() {
  var container = document.getElementById('quiz-questions');
  if (!container) return;
  var html = '';
  for (var i = 0; i < quizData.length; i++) {
    var q = quizData[i];
    var type = q.type || 'fill';
    var typeName = { fill: '填空题', choice: '选择题', sort: '句子排序', cloze: '完形填空' };
    html += '<div class="quiz-card" style="background:white;border-radius:16px;padding:20px 24px;box-shadow:0 4px 20px rgba(91,141,238,0.12);border:1.5px solid #dfe6e9">'
      + '<div style="display:flex;align-items:center;gap:10px;margin-bottom:12px">'
      + '<div style="width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,#5b8dee,#a55eea);color:white;font-weight:800;font-size:0.9rem;display:flex;align-items:center;justify-content:center;flex-shrink:0">' + (i+1) + '</div>'
      + '<div style="font-size:0.85rem;color:#636e72">' + (typeName[type] || '练习题') + '</div>'
      + '</div>';
    if (type === 'fill' || type === 'cloze') {
      var text = q.sentence || q.text || '';
      html += '<div style="font-size:1.05rem;line-height:1.8;color:#2d3436;margin-bottom:8px">' + text.replace(/___+/g, '<input class="qi-input" data-index="' + i + '" style="width:120px;padding:4px 10px;font-size:1rem;border:2px solid #dfe6e9;border-radius:8px;text-align:center;font-family:inherit;display:inline-block;margin:0 4px" autocomplete="off">') + '</div>';
    } else if (type === 'choice') {
      html += '<div style="font-size:1.05rem;line-height:1.8;color:#2d3436;margin-bottom:12px">' + escHtml(q.sentence || '') + '</div>';
      html += '<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:8px;margin-bottom:8px" id="quiz-choice-' + i + '">';
      var opts = q.options || [];
      for (var c = 0; c < opts.length; c++) {
        html += '<button class="choice-btn" data-index="' + i + '" data-value="' + escHtml(opts[c]) + '" style="padding:10px 14px;border:2px solid #dfe6e9;border-radius:10px;background:white;cursor:pointer;font-size:0.95rem;font-family:inherit;text-align:left;transition:all 0.15s">'
          + '<strong>' + String.fromCharCode(65 + c) + '.</strong> ' + escHtml(opts[c]) + '</button>';
      }
      html += '</div>';
    } else if (type === 'sort') {
      var words = q.words || [];
      html += '<div style="margin-bottom:12px"><div style="font-size:0.85rem;color:#636e72;margin-bottom:8px">把下列单词排成正确顺序：</div>'
        + '<div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:10px">';
      for (var s = 0; s < words.length; s++) {
        html += '<span style="background:#f0f4ff;padding:6px 14px;border-radius:8px;font-weight:700;color:#5b8dee;font-size:1rem">' + escHtml(words[s]) + '</span>';
      }
      html += '</div>';
      html += '<input class="qi-input" data-index="' + i + '" type="text" placeholder="输入正确句子..." style="width:100%;padding:8px 14px;border:2px solid #dfe6e9;border-radius:8px;font-size:1rem;font-family:inherit"></div>';
    }
    if (q.hint) {
      html += '<div style="font-size:0.85rem;color:#636e72;margin-top:8px;font-style:italic">提示：' + escHtml(q.hint) + '</div>';
    }
    html += '<div id="quiz-answer-' + i + '" style="margin-top:8px;font-size:0.88rem;color:#26de81;font-weight:600;display:none">答案：<strong>' + escHtml(q.answer) + '</strong> - ' + escHtml(q.translation || '') + '</div>';
    html += '</div>';
  }
  container.innerHTML = html;
  container.querySelectorAll('.qi-input').forEach(function(input) {
    input.addEventListener('input', function() { quizAnswers[input.dataset.index] = (input.value || '').trim(); });
  });
  container.querySelectorAll('.choice-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var idx = btn.dataset.index;
      var parent = btn.parentElement;
      parent.querySelectorAll('.choice-btn').forEach(function(b) { b.style.borderColor = '#dfe6e9'; b.style.background = 'white'; });
      btn.style.borderColor = '#5b8dee'; btn.style.background = '#eef3ff';
      quizAnswers[idx] = btn.dataset.value;
    });
  });
}

function checkQuiz() {
  var correct = 0;
  for (var i = 0; i < quizData.length; i++) {
    var q = quizData[i];
    var userAnswer = (quizAnswers[i] || '').toString().trim().toLowerCase();
    var correctAnswer = (q.answer || '').toString().trim().toLowerCase();
    var isCorrect = (userAnswer === correctAnswer);
    var relatedWord = null;
    for (var k = 0; k < wordBank.length; k++) {
      if (wordBank[k].word.toLowerCase() === correctAnswer) { relatedWord = wordBank[k]; break; }
    }
    if (relatedWord) {
      saveQuizLog({ date: todayStr(), wordId: relatedWord.id, word: relatedWord.word, correct: isCorrect });
      if (isCorrect) { markWordCorrect(relatedWord.id); } else { markWordWrong(relatedWord.id); }
    }
    if (q.type === 'choice') {
      var btns = document.querySelectorAll('#quiz-choice-' + i + ' .choice-btn');
      btns.forEach(function(btn) {
        var val = btn.dataset.value.toLowerCase();
        if (val === correctAnswer) { btn.classList.add('correct'); }
        else if (val === userAnswer && !isCorrect) { btn.classList.add('wrong'); }
        btn.disabled = true;
      });
    } else {
      var input = document.querySelector('.qi-input[data-index="' + i + '"]');
      if (input) {
        input.style.borderColor = isCorrect ? '#26de81' : '#ff5e57';
        input.style.background   = isCorrect ? '#e8fff3' : '#fff0f0';
        input.disabled = true;
      }
    }
    var answerEl = document.getElementById('quiz-answer-' + i);
    if (answerEl) answerEl.style.display = 'block';
    if (isCorrect) correct++;
  }
  var total   = quizData.length;
  var percent = total > 0 ? Math.round(correct / total * 100) : 0;
  var emoji  = percent >= 90 ? '?=': percent >= 70 ? '::': percent >= 50 ? '::': '::';
  var msg    = percent >= 90 ? '太棒了！满分高手！' : percent >= 70 ? '很不错！继续努力！' : percent >= 50 ? '还不错，多练几遍！' : '继续加油，你能行！';
  var resultEl = document.getElementById('quiz-result');
  if (resultEl) {
    resultEl.innerHTML = '<div style="font-size:3rem;font-weight:900;color:#5b8dee">' + correct + ' / ' + total + '</div>'
      + '<div style="font-size:1.1rem;margin-top:8px;color:#636e72">' + msg + '</div>'
      + '<div style="margin-top:12px;font-size:0.9rem;color:#636e72">正确率 ' + percent + '%</div>';
    resultEl.style.display = 'block';
  }
  document.getElementById('btn-check-quiz').style.display  = 'none';
  document.getElementById('btn-retry-quiz').style.display  = 'inline-flex';
  if (resultEl) resultEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function retryQuiz() {
  renderQuizQuestions();
  document.getElementById('quiz-result').style.display    = 'none';
  document.getElementById('btn-check-quiz').style.display  = 'inline-flex';
  document.getElementById('btn-retry-quiz').style.display  = 'none';
}

/* ========== Init ========== */
var sampleWords = [
  { word: 'adventure', zh: '冒险', phonetic: '/adventur/' },
  { word: 'explore',   zh: '探索', phonetic: '/iksplor/' },
  { word: 'discover',  zh: '发现', phonetic: '/diskver/' },
  { word: 'brave',     zh: '勇敢的', phonetic: '/breiv/' },
  { word: 'magical',   zh: '神奇的', phonetic: '/maedikl/' },
  { word: 'ancient',   zh: '古老的', phonetic: '/einnt/' },
  { word: 'treasure',  zh: '宝藏', phonetic: '/te'r/' },
  { word: 'journey',   zh: '旅程', phonetic: '/d'rni/' }
];

function init() {
  loadWords();
  loadStory();
  if (wordBank.length === 0) {
    var today = todayStr();
    for (var i = 0; i < sampleWords.length; i++) {
      var s = sampleWords[i];
      wordBank.push({
        id: Date.now() + Math.random(),
        word: s.word, zh: s.zh, phonetic: s.phonetic,
        definitions: [], examples: [], etymology: '',
        addDate: today,
        reviewPlan: buildReviewPlan(today),
        wrongCount: 0, lastWrong: '', mastered: false
      });
    }
    saveWords();
  }
  renderWordBank();
  if (lastStory) tryShowSavedStory();
  if ('speechSynthesis' in window) {
    window.speechSynthesis.getVoices();
  }
}

init();
"""

base = r"c:/Users/KK/WorkBuddy/20260504010031/english-words/"

# Write HTML
with open(base + "index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
print("HTML written")

# Write JS  
with open(base + "app.js", "w", encoding="utf-8") as f:
    f.write(js_content)
print("JS written")

print("Done!")
