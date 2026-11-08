/* 印刷ボタン、入力欄の保存、名前入りなぞり書きの組み立て。入力内容はこの端末のブラウザ(localStorage)にだけ保存され、送信されません。 */
(function () {
  var KEY = 'tsukue:';
  var ls = {
    get: function (k, d) { try { var v = localStorage.getItem(KEY + k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem(KEY + k, JSON.stringify(v)); } catch (e) {} }
  };
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function nameSheet(name) {
    var chars = Array.from(name.replace(/\s/g, '')).slice(0, 6);
    var inner;
    if (!chars.length) {
      inner = '<p class="empty">名前を入力すると、ここになぞり書きの練習が作られます。</p>';
    } else {
      var rows = chars.map(function (c) {
        c = esc(c);
        return '<div class="trow"><div class="tb model">' + c + '</div><div class="tb">' + c + '</div><div class="tb">' + c + '</div><div class="tb"></div><div class="tb"></div><div class="tb"></div></div>';
      }).join('');
      var full = '<div class="trow full">' + chars.map(function (c) { return '<div class="tb">' + esc(c) + '</div>'; }).join('') +
        new Array(6 - chars.length + 1).join('<div class="tb"></div>') + '</div>';
      inner = '<div class="trows">' + rows + full + '</div>';
    }
    return '<div class="sh"><h2>ひらがな れんしゅう<small>うすい じを なぞろう</small></h2>' +
      '<div class="nmline"><span>なまえ</span><i>' + esc(name) + '</i></div>' + inner + '</div>';
  }

  function bindInputs(scope) {
    Array.prototype.forEach.call(scope.querySelectorAll('input[data-k]'), function (el) {
      el.value = ls.get('f:' + el.getAttribute('data-k'), el.getAttribute('data-d') || '');
      el.addEventListener('input', function () { ls.set('f:' + el.getAttribute('data-k'), el.value); });
    });
  }

  var sheet = document.querySelector('.sheet');
  if (sheet) {
    var nin = document.getElementById('nameIn');
    if (nin) {
      nin.value = ls.get('name', '');
      sheet.innerHTML = nameSheet(nin.value);
      nin.addEventListener('input', function () { ls.set('name', nin.value); sheet.innerHTML = nameSheet(nin.value); });
    }
    bindInputs(sheet);
  }
  Array.prototype.forEach.call(document.querySelectorAll('[data-share]'), function (box) {
    var url = box.getAttribute('data-url'), title = box.getAttribute('data-title');
    var ok = box.querySelector('.share-ok');
    function say(m) { ok.textContent = m; setTimeout(function () { ok.textContent = ''; }, 2500); }
    var nat = box.querySelector('[data-share-native]');
    if (nat && navigator.share) {
      nat.hidden = false;
      nat.addEventListener('click', function () {
        navigator.share({ title: title, url: url }).catch(function () {});
      });
    }
    var cp = box.querySelector('[data-share-copy]');
    cp.addEventListener('click', function () {
      function fallback() {
        var ta = document.createElement('textarea');
        ta.value = url; ta.setAttribute('readonly', ''); ta.style.position = 'fixed'; ta.style.opacity = '0';
        document.body.appendChild(ta); ta.select();
        var done = false;
        try { done = document.execCommand('copy'); } catch (e) {}
        document.body.removeChild(ta);
        say(done ? 'コピーしました' : 'コピーできませんでした');
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(function () { say('コピーしました'); }, fallback);
      } else { fallback(); }
    });
  });
  Array.prototype.forEach.call(document.querySelectorAll('[data-print]'), function (b) {
    b.addEventListener('click', function () { window.print(); });
  });
})();

/* 狭い画面でタブが横に並ぶとき、いま開いているタブが見えるようにする */
(function () {
  try {
    var cur = document.querySelector('nav.tabs a[aria-current="page"]');
    var nav = cur && cur.parentNode;
    if (nav && nav.scrollWidth > nav.clientWidth) nav.scrollLeft = Math.max(0, cur.offsetLeft - 16);
  } catch (e) {}
})();
