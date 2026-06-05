/* 陪读问答交互层 — 选中文字提问，回复来自本地 qa-server，历史持久化在 qa-answers.json + localStorage */
(function () {
  'use strict';

  var API = (location.protocol === 'file:') ? null : '';   // file:// 无后端 → 降级只读本地
  var POLL_MS = 1000;
  var LS_KEY = 'explainer_qa_threads_v1';  // localStorage 已按端口(origin)隔离

  // ---------- 关闭提醒横幅（顶部 + 底部）----------
  function bannerHTML(where) {
    if (API === null) {
      return '离线模式（直接用 file:// 打开）· 历史只读，无法提问。要问答请让 Claude 启动问答服务。';
    }
    return '问答服务运行中 · 选中文字即可提问 · <strong>用完请告诉 Claude「关闭问答」来停止服务</strong>';
  }
  function mkBanner(pos) {
    var b = document.createElement('div');
    b.className = 'qa-banner qa-banner-' + pos + (API === null ? ' qa-banner-off' : '');
    b.innerHTML = bannerHTML(pos);
    return b;
  }
  function installBanners() {
    var top = mkBanner('top');
    document.body.insertBefore(top, document.body.firstChild);
    var bottom = mkBanner('bottom');
    document.body.appendChild(bottom);
  }

  // ---------- state ----------
  // threads: { qid: {qid, slideId, anchorText, marker?, msgs:[{role, text, ts}]} }
  var threads = {};
  var serverAnswers = {};   // 来自 qa-answers.json，按 qid

  function loadLocal() {
    try { threads = JSON.parse(localStorage.getItem(LS_KEY) || '{}'); }
    catch (e) { threads = {}; }
  }
  function saveLocal() {
    try { localStorage.setItem(LS_KEY, JSON.stringify(threads)); } catch (e) {}
  }
  function uid() {
    return 'q' + Date.now().toString(36) + Math.floor(Math.random() * 1e4).toString(36);
  }

  // ---------- DOM helpers ----------
  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    return e;
  }
  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  // ---------- bubble (选中文字后冒出来的"问"按钮) ----------
  var bubble = el('button', 'qa-bubble', '问');
  bubble.style.display = 'none';
  document.body.appendChild(bubble);

  var pendingSel = null; // {text, slideId, range}

  function currentSlideId(node) {
    while (node && node !== document.body) {
      if (node.classList && node.classList.contains('slide')) return node.id;
      node = node.parentNode;
    }
    return null;
  }

  document.addEventListener('mouseup', function () {
    setTimeout(function () {
      var sel = window.getSelection();
      var text = sel && sel.toString().trim();
      if (!text || text.length < 2) { bubble.style.display = 'none'; return; }
      // 不在抽屉里选
      var anchorNode = sel.anchorNode;
      if (anchorNode && anchorNode.parentNode && anchorNode.parentNode.closest && anchorNode.parentNode.closest('.qa-drawer')) return;
      var rect = sel.getRangeAt(0).getBoundingClientRect();
      pendingSel = { text: text, slideId: currentSlideId(sel.anchorNode && sel.anchorNode.parentNode) };
      bubble.style.left = (window.scrollX + rect.left + rect.width / 2 - 18) + 'px';
      bubble.style.top = (window.scrollY + rect.top - 42) + 'px';
      bubble.style.display = 'block';
    }, 10);
  });
  document.addEventListener('mousedown', function (e) {
    if (e.target !== bubble) bubble.style.display = 'none';
  });

  bubble.addEventListener('click', function () {
    if (!pendingSel) return;
    openDrawer(null, pendingSel.text, pendingSel.slideId, /*newThread*/true);
    bubble.style.display = 'none';
  });

  // ---------- drawer (右侧抽屉) ----------
  var drawer = el('div', 'qa-drawer');
  drawer.innerHTML =
    '<div class="qa-drawer-head">' +
    '  <span class="qa-drawer-title">陪读问答</span>' +
    '  <span class="qa-conn" id="qa-conn"></span>' +
    '  <button class="qa-x" title="关闭">×</button>' +
    '</div>' +
    '<div class="qa-anchor" id="qa-anchor"></div>' +
    '<div class="qa-msgs" id="qa-msgs"></div>' +
    '<div class="qa-compose">' +
    '  <textarea id="qa-input" rows="3" placeholder="对选中的内容提问…（换行随意，点「发送」才发送）"></textarea>' +
    '  <div class="qa-compose-row">' +
    '    <button class="qa-del" id="qa-del" title="删除这条问答历史">删除此条</button>' +
    '    <button class="qa-send" id="qa-send">发送</button>' +
    '  </div>' +
    '</div>';
  document.body.appendChild(drawer);
  drawer.querySelector('.qa-x').addEventListener('click', closeDrawer);
  drawer.querySelector('#qa-del').addEventListener('click', deleteActiveThread);

  var activeQid = null;

  function openDrawer(qid, anchorText, slideId, newThread) {
    drawer.classList.add('open');
    document.getElementById('qa-conn').textContent = API === null ? '· 离线（只读历史）' : '· 已连本地服务';
    document.getElementById('qa-conn').className = 'qa-conn ' + (API === null ? 'off' : 'on');
    if (newThread) {
      activeQid = uid();
      threads[activeQid] = { qid: activeQid, slideId: slideId, anchorText: anchorText, msgs: [] };
      saveLocal();
    } else {
      activeQid = qid;
    }
    var t = threads[activeQid];
    document.getElementById('qa-anchor').innerHTML =
      '<span class="qa-anchor-label">选中片段</span>「' + esc(t.anchorText) + '」' +
      (t.slideId ? ' <span class="qa-anchor-slide">' + esc(t.slideId) + '</span>' : '');
    renderMsgs();
    var inp = document.getElementById('qa-input');
    inp.disabled = (API === null);
    setTimeout(function () { inp.focus(); }, 50);
  }
  function closeDrawer() { drawer.classList.remove('open'); activeQid = null; }

  function renderMsgs() {
    var box = document.getElementById('qa-msgs');
    var t = threads[activeQid];
    box.innerHTML = '';
    if (!t.msgs.length) {
      box.appendChild(el('div', 'qa-empty', '还没有提问。在下面输入你的问题，发送后我会在这个窗口看到并回复。'));
    }
    t.msgs.forEach(function (m) {
      var row = el('div', 'qa-msg qa-' + m.role);
      row.appendChild(el('div', 'qa-role', m.role === 'user' ? '你' : '陪读'));
      row.appendChild(el('div', 'qa-text', renderText(m.text)));
      box.appendChild(row);
    });
    if (t.awaiting) {
      var w = el('div', 'qa-msg qa-assistant qa-waiting');
      w.appendChild(el('div', 'qa-role', '陪读'));
      w.appendChild(el('div', 'qa-text', '已收到，等待 Claude 回复…（不是即时的：Claude 在对话里看到你的问题后才会写回来，通常几十秒到一两分钟。这个抽屉会自动刷新出答案。）'));
      box.appendChild(w);
    }
    box.scrollTop = box.scrollHeight;
  }
  // 极简 markdown：**粗**、`代码`、换行
  function renderText(s) {
    var h = esc(s);
    h = h.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    h = h.replace(/`([^`]+)`/g, '<code>$1</code>');
    h = h.replace(/\n/g, '<br>');
    return h;
  }

  function send() {
    var inp = document.getElementById('qa-input');
    var q = inp.value.trim();
    if (!q || !activeQid) return;
    var t = threads[activeQid];
    t.msgs.push({ role: 'user', text: q, ts: Date.now() });
    t.awaiting = true;
    saveLocal();
    inp.value = '';
    renderMsgs();
    markSlide(t.slideId, t.anchorText, activeQid);

    if (API !== null) {
      fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          qid: activeQid, slideId: t.slideId, anchorText: t.anchorText,
          question: q, history: t.msgs
        })
      }).catch(function (e) {
        t.awaiting = false; saveLocal();
        t.msgs.push({ role: 'assistant', text: '（发送失败：本地问答服务没连上。让 Claude 启动问答服务，并通过它给出的 http://127.0.0.1:… 地址打开本页）', ts: Date.now() });
        renderMsgs();
      });
    }
  }
  document.getElementById('qa-send').addEventListener('click', send);
  // 回车只换行，不发送（必须点「发送」）。但 Cmd/Ctrl+Enter 作为快捷发送保留。
  document.getElementById('qa-input').addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) { e.preventDefault(); send(); }
    e.stopPropagation();  // 别让按键冒泡到翻页/滚动处理
  });

  // ---------- 删除历史 ----------
  function deleteActiveThread() {
    if (!activeQid) return;
    var t = threads[activeQid];
    if (!t) return;
    if (!window.confirm('删除这条问答历史？此操作不可撤销。')) return;
    // 移除该 slide 上的 ◦ 标记
    var mk = document.querySelector('.qa-marker[data-qid="' + activeQid + '"]');
    if (mk && mk.parentNode) mk.parentNode.removeChild(mk);
    delete threads[activeQid];
    saveLocal();
    activeQid = null;
    closeDrawer();
  }

  // ---------- 光标注释标记 (◦) ----------
  function markSlide(slideId, anchorText, qid) {
    if (!slideId) return;
    var sec = document.getElementById(slideId);
    if (!sec) return;
    var head = sec.querySelector('.col-read .slide-num') || sec.querySelector('.slide-num') || sec;
    if (!head.querySelector('.qa-marker[data-qid="' + qid + '"]')) {
      var m = el('span', 'qa-marker', '◦');
      m.title = '查看这条提问的完整问答历史';
      m.setAttribute('data-qid', qid);
      m.addEventListener('click', function (e) {
        e.stopPropagation();
        var t = threads[qid];
        openDrawer(qid, t.anchorText, t.slideId, false);
      });
      head.appendChild(m);
    }
  }
  function restoreMarkers() {
    Object.keys(threads).forEach(function (qid) {
      var t = threads[qid];
      if (t.msgs && t.msgs.length) markSlide(t.slideId, t.anchorText, qid);
    });
  }

  // ---------- 轮询服务端回复 ----------
  function applyAnswers(ans) {
    var changed = false;
    Object.keys(ans).forEach(function (qid) {
      var entry = ans[qid];           // { answers: [{text, ts}], answeredUpTo? }
      var t = threads[qid];
      if (!t) return;
      var serverList = entry.answers || [];
      var localAssistant = t.msgs.filter(function (m) { return m.role === 'assistant'; }).length;
      if (serverList.length > localAssistant) {
        for (var i = localAssistant; i < serverList.length; i++) {
          t.msgs.push({ role: 'assistant', text: serverList[i].text, ts: serverList[i].ts || Date.now() });
        }
        t.awaiting = false;
        changed = true;
      }
    });
    if (changed) { saveLocal(); if (activeQid) renderMsgs(); }
  }
  function poll() {
    if (API === null) return;
    fetch('/qa/qa-answers.json?ts=' + Date.now(), { cache: 'no-store' })
      .then(function (r) { return r.ok ? r.json() : {}; })
      .then(function (j) { serverAnswers = j || {}; applyAnswers(serverAnswers); })
      .catch(function () {});
  }

  // ---------- init ----------
  loadLocal();
  installBanners();
  restoreMarkers();
  poll();
  if (API !== null) setInterval(poll, POLL_MS);

  // 暴露给控制台调试
  window.__qa = { threads: function () { return threads; }, poll: poll };
})();
