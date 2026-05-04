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
  // Also read zh and phonetic from input fields
  var zhInput = document.getElementById('input-zh');
  var phInput = document.getElementById('input-phonetic');
  var zhVal = zhInput ? zhInput.value.trim() : '';
  var phVal = phInput ? phInput.value.trim() : '';
  var today = todayStr();
  wordBank.push({ id: Date.now(), word: val, zh: zhVal, phonetic: phVal, definitions:[], examples:[], etymology:'', addDate:today, reviewPlan:buildReviewPlan(today), wrongCount:0, lastWrong:'', mastered:false });
  saveWords();
  input.value = '';
  if (zhInput) zhInput.value = '';
  if (phInput) phInput.value = '';
  var lr = document.getElementById('lookup-result');
  if (lr) lr.style.display = 'none';
  renderWordBank(); showToast('添加成功');
}
function lookupWord() {
  var input = document.getElementById('input-word');
  if (!input) return;
  var word = input.value.trim();
  if (!word) { showToast('请先输入单词'); return; }
  var resultEl = document.getElementById('lookup-result');
  if (resultEl) { resultEl.style.display = 'block'; resultEl.innerHTML = '查询中...'; }
  fetch('https://api.dictionaryapi.dev/api/v2/entries/en/' + encodeURIComponent(word))
    .then(function(r) { return r.json(); })
    .then(function(data) {
      if (!data || (Array.isArray(data) && data[0] && data[0].title === 'No Definitions Found') || (data.title === 'No Definitions Found')) {
        if (resultEl) resultEl.innerHTML = '<span style="color:#ff5e57">未找到该单词，请手动输入意思。</span>';
        return;
      }
      var entry = Array.isArray(data) ? data[0] : data;
      var html = '';
      // Phonetic
      var phonetic = entry.phonetic || '';
      if (entry.phonetics) {
        for (var p = 0; p < entry.phonetics.length; p++) {
          if (entry.phonetics[p].text) { phonetic = entry.phonetics[p].text; break; }
        }
      }
      if (phonetic) {
        var phEl = document.getElementById('input-phonetic');
        if (phEl) phEl.value = phonetic;
        html += '<div style="color:#5b8dee;font-weight:600;margin-bottom:4px">/' + escHtml(phonetic) + '/</div>';
      }
      // Short English definition (just first one)
      if (entry.meanings && entry.meanings.length > 0) {
        var firstMeaning = entry.meanings[0];
        var pos = firstMeaning.partOfSpeech || '';
        if (firstMeaning.definitions && firstMeaning.definitions.length > 0) {
          var shortDef = firstMeaning.definitions[0].definition || '';
          // Keep it short
          if (shortDef.length > 60) shortDef = shortDef.substring(0, 60) + '...';
          html += '<div style="color:#636e72;font-size:0.85rem">' + escHtml(pos) + ' ' + escHtml(shortDef) + '</div>';
        }
      }
      if (resultEl) resultEl.innerHTML = html;
      // Translate word to Chinese
      translateToChinese(word, entry);
    })
    .catch(function(e) {
      if (resultEl) resultEl.innerHTML = '<span style="color:#ff5e57">查询失败，请手动输入意思。</span>';
    });
}
function translateToChinese(word, entry) {
  // Only translate the word itself, not the definition
  fetch('https://api.mymemory.translated.net/get?q=' + encodeURIComponent(word) + '&langpair=en|zh-CN')
    .then(function(r) { return r.json(); })
    .then(function(data) {
      if (data && data.responseData && data.responseData.translatedText) {
        var zhTranslation = data.responseData.translatedText;
        // Clean up: remove trailing punctuation, keep it short
        zhTranslation = zhTranslation.replace(/[，。！？、；：""''（）\[\]{}]/g, ' ').trim();
        // Take only the first part if multiple meanings separated by comma
        var shortZh = zhTranslation.split(/[,，;；]/)[0].trim();
        if (shortZh.length > 20) shortZh = shortZh.substring(0, 20);
        var zhEl = document.getElementById('input-zh');
        if (zhEl && !zhEl.value) {
          zhEl.value = shortZh;
          var resultEl = document.getElementById('lookup-result');
          if (resultEl) resultEl.innerHTML += '<div style="margin-top:8px;color:#26de81"><strong>中文:</strong> ' + escHtml(shortZh) + '</div>';
        }
      }
    })
    .catch(function(e) { /* ignore translation error */ });
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
  var sMap = {adventure:'adventure',fairy:'fairy tale',funny:'funny',science:'science fiction',daily:'daily life'};
  var lMap = {short:'100',medium:'200',long:'300'};
  var prompt = 'Write an English ' + (sMap[style]||'adventure') + ' story using about ' + (lMap[length]||'200') + ' words.\n\n';
  prompt += 'REQUIRED: You MUST wrap EVERY word from the list below in double asterisks like **word** in the story text.\n';
  prompt += 'Example: "The **brave** knight found a **magic** sword."\n\n';
  prompt += 'Word list: ' + words.join(', ') + '\n\n';
  prompt += 'Return ONLY valid JSON in this format:\n';
  prompt += '{"title":"story title","text":"story text with **word** markers","words":["word1","word2",...]}';
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
    // Step 1: escape HTML
    var escaped = escHtml(lastStory);
    // Step 2: try to replace **word** markers
    var withMarks = escaped.replace(/\*\*(.*?)\*\*/g, '<mark>$1</mark>');
    // Step 3: if no markers found, auto-highlight words from lastStoryWords
    if (withMarks === escaped) {
      var lowerText = lastStory.toLowerCase();
      var highlighted = escaped;
      var usedWords = {};
      for (var w = 0; w < lastStoryWords.length; w++) {
        var word = lastStoryWords[w];
        if (usedWords[word]) continue;
        var regex = new RegExp('\\b' + escHtml(word).replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\b', 'gi');
        highlighted = highlighted.replace(regex, function(match) {
          usedWords[word] = true;
          return '<mark>' + match + '</mark>';
        });
      }
      textEl.innerHTML = highlighted;
    } else {
      textEl.innerHTML = withMarks;
    }
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
  var prompt = 'Generate ' + count + ' English ' + (type==='fill'?'fill-in-the-blank':type==='choice'?'multiple-choice':type==='sort'?'sentence-ordering':'cloze') + ' questions. Difficulty: ' + diff + '. Words to use: ' + words.join(', ') + '.\n\n';
  prompt += 'IMPORTANT FORMAT RULES:\n';
  prompt += '- Return ONLY a JSON array, no extra text.\n';
  prompt += '- For multiple-choice: "answer" MUST be the index number (0,1,2,3), NOT the text.\n';
  prompt += '- For all other types: "answer" is the text string.\n\n';
  prompt += 'JSON format:\n';
  if (type === 'choice') {
    prompt += '[{"type":"choice","question":"question text","answer":0,"options":["opt A","opt B","opt C","opt D"],"hint":"optional hint"},...]';
  } else {
    prompt += '[{"type":"' + type + '","question":"question text","answer":"correct answer text","options":[],"hint":"optional hint"},...]';
  }
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
    html += '<div class="quiz-card card" id="quiz-q-' + i + '" style="margin-bottom:16px"><div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px">'
      + '<div style="font-weight:700">第' + (i+1) + '题（' + typeName + '）</div>'
      + '<div id="quiz-mark-' + i + '"></div></div>'
      + '<div style="margin-bottom:12px">' + escHtml(q.question) + '</div>';
    if (q.type === 'choice' && q.options) {
      html += '<div id="quiz-opts-' + i + '" style="display:flex;flex-direction:column;gap:8px">';
      for (var j = 0; j < q.options.length; j++) {
        html += '<button class="choice-btn" id="quiz-opt-' + i + '-' + j + '" style="padding:8px 14px;border:1.5px solid #dfe6e9;border-radius:10px;background:white;cursor:pointer;text-align:left;font-family:inherit;font-size:0.92rem" onclick="selectChoice(' + i + ',' + j + ',this)">' + String.fromCharCode(65+j) + '. ' + escHtml(q.options[j]) + '</button>';
      }
      html += '</div>';
    } else {
      html += '<input type="text" id="quiz-ans-' + i + '" style="width:100%;padding:10px 14px;border:1.5px solid #dfe6e9;border-radius:10px;font-size:0.92rem" placeholder="输入答案">'
        + '<div id="quiz-correct-ans-' + i + '" style="display:none;margin-top:6px;font-size:0.9rem"></div>';
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
    var userAnsText = '';
    if (q.type === 'choice' && q.options) {
      // 兼容两种格式：q.answer 可能是索引数字，也可能是答案文本
      var userIdx = quizAnswers[i];
      // 方式1：把 q.answer 当索引来比（处理数字和字符串形式的索引）
      var ansAsIndex = Number(q.answer);
      // 方式2：把 q.answer 当文本来比
      var ansAsText = String(q.answer).toLowerCase().trim();
      var userOptText = (userIdx !== undefined && q.options[userIdx]) ? q.options[userIdx].toLowerCase().trim() : '';
      // 只要有一种方式匹配就算对
      isCorrect = (userIdx !== undefined) && (
        (!isNaN(ansAsIndex) && userIdx === ansAsIndex) ||   // 索引匹配
        (userOptText === ansAsText)                           // 文本匹配
      );
    } else {
      var input = document.getElementById('quiz-ans-' + i);
      userAnsText = input ? input.value.trim() : '';
      isCorrect = userAnsText.toLowerCase() === String(q.answer).trim().toLowerCase();
    }
    // 显示对错标记
    var markEl = document.getElementById('quiz-mark-' + i);
    if (markEl) {
      if (isCorrect) {
        markEl.innerHTML = '<span style="color:#26de81;font-size:1.4rem;font-weight:900">O</span>';
      } else {
        markEl.innerHTML = '<span style="color:#ff5e57;font-size:1.4rem;font-weight:900">X</span>';
      }
    }
    // 选择题：高亮正确/错误选项
    if (q.type === 'choice' && q.options) {
      // 找出正确答案的索引（兼容两种格式）
      var correctIdx = -1;
      var tryIdx = Number(q.answer);
      if (!isNaN(tryIdx) && tryIdx >= 0 && tryIdx < q.options.length) {
        correctIdx = parseInt(tryIdx);
      } else {
        // q.answer 是文本，找到匹配的选项索引
        var ansText = String(q.answer).toLowerCase().trim();
        for (var k = 0; k < q.options.length; k++) {
          if (q.options[k].toLowerCase().trim() === ansText) { correctIdx = k; break; }
        }
      }
      if (correctIdx >= 0) {
        var correctBtn = document.getElementById('quiz-opt-' + i + '-' + correctIdx);
        if (correctBtn) { correctBtn.style.borderColor = '#26de81'; correctBtn.style.background = '#e8fff3'; }
      }
      // 也通过答案文本匹配来高亮（双重保险）
      if (correctIdx < 0) {
        for (var k = 0; k < q.options.length; k++) {
          if (q.options[k].toLowerCase().trim() === String(q.answer).toLowerCase().trim()) {
            var correctBtn2 = document.getElementById('quiz-opt-' + i + '-' + k);
            if (correctBtn2) { correctBtn2.style.borderColor = '#26de81'; correctBtn2.style.background = '#e8fff3'; }
            break;
          }
        }
      }
      if (!isCorrect && userIdx !== undefined) {
        var wrongBtn = document.getElementById('quiz-opt-' + i + '-' + userIdx);
        if (wrongBtn) { wrongBtn.style.borderColor = '#ff5e57'; wrongBtn.style.background = '#fff0f0'; }
      }
      // 禁用所有选项按钮
      for (var j = 0; j < q.options.length; j++) {
        var optBtn = document.getElementById('quiz-opt-' + i + '-' + j);
        if (optBtn) { optBtn.style.cursor = 'default'; optBtn.onclick = null; }
      }
    }
    // 填空题：显示正确答案
    if (q.type !== 'choice') {
      var ansEl = document.getElementById('quiz-correct-ans-' + i);
      var inputEl = document.getElementById('quiz-ans-' + i);
      if (ansEl) {
        ansEl.style.display = 'block';
        if (isCorrect) {
          ansEl.innerHTML = '<span style="color:#26de81;font-weight:700">回答正确！</span>';
        } else {
          ansEl.innerHTML = '<span style="color:#ff5e57;font-weight:700">正确答案：' + escHtml(q.answer) + '</span>';
        }
      }
      if (inputEl) { inputEl.disabled = true; if (isCorrect) inputEl.style.borderColor = '#26de81'; else inputEl.style.borderColor = '#ff5e57'; }
    }
    if (isCorrect) correct++;
    else {
      var ansWord = q.answer;
      // 选择题时，ansWord 可能是索引，需要转成单词
      if (q.type === 'choice' && q.options) {
        var idx = parseInt(q.answer);
        if (!isNaN(idx) && q.options[idx]) ansWord = q.options[idx];
        else ansWord = String(q.answer);
      }
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