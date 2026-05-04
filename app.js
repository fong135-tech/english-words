/* 英语单词乐园 v2.0 */
var STORAGE_KEY = 'wordpal_words';
var STORY_KEY   = 'wordpal_story';
var wordBank   = [];
var lastStory  = '';
var lastStoryTitle = '';
var lastStoryWords = [];
var quizData   = [];
var currentWeekOffset = 0;
var REVIEW_INTERVALS = [1, 3, 7, 14, 30];

/* ========== 工具函数 ========== */
function formatDate(d) {
  var y = d.getFullYear();
  var m = ('0' + (d.getMonth() + 1)).slice(-2);
  var day = ('0' + d.getDate()).slice(-2);
  return y + '-' + m + '-' + day;
}
function todayStr() { return formatDate(new Date()); }
function escHtml(s) {
  if (!s) return '';
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

/* ========== 存储 ========== */
function saveWords() {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(wordBank)); } catch(e) {}
}
function loadWords() {
  try { var d = localStorage.getItem(STORAGE_KEY); if (d) wordBank = JSON.parse(d); } catch(e) {}
}
function saveStory() {
  try { localStorage.setItem(STORY_KEY, JSON.stringify({title:lastStoryTitle, words:lastStoryWords, text:lastStory})); } catch(e) {}
}
function loadStory() {
  try {
    var d = localStorage.getItem(STORY_KEY);
    if (d) { var o = JSON.parse(d); lastStoryTitle = o.title||''; lastStoryWords = o.words||[]; lastStory = o.text||''; }
  } catch(e) {}
}

/* ========== 发音 ========== */
function speakText(text) {
  if (!('speechSynthesis' in window)) return;
  window.speechSynthesis.cancel();
  var u = new SpeechSynthesisUtterance(text);
  u.lang = 'en-US';
  u.rate = 0.9;
  window.speechSynthesis.speak(u);
}

/* ========== 记忆曲线 ========== */
function buildReviewPlan(addDateStr) {
  var d = new Date(addDateStr);
  var plan = [];
  for (var i = 0; i < REVIEW_INTERVALS.length; i++) {
    var r = new Date(d);
    r.setDate(r.getDate() + REVIEW_INTERVALS[i]);
    plan.push(formatDate(r));
  }
  return plan;
}
function getWeekRange(offset) {
  var now = new Date(); now.setDate(now.getDate() + offset * 7);
  var day = now.getDay();
  var diff = now.getDate() - day + (day === 0 ? -6 : 1);
  var mon = new Date(now); mon.setDate(diff);
  var sun = new Date(mon); sun.setDate(sun.getDate() + 6);
  return { start: formatDate(mon), end: formatDate(sun) };
}
function getWeekLabel(offset) {
  var r = getWeekRange(offset);
  function mf(s) { var p = s.slice(5).split('-'); return p[0]+'月'+p[1]+'日'; }
  var s = mf(r.start), e = mf(r.end);
  if (offset === 0) return '本周 ' + s + ' - ' + e;
  if (offset === -1) return '上周 ' + s + ' - ' + e;
  if (offset === 1) return '下周 ' + s + ' - ' + e;
  return s + ' - ' + e;
}
function isInWeek(dateStr, offset) {
  var r = getWeekRange(offset);
  return dateStr >= r.start && dateStr <= r.end;
}
function needsReview(word) {
  if (word.mastered) return false;
  var today = todayStr();
  if (!word.reviewPlan) return false;
  for (var i = 0; i < word.reviewPlan.length; i++) {
    if (word.reviewPlan[i] === today) return true;
  }
  return false;
}

/* ========== Toast ========== */
var toastTimer = null;
function showToast(msg) {
  var t = document.getElementById('toast');
  if (!t) return;
  t.textContent = msg;
  t.style.opacity = '1';
  clearTimeout(toastTimer);
  toastTimer = setTimeout(function() { t.style.opacity = '0'; }, 2800);
}

/* ========== 导航 ========== */
function setupNav() {
  var btns = document.querySelectorAll('.nav-btn');
  for (var i = 0; i < btns.length; i++) {
    (function(btn) {
      btn.addEventListener('click', function() {
        var page = btn.getAttribute('data-page');
        var pages = document.querySelectorAll('.page');
        for (var j = 0; j < pages.length; j++) pages[j].classList.remove('active');
        var target = document.getElementById('page-' + page);
        if (target) target.classList.add('active');
        for (var k = 0; k < btns.length; k++) btns[k].classList.remove('active');
        btn.classList.add('active');
        if (page === 'wordbank') renderWordBank();
        if (page === 'learn') renderLearnList();
        if (page === 'story') renderStoryCheckboxes();
        if (page === 'quiz') setupQuizPage();
      });
    })(btns[i]);
  }
}

/* ========== 单词库 ========== */
function renderWordBank() {
  var grid = document.getElementById('wordbank-grid');
  var empty = document.getElementById('wordbank-empty');
  if (!grid) return;
  var words = [];
  for (var i = 0; i < wordBank.length; i++) {
    if (isInWeek(wordBank[i].addDate, currentWeekOffset)) words.push(wordBank[i]);
  }
  var label = document.getElementById('wordbank-week-label');
  if (label) label.textContent = getWeekLabel(currentWeekOffset);
  if (words.length === 0) {
    grid.innerHTML = '';
    if (empty) empty.style.display = 'block';
    return;
  }
  if (empty) empty.style.display = 'none';
  var html = '';
  for (var j = 0; j < words.length; j++) {
    var w = words[j];
    html += '<div class="wb-card">'
      + '<button class="wb-del" onclick="deleteWord(' + w.id + ')">X</button>'
      + '<div class="wb-en">' + escHtml(w.word) + '</div>'
      + (w.phonetic ? '<div class="wb-phonetic">' + escHtml(w.phonetic) + '</div>' : '')
      + '<div class="wb-zh">' + escHtml(w.zh) + '</div>'
      + '<div class="wb-actions">'
      + '<button class="btn btn-sm btn-secondary" onclick="editWord(' + w.id + ')">编辑</button>'
      + '<button class="btn btn-sm btn-primary" onclick="speakText(\'' + escHtml(w.word).replace(/'/g, "\\'") + '\')">发音</button>'
      + '</div></div>';
  }
  grid.innerHTML = html;
}
function weekNavigate(d) { currentWeekOffset += d; renderWordBank(); }
function addWord() {
  var input = document.getElementById('input-word');
  if (!input) return;
  var val = input.value.trim();
  if (!val) { showToast('请输入单词'); return; }
  var exists = false;
  for (var i = 0; i < wordBank.length; i++) {
    if (wordBank[i].word.toLowerCase() === val.toLowerCase()) { exists = true; break; }
  }
  if (exists) { showToast('单词已存在'); return; }
  var today = todayStr();
  wordBank.push({ id: Date.now(), word: val, zh:'', phonetic:'', definitions:[], examples:[], etymology:'', addDate:today, reviewPlan:buildReviewPlan(today), wrongCount:0, lastWrong:'', mastered:false });
  saveWords(); input.value = ''; renderWordBank(); showToast('添加成功');
}
function deleteWord(id) {
  wordBank = wordBank.filter(function(w) { return w.id !== id; });
  saveWords(); renderWordBank(); showToast('已删除');
}
var currentEditWordId = null;
function editWord(id) {
  var w = null;
  for (var i = 0; i < wordBank.length; i++) { if (wordBank[i].id === id) { w = wordBank[i]; break; } }
  if (!w) return;
  currentEditWordId = id;
  var form = document.getElementById('word-edit-form');
  if (!form) return;
  form.innerHTML = '<div style="margin-bottom:12px"><label>中文</label><br><input id="edit-zh" style="width:100%" value="' + escHtml(w.zh) + '"></div>'
    + '<div style="margin-bottom:12px"><label>音标</label><br><input id="edit-phonetic" style="width:100%" value="' + escHtml(w.phonetic) + '"></div>'
    + '<div style="margin-bottom:12px"><label>已掌握</label> <input id="edit-mastered" type="checkbox" ' + (w.mastered?'checked':'') + '></div>';
  var modal = document.getElementById('modal-word-edit');
  if (modal) modal.classList.add('show');
}
function saveWordEdit() {
  var w = null;
  for (var i = 0; i < wordBank.length; i++) { if (wordBank[i].id === currentEditWordId) { w = wordBank[i]; break; } }
  if (!w) return;
  var zhEl = document.getElementById('edit-zh');
  var phEl = document.getElementById('edit-phonetic');
  var mEl = document.getElementById('edit-mastered');
  if (zhEl) w.zh = zhEl.value.trim();
  if (phEl) w.phonetic = phEl.value.trim();
  if (mEl) w.mastered = mEl.checked;
  saveWords(); closeWordEdit(); renderWordBank(); showToast('保存成功');
}
function closeWordEdit() {
  var modal = document.getElementById('modal-word-edit');
  if (modal) modal.classList.remove('show');
  currentEditWordId = null;
}
function batchAddWords() {
  var ta = document.getElementById('input-batch');
  if (!ta) return;
  var lines = ta.value.split('\n');
  var added = 0;
  for (var i = 0; i < lines.length; i++) {
    var val = lines[i].trim();
    if (!val) continue;
    var exists = false;
    for (var j = 0; j < wordBank.length; j++) {
      if (wordBank[j].word.toLowerCase() === val.toLowerCase()) { exists = true; break; }
    }
    if (!exists) {
      var today = todayStr();
      wordBank.push({ id:Date.now()+Math.random(), word:val, zh:'', phonetic:'', definitions:[], examples:[], etymology:'', addDate:today, reviewPlan:buildReviewPlan(today), wrongCount:0, lastWrong:'', mastered:false });
      added++;
    }
  }
  saveWords(); ta.value = ''; renderWordBank(); showToast('批量添加 ' + added + ' 个');
}

/* ========== 学习页面 ========== */
function renderLearnList() {
  var list = document.getElementById('learn-word-list');
  if (!list) return;
  var searchEl = document.getElementById('learn-search');
  var search = searchEl ? searchEl.value.trim().toLowerCase() : '';
  var words = wordBank.slice();
  if (search) words = words.filter(function(w) { return w.word.toLowerCase().indexOf(search) !== -1; });
  words.sort(function(a,b) { return a.word.toLowerCase() < b.word.toLowerCase() ? -1 : 1; });
  var html = '';
  for (var i = 0; i < words.length; i++) {
    var w = words[i];
    html += '<div class="learn-card" onclick="showWordDetail(' + w.id + ')">'
      + '<div style="font-size:1.3rem;font-weight:800">' + escHtml(w.word) + '</div>'
      + (w.phonetic ? '<div style="color:#5b8dee;margin-top:4px">' + escHtml(w.phonetic) + '</div>' : '')
      + (w.zh ? '<div style="color:#636e72;margin-top:6px">' + escHtml(w.zh) + '</div>' : '')
      + '</div>';
  }
  list.innerHTML = html || '<p style="color:#636e72;text-align:center;padding:40px">暂无单词</p>';
}
function showWordDetail(id) {
  var w = null;
  for (var i = 0; i < wordBank.length; i++) { if (wordBank[i].id === id) { w = wordBank[i]; break; } }
  if (!w) return;
  var content = document.getElementById('word-detail-content');
  if (!content) return;
  var defs = (w.definitions||[]).map(function(d){return '<li>'+escHtml(d)+'</li>'}).join('');
  var exs = (w.examples||[]).map(function(e){return '<li>'+escHtml(e)+'</li>'}).join('');
  content.innerHTML = '<div style="display:flex;align-items:center;gap:12px;margin-bottom:16px">'
    + '<div style="font-size:2rem;font-weight:900">' + escHtml(w.word) + '</div>'
    + '<button class="btn btn-sm btn-primary" onclick="speakText(\'' + escHtml(w.word).replace(/'/g, "\\'") + '\')">发音</button></div>'
    + (w.phonetic ? '<div style="color:#5b8dee;margin-bottom:12px">' + escHtml(w.phonetic) + '</div>' : '')
    + (w.zh ? '<div style="margin-bottom:12px">中文：' + escHtml(w.zh) + '</div>' : '')
    + (defs ? '<div><h4>定义</h4><ul>'+defs+'</ul></div>' : '')
    + (exs ? '<div><h4>例句</h4><ul>'+exs+'</ul></div>' : '');
  var modal = document.getElementById('modal-word-detail');
  if (modal) modal.classList.add('show');
}
function closeWordDetail() {
  var modal = document.getElementById('modal-word-detail');
  if (modal) modal.classList.remove('show');
}

/* ========== 故事页面 ========== */
function renderStoryCheckboxes() {
  var c = document.getElementById('story-word-checkboxes');
  if (!c) return;
  var html = '';
  var recommended = [];
  var others = [];
  for (var i = 0; i < wordBank.length; i++) {
    var w = wordBank[i];
    if (isInWeek(w.addDate,0) || needsReview(w) || w.wrongCount > 0) recommended.push(w);
    else others.push(w);
  }
  if (recommended.length > 0) {
    html += '<div style="font-weight:700;color:#5b8dee;margin-bottom:6px">推荐单词</div>';
    for (var j = 0; j < recommended.length; j++) {
      var w = recommended[j];
      html += '<label style="display:flex;gap:8px;padding:6px 10px;border:1px solid #e8ecff;border-radius:8px">'
        + '<input type="checkbox" value="' + escHtml(w.word) + '" checked>'
        + '<span><b>' + escHtml(w.word) + '</b> ' + (w.zh?'<span style="color:#636e72">('+escHtml(w.zh)+')</span>':'') + '</span></label>';
    }
  }
  html += '<div style="font-weight:700;color:#636e72;margin:12px 0 6px">其他单词</div>';
  for (var k = 0; k < others.length; k++) {
    var w2 = others[k];
    html += '<label style="display:flex;gap:8px;padding:6px 10px;border:1px solid #e8ecff;border-radius:8px">'
      + '<input type="checkbox" value="' + escHtml(w2.word) + '">'
      + '<span><b>' + escHtml(w2.word) + '</b></span></label>';
  }
  c.innerHTML = html;
  updateStoryCount();
}
function updateStoryCount() {
  var cbs = document.querySelectorAll('#story-word-checkboxes input[type="checkbox"]');
  var n = 0; for (var i = 0; i < cbs.length; i++) { if (cbs[i].checked) n++; }
  var el = document.getElementById('story-count');
  if (el) el.textContent = n;
}
function getSelectedWords() {
  var cbs = document.querySelectorAll('#story-word-checkboxes input[type="checkbox"]');
  var words = []; for (var i = 0; i < cbs.length; i++) { if (cbs[i].checked) words.push(cbs[i].value); }
  return words;
}
function copyStoryPrompt() {
  var words = getSelectedWords();
  if (words.length === 0) { showToast('请选择单词'); return; }
  var styleEl = document.getElementById('story-style');
  var lenEl = document.getElementById('story-length');
  var style = styleEl ? styleEl.value : 'adventure';
  var length = lenEl ? lenEl.value : 'medium';
  var sMap = {adventure:'冒险',fairy:'童话',funny:'搞笑',science:'科学',daily:'日常'};
  var lMap = {short:'100',medium:'200',long:'300'};
  var prompt = '请用英语写一个' + (sMap[style]||'冒险') + '故事，约' + (lMap[length]||'200') + '词。\n'
    + '使用以下单词（用**word**标记）：\n' + words.join('、') + '\n\n'
    + 'JSON格式：{"title":"标题","text":"正文","words":["word1","word2"]}';
  if (navigator.clipboard) {
    navigator.clipboard.writeText(prompt).then(function() { showToast('提示词已复制'); var pa = document.getElementById('story-paste-area'); if (pa) pa.style.display = 'block'; });
  }
}
function importStory() {
  var input = document.getElementById('story-paste-input');
  if (!input) return;
  var text = input.value.trim();
  if (!text) { showToast('请粘贴AI回复'); return; }
  try {
    var data = JSON.parse(text);
    lastStoryTitle = data.title || '';
    lastStory = data.text || '';
    lastStoryWords = data.words || [];
    saveStory();
    showStoryOutput();
    showToast('故事导入成功');
  } catch(e) { showToast('JSON格式错误'); }
}
function showStoryOutput() {
  var ph = document.getElementById('story-placeholder');
  var out = document.getElementById('story-output');
  var pa = document.getElementById('story-paste-area');
  if (ph) ph.style.display = 'none';
  if (pa) pa.style.display = 'none';
  if (out) out.style.display = 'block';
  var titleEl = document.getElementById('story-title');
  if (titleEl) titleEl.textContent = lastStoryTitle;
  var textEl = document.getElementById('story-text');
  if (textEl) {
    var html = escHtml(lastStory).replace(/\*\*(.*?)\*\*/g, '<mark>$1</mark>');
    textEl.innerHTML = html;
  }
  var wordsEl = document.getElementById('story-used-words');
  if (wordsEl) {
    var h = '';
    for (var i = 0; i < lastStoryWords.length; i++) h += '<span style="background:#f0f4ff;padding:3px 10px;border-radius:8px;font-size:0.85rem">' + escHtml(lastStoryWords[i]) + '</span>';
    wordsEl.innerHTML = h;
  }
}
function readStory() { if (lastStory) speakText(lastStory.replace(/\*\*(.*?)\*\*/g, '$1')); }
function editStory() {
  var pa = document.getElementById('story-paste-area');
  var out = document.getElementById('story-output');
  if (pa) pa.style.display = 'block';
  if (out) out.style.display = 'none';
  var input = document.getElementById('story-paste-input');
  if (input) input.value = JSON.stringify({title:lastStoryTitle,text:lastStory,words:lastStoryWords}, null, 2);
}
function clearStoryPaste() { var input = document.getElementById('story-paste-input'); if (input) input.value = ''; }
function tryShowSavedStory() { if (lastStory) showStoryOutput(); }

/* ========== 测验页面 ========== */
function setupQuizPage() {
  var q = document.getElementById('quiz-questions'); if (q) q.innerHTML = '';
  var r = document.getElementById('quiz-result'); if (r) r.style.display = 'none';
  var f = document.getElementById('quiz-footer'); if (f) f.style.display = 'none';
  var pa = document.getElementById('quiz-paste-area'); if (pa) pa.style.display = 'none';
  var hint = document.getElementById('quiz-auto-hint');
  if (hint) {
    var rec = [];
    for (var i = 0; i < wordBank.length; i++) {
      var w = wordBank[i];
      if (isInWeek(w.addDate,0) || needsReview(w) || w.wrongCount > 0) rec.push(w.word);
    }
    if (rec.length > 0) { hint.textContent = '推荐单词：' + rec.join('、'); hint.style.display = 'block'; }
    else hint.style.display = 'none';
  }
}
function copyQuizPrompt() {
  var typeEl = document.getElementById('quiz-type');
  var countEl = document.getElementById('quiz-count');
  var diffEl = document.getElementById('quiz-difficulty');
  var type = typeEl ? typeEl.value : 'fill';
  var count = countEl ? parseInt(countEl.value) : 8;
  var diff = diffEl ? diffEl.value : 'medium';
  var words = [];
  for (var i = 0; i < wordBank.length; i++) {
    var w = wordBank[i];
    if (isInWeek(w.addDate,0) || needsReview(w) || w.wrongCount > 0) words.push(w.word);
  }
  if (words.length === 0) words = wordBank.slice(0, count).map(function(w){return w.word});
  var tMap = {fill:'填空题',choice:'选择题',sort:'排序题',cloze:'完形填空'};
  var prompt = '生成' + count + '道英语' + (tMap[type]||'填空题') + '。\n难度：' + diff + '。\n单词：' + words.join('、') + '\n\nJSON数组格式：[{"type":"' + type + '","question":"题目","answer":"答案","options":["A","B","C","D"],"hint":""},...]';
  if (navigator.clipboard) {
    navigator.clipboard.writeText(prompt).then(function() { showToast('提示词已复制'); var pa = document.getElementById('quiz-paste-area'); if (pa) pa.style.display = 'block'; });
  }
}
function importQuiz() {
  var input = document.getElementById('quiz-paste-input');
  if (!input) return;
  var text = input.value.trim();
  if (!text) { showToast('请粘贴AI回复'); return; }
  try {
    quizData = JSON.parse(text);
    renderQuizQuestions();
    showToast('导入成功，共' + quizData.length + '题');
  } catch(e) { showToast('JSON格式错误'); }
}
function renderQuizQuestions() {
  var container = document.getElementById('quiz-questions');
  if (!container) return;
  quizAnswers = {};
  var html = '';
  for (var i = 0; i < quizData.length; i++) {
    var q = quizData[i];
    var typeName = q.type==='fill'?'填空':q.type==='choice'?'选择':q.type==='sort'?'排序':'完形';
    html += '<div class="quiz-card card" style="margin-bottom:16px"><div style="font-weight:700;margin-bottom:10px">第' + (i+1) + '题（' + typeName + '）</div>'
      + '<div style="margin-bottom:12px">' + escHtml(q.question) + '</div>';
    if (q.type === 'choice' && q.options) {
      html += '<div style="display:flex;flex-direction:column;gap:8px">';
      for (var j = 0; j < q.options.length; j++) {
        html += '<button class="choice-btn" style="padding:8px 14px;border:1.5px solid #dfe6e9;border-radius:10px;background:white;cursor:pointer;text-align:left;font-family:inherit;font-size:0.92rem" onclick="selectChoice(' + i + ',' + j + ',this)">' + String.fromCharCode(65+j) + '. ' + escHtml(q.options[j]) + '</button>';
      }
      html += '</div>';
    } else {
      html += '<input type="text" id="quiz-ans-' + i + '" style="width:100%;padding:10px 14px;border:1.5px solid #dfe6e9;border-radius:10px;font-size:0.92rem" placeholder="输入答案">';
    }
    if (q.hint) html += '<div style="font-size:0.82rem;color:#b2bec3;margin-top:8px">提示：' + escHtml(q.hint) + '</div>';
    html += '</div>';
  }
  container.innerHTML = html;
  var footer = document.getElementById('quiz-footer');
  if (footer) footer.style.display = 'flex';
  var checkBtn = document.getElementById('btn-check-quiz');
  if (checkBtn) checkBtn.style.display = 'inline-flex';
  var retryBtn = document.getElementById('btn-retry-quiz');
  if (retryBtn) retryBtn.style.display = 'none';
}
var quizAnswers = {};
function selectChoice(qIdx, optIdx, btnEl) {
  quizAnswers[qIdx] = optIdx;
  var card = btnEl.parentElement;
  var btns = card.querySelectorAll('.choice-btn');
  for (var i = 0; i < btns.length; i++) { btns[i].style.borderColor='#dfe6e9'; btns[i].style.background='white'; }
  btnEl.style.borderColor = '#5b8dee'; btnEl.style.background = '#f0f4ff';
}
function checkQuiz() {
  var correct = 0;
  for (var i = 0; i < quizData.length; i++) {
    var q = quizData[i];
    var isCorrect = false;
    if (q.type === 'choice') {
      isCorrect = quizAnswers[i] !== undefined && String(quizAnswers[i]) === String(q.answer);
    } else {
      var input = document.getElementById('quiz-ans-' + i);
      var userAns = input ? input.value.trim().toLowerCase() : '';
      isCorrect = userAns === String(q.answer).trim().toLowerCase();
    }
    if (isCorrect) correct++;
    else {
      var ansWord = q.answer;
      for (var j = 0; j < wordBank.length; j++) {
        if (wordBank[j].word.toLowerCase() === ansWord.toLowerCase()) {
          wordBank[j].wrongCount = (wordBank[j].wrongCount||0) + 1;
          wordBank[j].lastWrong = todayStr();
          break;
        }
      }
    }
  }
  saveWords();
  var total = quizData.length;
  var percent = total > 0 ? Math.round(correct/total*100) : 0;
  var msg = percent >= 90 ? '太棒了！' : percent >= 70 ? '很不错！' : percent >= 50 ? '还不错！' : '继续加油！';
  var resultEl = document.getElementById('quiz-result');
  if (resultEl) {
    resultEl.innerHTML = '<div style="font-size:3rem;font-weight:900;color:#5b8dee">' + correct + '/' + total + '</div>'
      + '<div style="margin-top:8px;color:#636e72">' + msg + '</div>'
      + '<div style="margin-top:12px;font-size:0.9rem;color:#636e72">正确率 ' + percent + '%</div>';
    resultEl.style.display = 'block';
  }
  var checkBtn = document.getElementById('btn-check-quiz');
  if (checkBtn) checkBtn.style.display = 'none';
  var retryBtn = document.getElementById('btn-retry-quiz');
  if (retryBtn) retryBtn.style.display = 'inline-flex';
}
function retryQuiz() {
  renderQuizQuestions();
  var r = document.getElementById('quiz-result'); if (r) r.style.display = 'none';
  var c = document.getElementById('btn-check-quiz'); if (c) c.style.display = 'inline-flex';
  var rt = document.getElementById('btn-retry-quiz'); if (rt) rt.style.display = 'none';
}
function clearQuizPaste() { var input = document.getElementById('quiz-paste-input'); if (input) input.value = ''; }

/* ========== 事件绑定 ========== */
function setupWordBankEvents() {
  var btnAdd = document.getElementById('btn-add-word');
  if (btnAdd) btnAdd.addEventListener('click', addWord);
  var btnBatch = document.getElementById('btn-batch-add');
  if (btnBatch) btnBatch.addEventListener('click', batchAddWords);
  var input = document.getElementById('input-word');
  if (input) input.addEventListener('keydown', function(e) { if (e.key === 'Enter') addWord(); });
}
function setupLearnSearch() {
  var search = document.getElementById('learn-search');
  if (search) search.addEventListener('input', renderLearnList);
}
function setupStoryEvents() {
  var btn = document.getElementById('btn-copy-story-prompt');
  if (btn) btn.addEventListener('click', copyStoryPrompt);
  var cbs = document.querySelectorAll('#story-word-checkboxes input[type="checkbox"]');
  for (var i = 0; i < cbs.length; i++) {
    (function(cb) { cb.addEventListener('change', updateStoryCount); })(cbs[i]);
  }
}
function setupQuizEvents() {
  var btn = document.getElementById('btn-copy-quiz-prompt');
  if (btn) btn.addEventListener('click', copyQuizPrompt);
}

/* ========== Init ========== */
var sampleWords = [
  {word:'adventure',zh:'冒险',phonetic:'/adˈventʃər/'},
  {word:'explore',zh:'探索',phonetic:'/ɪkˈsplɔːr/'},
  {word:'discover',zh:'发现',phonetic:'/dɪˈskʌvər/'},
  {word:'brave',zh:'勇敢的',phonetic:'/breɪv/'},
  {word:'magical',zh:'神奇的',phonetic:'/ˈmædʒɪkəl/'},
  {word:'ancient',zh:'古老的',phonetic:'/ˈeɪnʃənt/'},
  {word:'treasure',zh:'宝藏',phonetic:'/ˈtreʒər/'},
  {word:'journey',zh:'旅程',phonetic:'/ˈdʒɜːrni/'}
];
function init() {
  loadWords();
  loadStory();
  if (wordBank.length === 0) {
    var today = todayStr();
    for (var i = 0; i < sampleWords.length; i++) {
      var s = sampleWords[i];
      wordBank.push({ id:Date.now()+Math.random(), word:s.word, zh:s.zh, phonetic:s.phonetic, definitions:[], examples:[], etymology:'', addDate:today, reviewPlan:buildReviewPlan(today), wrongCount:0, lastWrong:'', mastered:false });
    }
    saveWords();
  }
  setupNav();
  setupWordBankEvents();
  setupLearnSearch();
  setupStoryEvents();
  setupQuizEvents();
  renderWordBank();
  tryShowSavedStory();
  if ('speechSynthesis' in window) window.speechSynthesis.getVoices();
}
init();