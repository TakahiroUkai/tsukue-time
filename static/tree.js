/* クリスマスツリーメーカー。ぬりえ・シール台紙の絵を、このブラウザの中だけで作る(名前や設定は送信されず、この端末の localStorage にだけ保存される)。 */
(function () {
  var sheet = document.getElementById('tmSheet');
  if (!sheet) return;
  var KEY = 'tsukue:tree';
  function load() { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; } }
  function save(v) { try { localStorage.setItem(KEY, JSON.stringify(v)); } catch (e) {} }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function rng(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; var t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }

  var CX = 105;
  var SHAPES = {
    tri: { style: 'straight', tiers: [[40, 100, 32], [75, 150, 48], [120, 205, 64]], trunk: [205, 236, 11] },
    round: { style: 'scallop', tiers: [[44, 104, 34], [80, 152, 50], [124, 206, 64]], trunk: [206, 236, 11] },
    slim: { style: 'straight', tiers: [[38, 92, 24], [68, 130, 34], [104, 172, 44], [146, 218, 54]], trunk: [218, 242, 10] }
  };
  var LEVELS = { easy: { sw: 1.8, r: 9, star: 12 }, normal: { sw: 1.2, r: 6.8, star: 10 }, fine: { sw: 0.8, r: 5.2, star: 8 } };
  var COLORS = ['あか', 'あお', 'きいろ', 'みどり'];

  function bulge(shape, t) { return shape.style === 'scallop' ? t[2] / Math.max(3, Math.round(t[2] / 11)) : 0; }
  function hw(t, y) { return t[2] * Math.max(0, Math.min(1, (y - t[0]) / (t[1] - t[0]))); }
  function starPath(x, y, R) {
    var d = '';
    for (var i = 0; i < 10; i++) {
      var a = -Math.PI / 2 + i * Math.PI / 5, r = i % 2 ? R * 0.45 : R;
      d += (i ? 'L' : 'M') + (x + r * Math.cos(a)).toFixed(2) + ' ' + (y + r * Math.sin(a)).toFixed(2);
    }
    return d + 'Z';
  }
  function tierPath(t, style) {
    var top = t[0], base = t[1], h = t[2];
    if (style === 'straight') return 'M' + CX + ' ' + top + 'L' + (CX + h) + ' ' + base + 'L' + (CX - h) + ' ' + base + 'Z';
    var n = Math.max(3, Math.round(h / 11)), seg = 2 * h / n, d = 'M' + CX + ' ' + top + 'L' + (CX + h) + ' ' + base;
    for (var i = 1; i <= n; i++) d += 'A' + (seg / 2).toFixed(2) + ' ' + (seg / 2).toFixed(2) + ' 0 0 1 ' + (CX + h - i * seg).toFixed(2) + ' ' + base;
    return d + 'Z';
  }

  /* かざりの場所をくじ引きで決める(上の段にかくれる場所と、ほかのかざりに重なる場所は避ける) */
  function place(shape, count, r, seed, kinds) {
    var rand = rng(seed * 7919 + 13), tiers = shape.tiers, out = [], gap = 1.15;
    var areas = tiers.map(function (t) { return t[2] * (t[1] - t[0]); }), sum = areas.reduce(function (a, b) { return a + b; }, 0);
    for (var n = 0; n < count; n++) {
      var kind = kinds === 'ball' ? 'ball' : kinds === 'star' ? 'star' : (n % 3 === 2 ? 'star' : 'ball');
      var rr = kind === 'star' ? r * 1.15 : r, ok = null;
      for (var tries = 0; tries < 900 && !ok; tries++) {
        var f = tries > 500 ? 1.05 : gap;
        var pick = rand() * sum, k = 0;
        while (k < tiers.length - 1 && pick > areas[k]) { pick -= areas[k]; k++; }
        var t = tiers[k], y0 = t[0] + rr * 2.2, y1 = t[1] - rr - 3;
        if (y1 <= y0) continue;
        var y = y0 + rand() * (y1 - y0), w = hw(t, Math.min(y, t[1])) - rr * 1.35;
        if (w <= 0) continue;
        var x = CX + (rand() * 2 - 1) * w, bad = false;
        for (var j = 0; j < k && !bad; j++) {
          var u = tiers[j];
          if (y - rr - 1 < u[1] + bulge(shape, u) && Math.abs(x - CX) < hw(u, Math.min(y, u[1])) + rr * 1.4) bad = true;
        }
        for (var m = 0; m < out.length && !bad; m++) {
          var dx = x - out[m].x, dy = y - out[m].y;
          if (Math.sqrt(dx * dx + dy * dy) < (rr + out[m].r) * f) bad = true;
        }
        if (!bad) ok = { x: x, y: y, r: rr, kind: kind };
      }
      if (ok) out.push(ok);
    }
    return out;
  }

  function present(x, yb, w, h, sw, col) {
    var rx = x - w / 2, ry = yb - h, s = 'stroke="' + col + '" stroke-width="' + sw + '"';
    return '<rect x="' + rx.toFixed(1) + '" y="' + ry.toFixed(1) + '" width="' + w + '" height="' + h + '" ' + s + '/>' +
      '<path d="M' + x + ' ' + ry + 'V' + yb + 'M' + rx + ' ' + (ry + h * 0.4).toFixed(1) + 'H' + (rx + w) + '" ' + s + '/>' +
      '<path d="M' + x + ' ' + ry + 'c-6 -7 -9 0 0 0c6 -7 9 0 0 0" ' + s + '/>';
  }

  function build(o) {
    var shape = SHAPES[o.shape] || SHAPES.tri, lv = LEVELS[o.level] || LEVELS.normal, seal = o.mode === 'seal';
    var line = seal ? '#9a9a9a' : '#111', sw = seal ? Math.max(0.9, lv.sw * 0.8) : lv.sw;
    var ground = shape.trunk[1], s = '';
    var tr = shape.trunk, tw = tr[2];
    s += '<g fill="#fff" stroke="' + line + '" stroke-width="' + sw + '" stroke-linejoin="round" stroke-linecap="round">';
    s += '<rect x="' + (CX - tw) + '" y="' + tr[0] + '" width="' + tw * 2 + '" height="' + (tr[1] - tr[0]) + '"/>';
    for (var i = shape.tiers.length - 1; i >= 0; i--) s += '<path d="' + tierPath(shape.tiers[i], shape.style) + '"/>';
    s += '<path d="' + starPath(CX, shape.tiers[0][0] - lv.star * 0.35, lv.star) + '"/>';
    s += '<path fill="none" d="M12 ' + ground + 'Q58 ' + (ground - 9) + ' ' + CX + ' ' + ground + 'T198 ' + ground + '"/>';
    if (o.gifts) {
      var rand = rng(o.seed * 31 + 5), gy = ground + 15;
      s += present(CX - 52 - rand() * 8, gy, 20 + Math.round(rand() * 6), 15 + Math.round(rand() * 5), sw, line);
      s += present(CX + 46 + rand() * 8, gy, 20 + Math.round(rand() * 6), 15 + Math.round(rand() * 5), sw, line);
    }
    s += '</g>';
    var orns = place(shape, o.count, lv.r, o.seed, seal ? 'ball' : o.kinds), ci = 0;
    if (seal) {
      s += '<g fill="none" stroke="#777" stroke-width="0.6" stroke-dasharray="1.6 1.4" stroke-linecap="round">';
      orns.forEach(function (a) { s += '<circle cx="' + a.x.toFixed(1) + '" cy="' + a.y.toFixed(1) + '" r="' + a.r.toFixed(1) + '"/>'; });
      s += '</g><g fill="#a0a0a0" font-size="' + Math.max(3, lv.r * 0.5).toFixed(1) + '" text-anchor="middle" dominant-baseline="central" class="tm-t">';
      orns.forEach(function (a) { s += '<text x="' + a.x.toFixed(1) + '" y="' + a.y.toFixed(1) + '">' + COLORS[ci++ % COLORS.length] + '</text>'; });
      s += '</g>';
    } else {
      s += '<g fill="#fff" stroke="#111" stroke-width="' + sw + '" stroke-linejoin="round" stroke-linecap="round">';
      orns.forEach(function (a) {
        if (a.kind === 'star') s += '<path d="' + starPath(a.x, a.y, a.r) + '"/>';
        else s += '<circle cx="' + a.x.toFixed(1) + '" cy="' + a.y.toFixed(1) + '" r="' + a.r.toFixed(1) + '"/>' +
          '<rect x="' + (a.x - a.r * 0.3).toFixed(1) + '" y="' + (a.y - a.r - a.r * 0.3).toFixed(1) + '" width="' + (a.r * 0.6).toFixed(1) + '" height="' + (a.r * 0.35).toFixed(1) + '"/>';
      });
      s += '</g>';
    }
    var name = Array.from(o.name || '').slice(0, 8).join('');
    var label = name ? name + ' の クリスマス' : 'メリークリスマス';
    s += '<rect x="45" y="266" width="120" height="22" rx="11" fill="#fff" stroke="' + line + '" stroke-width="' + sw + '"/>';
    s += '<text x="105" y="277.5" font-size="' + (name.length > 6 ? 8 : 10) + '" text-anchor="middle" dominant-baseline="central" fill="#222" class="tm-t">' + esc(label) + '</text>';
    s += '<text x="105" y="20" font-size="8.5" text-anchor="middle" fill="' + (seal ? '#888' : '#444') + '" class="tm-t">' +
      (seal ? 'まるシールを はって ツリーを かざろう' : 'すきな いろで ぬってみよう') + '</text>';
    return '<svg viewBox="0 0 210 297" class="tm-svg" role="img" aria-label="クリスマスツリー(' + (seal ? 'シール台紙' : 'ぬりえ') + ')">' + s + '</svg>';
  }

  var st = { shape: 'tri', mode: 'color', level: 'normal', count: 10, kinds: 'all', gifts: true, name: '', seed: 1 };
  var saved = load();
  Object.keys(st).forEach(function (k) { if (saved[k] !== undefined) st[k] = saved[k]; });
  st.count = +st.count || 10;

  var ctl = document.getElementById('tmCtl');
  function sync() {
    ['shape', 'mode', 'level', 'count', 'kinds'].forEach(function (k) {
      Array.prototype.forEach.call(ctl.querySelectorAll('input[name="' + k + '"]'), function (el) { el.checked = el.value === String(st[k]); });
    });
    ctl.querySelector('input[name="gifts"]').checked = !!st.gifts;
    ctl.querySelector('input[name="tname"]').value = st.name;
  }
  function draw() { sheet.innerHTML = build(st); save(st); }
  ctl.addEventListener('change', function (e) {
    var el = e.target;
    if (el.name === 'gifts') st.gifts = el.checked;
    else if (el.name === 'tname') return;
    else st[el.name] = el.name === 'count' ? +el.value : el.value;
    draw();
  });
  ctl.querySelector('input[name="tname"]').addEventListener('input', function (e) { st.name = e.target.value.slice(0, 16); draw(); });
  document.getElementById('tmAgain').addEventListener('click', function () { st.seed = (st.seed % 9999) + 1; draw(); });
  sync(); draw();
})();
