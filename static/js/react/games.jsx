/* ============================================================
   BrainGames — React o'yin pleyeri (MindSkills uslubi)
   window.BG_GAME, BG_SUBMIT_URL, BG_HOME, BG_CSRF, BG_SOUND, BG_USER
   ============================================================ */
const { useState, useEffect, useRef } = React;
const G = window.BG_GAME || {};
const USER = window.BG_USER || { name: "O'yinchi", avatar: "🦊" };

const rnd = n => Math.floor(Math.random() * n);
const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = rnd(i + 1);[a[i], a[j]] = [a[j], a[i]]; } return a; };
function gcd(a, b) { return b ? gcd(b, a % b) : a; }

/* ---------- Qiyinlik darajalari (Adaptiv) ---------- */
const DIFFS = [
  { id: 1, name: 'Oson', icon: '🟢', color: '#22b07d', desc: 'Boshlovchilar uchun' },
  { id: 2, name: "O'rta", icon: '🟡', color: '#f5a623', desc: 'Kundalik mashq' },
  { id: 3, name: 'Qiyin', icon: '🔴', color: '#ef4d6b', desc: 'Tajribalilar uchun' },
];
const DIFF_BY_ID = { 1: DIFFS[0], 2: DIFFS[1], 3: DIFFS[2] };
// daraja bo'yicha qiymat tanlash: lvl([oson, o'rta, qiyin], d)
const lvl = (arr, d) => arr[(d || 2) - 1];
function lastDiff() { const v = parseInt(localStorage.getItem('bg_difficulty'), 10); return (v >= 1 && v <= 3) ? v : 2; }
// Faol qiyinlik — Shell chipida ko'rsatish uchun App render paytida yangilanadi
let ACTIVE_DIFF = 2;
// App o'rnatadi: qiyinlik tanlash ekranini qayta ochadi
let openDiffPicker = null;

/* ---------- Ovoz sozlamalari ---------- */
// AUDIO: { master, music, sfx, voice } — localStorage 'bg_audio' da saqlanadi
const AUDIO = (() => {
  let s = {};
  try { s = JSON.parse(localStorage.getItem('bg_audio') || '{}'); } catch (e) { }
  return {
    master: s.master !== undefined ? !!s.master : (window.BG_SOUND !== false),
    music: s.music !== false,
    sfx: s.sfx !== false,
    voice: s.voice !== false,
  };
})();
function saveAudio() { try { localStorage.setItem('bg_audio', JSON.stringify(AUDIO)); } catch (e) { } }
function audioOn(kind) { return AUDIO.master !== false && AUDIO[kind] !== false; }

// Umumiy AudioContext (Sound + Music baham ko'radi). Foydalanuvchi imo-ishorasidan keyin resume bo'ladi.
let _actx = null;
function actx() {
  try {
    _actx = _actx || new (window.AudioContext || window.webkitAudioContext)();
    if (_actx.state === 'suspended') _actx.resume();
  } catch (e) { _actx = null; }
  return _actx;
}

/* ---------- Effektlar (SFX) ---------- */
const Sound = (() => {
  function beep(f, d, type, vol) {
    if (!audioOn('sfx')) return;
    try {
      const ctx = actx(); if (!ctx) return;
      const o = ctx.createOscillator(), g = ctx.createGain();
      o.type = type || 'sine'; o.frequency.value = f; o.connect(g); g.connect(ctx.destination);
      g.gain.value = vol || .07; o.start();
      g.gain.exponentialRampToValueAtTime(.0001, ctx.currentTime + (d || .15)); o.stop(ctx.currentTime + (d || .15));
    } catch (e) { }
  }
  // Pufak "pop" ovozi — har bir tugma tanlashda
  function pop() {
    if (!audioOn('sfx')) return;
    try {
      const ctx = actx(); if (!ctx) return;
      const o = ctx.createOscillator(), g = ctx.createGain(); const t = ctx.currentTime;
      o.type = 'sine';
      o.frequency.setValueAtTime(260, t); o.frequency.exponentialRampToValueAtTime(1180, t + .05);
      o.connect(g); g.connect(ctx.destination);
      g.gain.setValueAtTime(.0001, t); g.gain.exponentialRampToValueAtTime(.16, t + .012);
      g.gain.exponentialRampToValueAtTime(.0001, t + .14);
      o.start(t); o.stop(t + .16);
    } catch (e) { }
  }
  return {
    tick: () => beep(620, .07), flip: () => beep(880, .06), pop,
    correct: () => { beep(880, .1); setTimeout(() => beep(1180, .12), 90); },
    wrong: () => beep(170, .22, 'sawtooth'),
    win: () => [660, 880, 1180, 1320].forEach((f, i) => setTimeout(() => beep(f, .16), i * 110)),
  };
})();

/* ---------- Fon musiqasi (Kahoot uslubidagi quvnoq loop) ---------- */
const Music = (() => {
  let timer = null, i = 0, playing = false;
  const STEP = 230; // ms
  const MEL = [523.25, 659.25, 783.99, 659.25, 698.46, 880, 1046.5, 880, 783.99, 987.77, 1174.66, 987.77, 1046.5, 783.99, 659.25, 523.25];
  const BASS = [130.81, 0, 0, 0, 174.61, 0, 0, 0, 196.00, 0, 0, 0, 130.81, 0, 0, 0];
  function tone(freq, dur, vol, type) {
    if (!freq) return;
    try {
      const ctx = actx(); if (!ctx) return;
      const o = ctx.createOscillator(), g = ctx.createGain(); const t = ctx.currentTime;
      o.type = type || 'triangle'; o.frequency.value = freq; o.connect(g); g.connect(ctx.destination);
      g.gain.setValueAtTime(.0001, t); g.gain.exponentialRampToValueAtTime(vol, t + .02);
      g.gain.exponentialRampToValueAtTime(.0001, t + dur);
      o.start(t); o.stop(t + dur + .02);
    } catch (e) { }
  }
  function tick() {
    if (!playing) return;
    if (audioOn('music')) {
      tone(MEL[i % MEL.length], STEP / 1000 * 0.9, .045, 'triangle');
      tone(BASS[i % BASS.length], STEP / 1000 * 1.5, .05, 'sine');
    }
    i++; timer = setTimeout(tick, STEP);
  }
  return {
    start() { if (playing) return; playing = true; i = 0; tick(); },
    stop() { playing = false; clearTimeout(timer); },
    get playing() { return playing; },
  };
})();

/* ---------- Ovozli maqtov / tanbeh (o'zbekcha TTS) ----------
   Brauzer SpeechSynthesis orqali o'qiydi. Haqiqiy o'zbek ovozi
   bo'lmasa, eng yaqin (tr/ru) yoki standart ovoz tanlanadi. */
const Speech = (() => {
  function bestVoice() {
    try {
      const vs = (window.speechSynthesis && speechSynthesis.getVoices()) || [];
      return vs.find(v => /uz/i.test(v.lang)) || vs.find(v => /tr/i.test(v.lang)) || vs.find(v => /ru/i.test(v.lang)) || vs[0] || null;
    } catch (e) { return null; }
  }
  function say(text) {
    if (!audioOn('voice') || !('speechSynthesis' in window)) return;
    try {
      const u = new SpeechSynthesisUtterance(text);
      const v = bestVoice(); if (v) { u.voice = v; u.lang = v.lang; } else { u.lang = 'uz-UZ'; }
      u.rate = 1; u.pitch = 1.15; u.volume = 1;
      speechSynthesis.cancel(); speechSynthesis.speak(u);
    } catch (e) { }
  }
  const WIN = ["Oo qoyil!", "Malades!", "Qoyilmaqom!", "G'alaba!", "Davom etamiz!"];
  const LOSE = ["Oo yo'q!", "Afsus!", "Yana biror urinib ko'ring!"];
  return { win: () => say(WIN[rnd(WIN.length)]), lose: () => say(LOSE[rnd(LOSE.length)]), say };
})();
// Ovozlar asinxron yuklanadi — ro'yxatni oldindan tayyorlaymiz
if ('speechSynthesis' in window) { try { speechSynthesis.getVoices(); speechSynthesis.onvoiceschanged = () => { }; } catch (e) { } }

async function postResult(score, duration, difficulty) {
  try {
    const res = await fetch(window.BG_SUBMIT_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': window.BG_CSRF },
      body: JSON.stringify({ score, duration: duration || 30, difficulty: difficulty || ACTIVE_DIFF }),
    });
    return await res.json();
  } catch (e) { return {}; }
}

/* ---------- Toast ---------- */
let toastFn = null;
function Toasts() {
  const [list, set] = useState([]);
  toastFn = (m) => { const id = Math.random(); set(l => [...l, { id, m }]); setTimeout(() => set(l => l.filter(x => x.id !== id)), 2400); };
  return <div className="ms-toasts">{list.map(x => <div key={x.id} className="ms-toast" dangerouslySetInnerHTML={{ __html: x.m }} />)}</div>;
}
const toast = m => toastFn && toastFn(m);

function fullscreen() {
  if (!document.fullscreenElement) { (document.documentElement.requestFullscreen || (() => { })).call(document.documentElement); }
  else { (document.exitFullscreen || (() => { })).call(document); }
}
function toggleTheme() { const r = document.documentElement; const n = r.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'; r.setAttribute('data-theme', n); localStorage.setItem('bg_theme', n); }
function toggleSound() {
  AUDIO.master = AUDIO.master === false; // false→true, true→false
  saveAudio();
  toast(AUDIO.master ? "🔊 Ovoz yoniq" : "🔇 Ovoz o'chiq");
}

/* ---------- O'ng vertikal panel ---------- */
function Rail({ tab, onTab }) {
  const items = [['players', 'bi-people-fill'], ['settings', 'bi-gear-fill'], ['sliders', 'bi-sliders'], ['calc', 'bi-calculator'], ['tools', 'bi-tools']];
  return (
    <div className="player-rail">
      {items.map(([k, ic]) => <button key={k} className={"rbtn " + (tab === k ? 'on' : '')} onClick={() => onTab && onTab(k)}><i className={"bi " + ic} /></button>)}
      <div className="rail-sp" />
      <div className="rail-uz">UZ</div>
      <div className="rail-timer">00:00</div>
      <button className="rbtn" onClick={toggleTheme}><i className="bi bi-brightness-high-fill" /></button>
      <button className="rbtn"><i className="bi bi-lock-fill" /></button>
    </div>
  );
}

function gotoSibling(dir) {
  const sibs = window.BG_SIBLINGS || [];
  if (!sibs.length) { window.location = window.BG_HOME; return; }
  let idx = sibs.findIndex(s => s.slug === G.slug); if (idx < 0) idx = 0;
  const ni = (idx + dir + sibs.length) % sibs.length;
  window.location = window.BG_PLAY_BASE + sibs[ni].slug + '/';
}
const SCENES = {
  mental: 'radial-gradient(130% 90% at 50% -10%, #ffe1f0 0%, #f9a8cf 28%, #c25a8a 58%, #4a2152 100%)',
  xotira: 'radial-gradient(130% 90% at 50% -10%, #d3fff7 0%, #67e8d8 30%, #19b5c9 60%, #0c4150 100%)',
  tezoqish: 'radial-gradient(130% 90% at 50% -10%, #ffe0e6 0%, #fb9aae 28%, #ef4d6b 58%, #6b1a32 100%)',
  diqqat: 'radial-gradient(130% 90% at 50% -10%, #dcffe7 0%, #86efac 30%, #22b07d 60%, #114227 100%)',
  matematika: 'radial-gradient(130% 90% at 50% -10%, #fff3cf 0%, #fcd34d 30%, #f5a623 60%, #92400e 100%)',
  subject: 'radial-gradient(130% 90% at 50% -10%, #dbeafe 0%, #93c5fd 30%, #2b8af0 60%, #1e3a8a 100%)',
};
function catKey() {
  return (G.category || '').indexOf('fan-') === 0 ? 'subject' : (G.category || 'mental');
}
function bgClass(calm) { return 'player-bg pbg-' + catKey() + (calm ? ' calm' : ''); }
function sceneFor() { return SCENES[catKey()] || SCENES.mental; }

/* ---------- Ovoz sozlamalari menyusi ---------- */
const AUDIO_ROWS = [['master', 'Umumiy ovoz', 'bi-volume-up-fill'], ['music', 'Fon musiqasi', 'bi-music-note-beamed'], ['sfx', 'Tugma effektlari', 'bi-soundwave'], ['voice', 'Ovozli maqtov', 'bi-chat-left-heart-fill']];
function AudioMenu({ onClose, onChange }) {
  function toggle(k) {
    AUDIO[k] = AUDIO[k] === false; // flip
    saveAudio();
    if (k === 'music' && !audioOn('music')) Music.stop();
    if (audioOn('sfx')) Sound.pop();
    onChange();
  }
  return (
    <div className="audio-menu" onClick={e => e.stopPropagation()}>
      <div className="audio-menu-head">🔊 Ovoz sozlamalari</div>
      {AUDIO_ROWS.map(([k, lbl, ic]) => (
        <label key={k} className="audio-row">
          <span><i className={'bi ' + ic} /> {lbl}</span>
          <input type="checkbox" checked={AUDIO[k] !== false} onChange={() => toggle(k)} />
        </label>
      ))}
    </div>
  );
}

/* ---------- Umumiy qobiq ---------- */
function Shell({ score, name, mascot, topActions, gear, onGear, tab, onTab, panel, calm, children }) {
  const [audioMenu, setAudioMenu] = useState(false);
  const [, force] = useState(0);
  useEffect(() => {
    if (!audioMenu) return;
    const close = () => setAudioMenu(false);
    document.addEventListener('click', close);
    return () => document.removeEventListener('click', close);
  }, [audioMenu]);
  return (
    <div className="player">
      <div className="player-top">
        <a className="pbtn" href={window.BG_HOME} title="Chiqish"><i className="bi bi-house-door-fill" /></a>
        <span className="player-chip">{G.category_name || "O'yin"}</span>
        <span className="player-chip d-none d-md-inline">{G.name}</span>
        <button className="pbtn" onClick={() => gotoSibling(-1)} title="Oldingi o'yin"><i className="bi bi-chevron-left" /></button>
        <button className="pbtn" onClick={() => gotoSibling(1)} title="Keyingi o'yin"><i className="bi bi-chevron-right" /></button>
        <a className="pbtn" href={window.BG_HOME} title="Boshqa o'yinlar"><i className="bi bi-grid-3x3-gap-fill" /></a>
        <button className="player-chip diff-chip" title="Qiyinlik darajasi — o'zgartirish uchun bosing"
          style={{ '--dc': (DIFF_BY_ID[ACTIVE_DIFF] || DIFFS[1]).color }}
          onClick={() => openDiffPicker && openDiffPicker()}>
          {(DIFF_BY_ID[ACTIVE_DIFF] || DIFFS[1]).icon} {(DIFF_BY_ID[ACTIVE_DIFF] || DIFFS[1]).name}
        </button>
        <span className="sp" />
        {topActions}
        {gear !== false && <button className="pbtn" onClick={onGear} title="Sozlamalar"><i className="bi bi-gear-fill" /></button>}
        <button className="pbtn" title="Multipleyer"><i className="bi bi-cast" /></button>
        <span className="audio-wrap">
          <button className="pbtn" title="Ovoz sozlamalari"
            onClick={e => { e.stopPropagation(); setAudioMenu(m => !m); }}>
            <i className={'bi ' + (audioOn('master') ? 'bi-volume-up-fill' : 'bi-volume-mute-fill')} />
          </button>
          {audioMenu && <AudioMenu onClose={() => setAudioMenu(false)} onChange={() => force(x => x + 1)} />}
        </span>
        <button className="pbtn" onClick={fullscreen} title="To'liq ekran"><i className="bi bi-arrows-fullscreen" /></button>
        <button className="pbtn" title="Menyu"><i className="bi bi-list" /></button>
      </div>
      <div className="player-subbar"><i className="bi bi-gear-fill" /> ({score || 0}) {name || USER.name}</div>
      <div className="player-body">
        <div className="player-stage">
          <div className={bgClass(calm)} style={{ background: sceneFor() }}>
            {window.BG_BG_IMG && <img className="player-bg-photo" src={window.BG_BG_IMG} alt="" onError={e => { e.target.style.display = 'none'; }} />}
            <span className="player-bg-scrim" />
            <span className="pbg-a" /><span className="pbg-b" /><span className="pbg-c" />
          </div>
          {mascot && <div className="player-mascot">{mascot}</div>}
          {children}
        </div>
        {panel}
        <Rail tab={tab} onTab={onTab} />
      </div>
    </div>
  );
}

/* ---------- Sozlamalar paneli (Forsaj) ---------- */
function Stepper({ label, color, value, set, suffix }) {
  return (
    <div className="fp-stepper">
      <div className="fp-stepper-main" style={{ background: color }}>
        <span>{label}</span><b>{value}{suffix || ''}</b>
        <span className="fp-arrows"><button onClick={() => set(value + 1)}>▲</button><button onClick={() => set(Math.max(1, value - 1))}>▼</button></span>
      </div>
    </div>
  );
}
function SettingsPanel({ cfg, setCfg }) {
  const set = (k, v) => setCfg(c => ({ ...c, [k]: v }));
  const toggleChip = (key, n) => setCfg(c => {
    const arr = c[key] || [];
    return { ...c, [key]: arr.includes(n) ? arr.filter(x => x !== n) : [...arr, n].sort((a, b) => a - b) };
  });
  return (
    <div className="player-panel">
      <div className="fp-label">Sozlangan o'yinchi yoki guruh</div>
      <select className="fp-sel dark"><option>👥 Guruh</option><option>{USER.name}</option></select>
      <div className="fp-label">Tez-tez sozlash</div>
      <select className="fp-sel red"><option>Tanlang</option></select>
      <div className="fp-label">Modul</div>
      <select className="fp-sel orange"><option>Oddiy xisob</option><option>Ko'paytirish</option></select>
      <div className="fp-label">Operatsiyalar</div>
      <select className="fp-sel red" value={cfg.ops} onChange={e => set('ops', e.target.value)}>
        <option value="+">Qo'shish</option>
        <option value="-">Ayirish</option>
        <option value="+-">Qo'shish va ayirish</option>
      </select>
      <div className="fp-hint">Qaysi sonlar chiqsin — bosib tanlang</div>
      <div className="fp-chiprow">
        {[1, 2, 3, 4, 5, 6, 7, 8, 9].map(n => {
          const on = (cfg.plus || []).includes(n);
          return <button key={n} type="button" className={'fp-chip blue' + (on ? '' : ' off')} onClick={() => toggleChip('plus', n)}>+{n}</button>;
        })}
        <button className="fp-x" title="Hammasini olib tashlash" onClick={() => set('plus', [])}>✕</button>
      </div>
      <div className="fp-chiprow">
        {[1, 2, 3, 4, 5, 6, 7, 8, 9].map(n => {
          const on = (cfg.minus || []).includes(n);
          return <button key={n} type="button" className={'fp-chip red' + (on ? '' : ' off')} onClick={() => toggleChip('minus', n)}>−{n}</button>;
        })}
        <button className="fp-x red" title="Hammasini olib tashlash" onClick={() => set('minus', [])}>✕</button>
      </div>
      <Stepper label="Raqam" color="#22b07d" value={cfg.digits} set={v => set('digits', Math.min(3, v))} />
      <Stepper label="Qatorlar" color="#2b8af0" value={cfg.terms} set={v => set('terms', v)} />
      <Stepper label="Interval" color="#ed1c24" value={cfg.interval} set={v => set('interval', v)} suffix=" c" />
      <div className="fp-label">Raqam rangi</div>
      <div className="fp-colors">
        {['#22c55e', '#2b8af0', '#ed1c24', '#f5a623', '#a855f7', '#06b6d4', '#ec4899', '#ffffff'].map(c => (
          <button key={c} type="button"
            className={'fp-color' + ((cfg.numColor || '#22c55e') === c ? ' on' : '')}
            style={{ background: c }} title={c}
            onClick={() => set('numColor', c)} />
        ))}
        <input type="color" className="fp-color-input" value={cfg.numColor || '#22c55e'}
          onChange={e => set('numColor', e.target.value)} title="Boshqa rang" />
      </div>
      <select className="fp-sel orange mt-2"><option>Almashinish: Yo'q</option></select>
      <div className="fp-label">Limit</div>
      <select className="fp-sel"><option>Cheklov yo'q</option></select>
      <div className="fp-label">Darajalar rejimi</div>
      <select className="fp-sel"><option>Barcha darajalar</option></select>
      <div className="fp-label">Shrift</div>
      <select className="fp-sel dark"><option>Tanlang</option></select>
      <div className="fp-label">Qo'shimcha</div>
      {[['onlyCorrect', "Faqat to'g'ri javoblarni qabul qiling"], ['sample', "Namuna natijasini ko'rsatish"], ['explain', "Tugallangan misolga izoh bering"], ['showNums', "Sonlarni ko'rsatish"], ['voice', "Raqamlarni ovozli eshitish"], ['dictant', "Diktant rejimi"]].map(([k, lbl]) => (
        <label key={k} className="fp-check"><span>{lbl}</span><input type="checkbox" checked={!!cfg[k]} onChange={e => set(k, e.target.checked)} /></label>
      ))}
    </div>
  );
}
const PP_AV = ['🦊', '🐼', '🦁', '🐯', '🐵', '🐶', '🐱', '🐸', '🦉', '🐨', '🐲', '🦄'];
function PlayersPanel() {
  const [players, setPlayers] = useState([{ name: USER.name, avatar: USER.avatar, score: 0 }]);
  const add = () => setPlayers(p => [...p, { name: "O'yinchi " + (p.length + 1), avatar: PP_AV[p.length % PP_AV.length], score: 0 }]);
  const reset = () => setPlayers(p => p.map(x => ({ ...x, score: 0 })));
  const adj = (i, d) => setPlayers(p => p.map((x, j) => j === i ? { ...x, score: Math.max(0, x.score + d) } : x));
  const remove = (i) => setPlayers(p => p.length > 1 ? p.filter((_, j) => j !== i) : p);
  return (
    <div className="player-panel">
      <button className="pp-add" onClick={add}><i className="bi bi-person-plus-fill" /> O'yinchi qo'shish</button>
      <button className="pp-reset" onClick={reset}>Ballarni nolga keltirish</button>
      <div className="pp-list">
        {players.map((pl, i) => (
          <div key={i} className="pp-item">
            <span className="pp-ava">{pl.avatar}</span>
            <span className="pp-name">{pl.name}</span>
            <div className="pp-ctrl"><button onClick={() => adj(i, -1)}>−</button><b>{pl.score}</b><button onClick={() => adj(i, 1)}>+</button></div>
            {players.length > 1 && <button className="pp-del" onClick={() => remove(i)}>✕</button>}
          </div>
        ))}
      </div>
    </div>
  );
}

/* ============================================================ FINISH */
function Finish({ score, onAgain }) {
  const [data, setData] = useState(null);
  useEffect(() => { Sound.win(); setTimeout(() => Speech.win(), 350); postResult(score).then(setData); }, []);
  return (
    <Shell score={score} gear={false}>
      <div className="player-result">
        <div style={{ fontSize: 64 }}>🎉</div>
        <h2>Ajoyib!</h2>
        <div className="eq">Ball: <b>{score}</b></div>
        {data ? <div className="fw-bold mt-2">+{data.xp_earned || 0} XP · +{data.coins_earned || 0} 🪙 · +{data.stars_earned || 0} ⭐</div>
          : <div className="text-muted mt-2">Saqlanmoqda…</div>}
        {data && data.achievements && data.achievements.length > 0 &&
          <div className="mt-2 fw-bold" style={{ color: 'var(--green)' }}>🎖️ {data.achievements.map(a => a.title).join(', ')}</div>}
        <div className="d-flex gap-2 justify-content-center mt-3">
          <a className="btn-outline-ms" href={window.BG_HOME}>Chiqish</a>
          <button className="btn-ms" onClick={onAgain}>Yana o'ynash</button>
        </div>
      </div>
    </Shell>
  );
}

/* ============================================================ MENTAL (forsaj / flash / kopaytir) */
function Mental({ onFinish, diff }) {
  const mode = G.kind; // forsaj | flash | kopaytir
  const isKop = mode === 'kopaytir';
  // Qiyinlik bo'yicha boshlang'ich sozlamalar (panelda keyin o'zgartirsa bo'ladi)
  const P = lvl([
    { terms: 3, digits: 1, ops: '+', interval: 2.6 },
    { terms: 5, digits: 1, ops: '+-', interval: 2 },
    { terms: 7, digits: 2, ops: '+-', interval: 1.3 },
  ], diff);
  const [cfg, setCfg] = useState({ terms: P.terms, digits: P.digits, ops: P.ops, interval: P.interval, plus: [1, 2, 3, 4, 5, 6, 7, 8, 9], minus: [1, 2, 3, 4, 5, 6, 7, 8, 9], showNums: true, voice: false, sample: true, explain: true, numColor: '#22c55e' });
  const [tab, setTab] = useState(isKop ? 'players' : 'settings');
  const [panelOpen, setPanelOpen] = useState(true);
  const [phase, setPhase] = useState('idle');
  const [disp, setDisp] = useState(''); const [op, setOp] = useState('');
  const [round, setRound] = useState(0); const [score, setScore] = useState(0);
  const seq = useRef(null); const ans = useRef(null); const last = useRef(null);
  const ROUNDS = 5;
  const [who, setWho] = useState(0);
  useEffect(() => { const x = setInterval(() => setWho(w => 1 - w), 1100); return () => clearInterval(x); }, []);

  // Tanlangan raqamlardan (chiplardan) cfg.digits xonali son yasaydi
  function pickNum(pool) {
    const p = (pool && pool.length) ? pool : [1, 2, 3, 4, 5, 6, 7, 8, 9];
    let s = '';
    for (let k = 0; k < cfg.digits; k++) s += p[rnd(p.length)];
    return parseInt(s, 10);
  }
  function genSeq() {
    const plus = (cfg.plus && cfg.plus.length) ? cfg.plus : [1, 2, 3, 4, 5, 6, 7, 8, 9];
    const minus = (cfg.minus && cfg.minus.length) ? cfg.minus : [1, 2, 3, 4, 5, 6, 7, 8, 9];
    const nums = [], signs = []; let sum = 0;
    for (let i = 0; i < cfg.terms; i++) {
      // Birinchi had doim "+", keyingilarda ops va joriy yig'indiga qarab
      const wantMinus = i > 0 && (cfg.ops === '-' || (cfg.ops === '+-' && Math.random() < .5));
      if (wantMinus) {
        const cand = pickNum(minus);
        if (sum - cand >= 0) { sum -= cand; nums.push(cand); signs.push('-'); continue; }
      }
      const val = pickNum(plus);
      sum += val; nums.push(val); signs.push('+');
    }
    return { nums, signs, sum };
  }
  function genKop() { const hi = lvl([5, 9, 12], diff); const a = 2 + rnd(hi - 1), b = 2 + rnd(hi - 1); return { a, b, sum: a * b }; }

  function start() {
    if (isKop) { seq.current = genKop(); setPhase('answer'); setTimeout(() => ans.current && ans.current.focus(), 60); return; }
    seq.current = genSeq(); setPhase('count'); setDisp('3'); Sound.tick();
    let c = 3; const cd = setInterval(() => { c--; if (c > 0) { setDisp('' + c); Sound.tick(); } else { clearInterval(cd); flash(); } }, 700);
  }
  function flash() {
    setPhase('flash'); const sp = Math.max(450, cfg.interval * 500); const s = seq.current; let i = 0;
    const show = () => {
      if (i >= s.nums.length) { setDisp(''); setOp(''); setPhase('answer'); setTimeout(() => ans.current && ans.current.focus(), 60); return; }
      setOp(s.signs[i] === '-' ? '−' : '+'); setDisp('' + s.nums[i]); Sound.flip(); i++;
      setTimeout(() => { setDisp(''); setOp(''); setTimeout(show, Math.max(120, sp * 0.25)); }, sp);
    };
    show();
  }
  function check() {
    const s = seq.current; const v = Number(ans.current.value); const ok = v === s.sum; last.current = { ok, v, s };
    if (ok) { const pts = isKop ? 20 : 10 * cfg.terms + (cfg.digits - 1) * 15 + (cfg.ops === '+-' ? 15 : 0); setScore(x => x + pts); Sound.correct(); }
    else { Sound.wrong(); Speech.lose(); }
    setPhase('result');
  }
  function next() { const r = round + 1; if (r >= ROUNDS) { onFinish(score); return; } setRound(r); setPhase(isKop ? 'idle' : 'idle'); if (isKop) start(); }

  const mascot = null;
  const panel = panelOpen ? (tab === 'players'
    ? <PlayersPanel />
    : <SettingsPanel cfg={cfg} setCfg={setCfg} />) : null;

  const topActions = <>
    {(phase === 'idle') && <button className="pbtn" onClick={start} title="Boshlash"><i className="bi bi-play-fill" /></button>}
    {(phase === 'answer') && <button className="pbtn" onClick={check} title="Tekshirish"><i className="bi bi-check-lg" /></button>}
    <button className="pbtn" onClick={() => { setPhase('idle'); setRound(0); }} title="To'xtatish"><i className="bi bi-stop-fill" /></button>
  </>;

  return (
    <Shell score={score} mascot={mascot} topActions={topActions} onGear={() => { setTab('settings'); setPanelOpen(o => tab === 'settings' ? !o : true); }} tab={tab} onTab={t => { setTab(t); setPanelOpen(true); }} panel={panel}>
      {phase === 'idle' && <>
        <div className="player-card">
          <div className="pc-ava">{USER.avatar}</div>
          <div className="pc-score">{score}</div>
          <div className="pc-side"><button className="pc-mini" title="Raqam rangi" onClick={() => { setTab('settings'); setPanelOpen(true); }}>🎨</button><button className="pc-mini">🕘</button></div>
        </div>
        <div className="player-title">{USER.name}</div>
        <div className="player-mode"><button className="arr" onClick={() => gotoSibling(-1)}>‹</button><span className="name">{G.name}</span><button className="arr" onClick={() => gotoSibling(1)}>›</button></div>
        <button className="player-startbtn" onClick={start}>Boshlamoq</button>
      </>}
      {phase === 'count' && <div className="player-count" style={{ color: cfg.numColor, fontSize: 'min(46vh,55vw,340px)' }}>{disp}</div>}
      {phase === 'flash' && <div className="player-flash" style={{ color: cfg.numColor, fontSize: 'min(62vh,64vw,520px)', lineHeight: 1 }}>{op && <span className="flash-op">{op}</span>}{disp || ' '}</div>}
      {phase === 'answer' && <>
        {isKop
          ? <div className="player-flash kop" style={{ color: cfg.numColor, fontSize: 'min(38vh,30vw,300px)' }}>{seq.current.a}<span className="flash-op">×</span>{seq.current.b}</div>
          : <div className="player-flash" style={{ fontSize: 'min(22vh,150px)', opacity: .85 }}>= ?</div>}
        <div className="player-answer">
          <input ref={ans} type="number" inputMode="numeric" placeholder="Javob" onKeyDown={e => e.key === 'Enter' && check()} />
        </div>
        <button className="player-startbtn mt-2" style={{ fontSize: 18, padding: '12px 34px' }} onClick={check}>Tekshirish</button>
      </>}
      {phase === 'result' && (() => {
        const L = last.current; const ex = isKop ? `${L.s.a} × ${L.s.b}` : L.s.nums.map((n, i) => i === 0 ? n : `${L.s.signs[i] === '-' ? '−' : '+'} ${n}`).join(' ');
        return <div className="player-result">
          <div style={{ fontSize: 54 }}>{L.ok ? '✅' : '❌'}</div>
          <div className="eq">{ex} = <b>{L.s.sum}</b></div>
          {!L.ok && <div className="text-danger fw-bold mt-1">Sizning javobingiz: {isNaN(L.v) ? '—' : L.v}</div>}
          <button className="player-startbtn mt-3" style={{ fontSize: 18, padding: '12px 26px' }} onClick={next}>{round + 1 >= ROUNDS ? '🏁 Yakunlash' : 'Keyingi →'}</button>
        </div>;
      })()}
    </Shell>
  );
}

/* ============================================================ COLUMNS */
function Columns({ onFinish, diff }) {
  const ROUNDS = 5; const [round, setRound] = useState(0); const [score, setScore] = useState(0); const [phase, setPhase] = useState('q');
  const ans = useRef(null); const last = useRef(null);
  const [data, setData] = useState(() => genU(0));
  function genU(r) { const c = lvl([{ base: 3, lo: 2, hi: 9 }, { base: 4, lo: 2, hi: 19 }, { base: 5, lo: 10, hi: 49 }], diff); const k = c.base + Math.min(r, 4); const nums = Array.from({ length: k }, () => c.lo + rnd(c.hi - c.lo + 1)); return { nums, sum: nums.reduce((a, b) => a + b, 0) }; }
  function check() { const v = Number(ans.current.value); const ok = v === data.sum; last.current = { ok, v }; if (ok) { setScore(s => s + 15 + round * 5); Sound.correct(); } else { Sound.wrong(); Speech.lose(); } setPhase('result'); }
  function next() { const r = round + 1; if (r >= ROUNDS) { onFinish(score); return; } setRound(r); setData(genU(r)); setPhase('q'); }
  return (
    <Shell score={score} gear={false}>
      <div className="player-score">{round + 1}/{ROUNDS}</div>
      <div style={{ background: 'rgba(255,255,255,.96)', borderRadius: 18, padding: '18px 54px', color: '#2b2b3a' }}>
        {data.nums.map((n, i) => <div key={i} style={{ fontFamily: 'Fredoka', fontWeight: 700, fontSize: 40, textAlign: 'right' }}>{n}</div>)}
        <div style={{ borderTop: '4px solid var(--red)', marginTop: 8 }} />
      </div>
      {phase === 'q'
        ? <><div className="player-answer"><input ref={ans} type="number" placeholder="Yig'indi" autoFocus onKeyDown={e => e.key === 'Enter' && check()} /></div><button className="player-startbtn mt-2" style={{ fontSize: 18, padding: '12px 30px' }} onClick={check}>Tekshirish</button></>
        : <div className="player-result"><div style={{ fontSize: 48 }}>{last.current.ok ? '✅' : '❌'}</div><div className="eq">= <b>{data.sum}</b></div><button className="player-startbtn mt-3" style={{ fontSize: 18, padding: '12px 26px' }} onClick={next}>{round + 1 >= ROUNDS ? '🏁 Yakun' : 'Keyingi →'}</button></div>}
    </Shell>
  );
}

/* ============================================================ QUIZ (variantli) */
const opts4 = ans => { const s = new Set([ans]); while (s.size < 4) { const d = ans + rnd(11) - 5; if (d >= 0) s.add(d); } return shuffle([...s]); };
// Har bir generator qiyinlik darajasini (d=1..3) qabul qiladi va sonlar
// diapazonini shunga moslaydi.
const GEN = {
  mul: d => { const hi = lvl([5, 9, 12], d); const a = 2 + rnd(hi - 1), b = 2 + rnd(hi - 1), x = a * b; return { q: `${a} × ${b}`, ans: x, opts: opts4(x) }; },
  base: d => { const hi = lvl([10, 50, 99], d); const a = rnd(hi + 1), b = rnd(hi + 1), x = a + b; return { q: `${a} + ${b}`, ans: x, opts: opts4(x) }; },
  power: d => { const hi = lvl([5, 9, 14], d); const a = 2 + rnd(hi - 1), x = a * a; return { q: `${a}²`, ans: x, opts: opts4(x) }; },
  gcd: d => { const g = 2 + rnd(lvl([4, 6, 9], d)); const a = g * (1 + rnd(5)), b = g * (1 + rnd(5)); const x = gcd(a, b); return { q: `EKUB(${a}, ${b})`, ans: x, opts: opts4(x) }; },
  frac: d => { const base = (2 + rnd(lvl([5, 9, 16], d))) * 2, x = base / 2; return { q: `${base} ning yarmi`, ans: x, opts: opts4(x) }; },
  percent: d => { const ps = lvl([[10, 50], [10, 20, 25, 50], [5, 15, 20, 25, 40]], d); const p = ps[rnd(ps.length)], base = (2 + rnd(8)) * 10, x = Math.round(base * p / 100); return { q: `${base} ning ${p}%`, ans: x, opts: opts4(x) }; },
  matrix: d => { const hi = lvl([5, 9, 15], d); const a = 1 + rnd(hi), b = 1 + rnd(hi), x = a + b; return { q: `[${a}] + [${b}]`, ans: x, opts: opts4(x) }; },
  add: d => { const hi = lvl([19, 50, 99], d); const a = rnd(hi + 1), b = rnd(hi + 1), x = a + b; return { q: `${a} + ${b}`, ans: x, opts: opts4(x) }; },
  sub: d => { const hi = lvl([20, 60, 99], d); const a = 20 + rnd(hi), b = rnd(a), x = a - b; return { q: `${a} − ${b}`, ans: x, opts: opts4(x) }; },
  div: d => { const hi = lvl([5, 8, 12], d); const b = 2 + rnd(hi - 1), x = 2 + rnd(hi), a = b * x; return { q: `${a} ÷ ${b}`, ans: x, opts: opts4(x) }; },
  double: d => { const hi = lvl([20, 40, 99], d); const a = 1 + rnd(hi), x = a * 2; return { q: `${a} ni ikkilantiring`, ans: x, opts: opts4(x), eq: false }; },
  half: d => { const hi = lvl([12, 25, 50], d); const a = (1 + rnd(hi)) * 2, x = a / 2; return { q: `${a} ning yarmi`, ans: x, opts: opts4(x), eq: false }; },
  compare: d => { const hi = lvl([20, 50, 99], d); const a = rnd(hi + 1), b = rnd(hi + 1), ans = a > b ? '>' : a < b ? '<' : '='; return { q: `${a} ▢ ${b}`, ans, opts: ['>', '<', '='], eq: false }; },
  eo: d => { const hi = lvl([20, 99, 999], d); const a = rnd(hi + 1), ans = a % 2 === 0 ? 'Juft' : 'Toq'; return { q: `${a} — qaysi?`, ans, opts: ['Juft', 'Toq'], eq: false }; },
  seq: d => { const st = 1 + rnd(5), step = lvl([1 + rnd(3), 2 + rnd(4), 3 + rnd(6)], d), seq = [st, st + step, st + 2 * step, st + 3 * step], x = st + 4 * step; return { q: `${seq.join(', ')}, …`, ans: x, opts: shuffle([x, x + step, x - step, x + step + 1]), eq: false }; },
  max: d => { const cnt = lvl([4, 4, 6], d), hi = lvl([30, 95, 200], d); const arr = shuffle(Array.from({ length: cnt }, () => 5 + rnd(hi))); const x = Math.max(...arr); return { q: `Eng katta son?`, ans: x, opts: arr, eq: false }; },
};
function Quiz({ onFinish, diff }) {
  const bank = useRef(G.questions && G.questions.length ? shuffle(G.questions) : null);
  const ptr = useRef(0);
  function nextQ() {
    if (bank.current) { const it = bank.current[ptr.current % bank.current.length]; ptr.current++; return { q: it.q, opts: it.o, ans: it.o[it.a], eq: false }; }
    return (GEN[G.gen] || GEN.base)(diff);
  }
  // Banked testlar (fanlar) uchun qiyinlik = vaqt bosimi
  const TOTAL = bank.current ? bank.current.length : 10; const PER = lvl([28, 20, 13], diff);
  const [idx, setIdx] = useState(0); const [score, setScore] = useState(0); const [time, setTime] = useState(PER);
  const [cur, setCur] = useState(() => nextQ()); const [picked, setPicked] = useState(null);
  const timer = useRef(null);
  useEffect(() => {
    setTime(PER); clearInterval(timer.current);
    timer.current = setInterval(() => setTime(x => { if (x <= 1) { clearInterval(timer.current); answer(null); } return x - 1; }), 1000);
    return () => clearInterval(timer.current);
  }, [idx]);
  function answer(v) {
    if (picked !== null) return; clearInterval(timer.current); setPicked(v);
    const ok = v === cur.ans; if (ok) { setScore(s => s + 10 + time * 2); Sound.correct(); } else { Sound.wrong(); Speech.lose(); }
    setTimeout(() => { const n = idx + 1; if (n >= TOTAL) onFinish(score + (ok ? 10 + time * 2 : 0)); else { setPicked(null); setCur(nextQ()); setIdx(n); } }, 850);
  }
  const cols = cur.opts.length > 3 ? '1fr 1fr' : '1fr 1fr 1fr';
  return (
    <Shell score={score} gear={false}>
      <div className="d-flex justify-content-between fw-bold mb-2" style={{ maxWidth: 560, width: '92%' }}>
        <span>📝 {idx + 1}/{TOTAL}</span><span>⏱️ {time}s</span><span>⭐ {score}</span>
      </div>
      <div className="quiz-bar"><i style={{ width: (time / PER * 100) + '%', background: time <= 5 ? '#fde047' : '#fff' }} /></div>
      <div className="player-flash quiz-q">{cur.q}{cur.eq === false ? '' : ' = ?'}</div>
      <div className="quiz-opts" style={{ gridTemplateColumns: cols }}>{cur.opts.map((o, i) => { let cls = 'quiz-opt'; if (picked !== null) { if (o === cur.ans) cls += ' ok'; else if (o === picked) cls += ' no'; } return <button key={i} className={cls} disabled={picked !== null} onClick={() => answer(o)}>{o}</button>; })}</div>
    </Shell>
  );
}

/* ============================================================ MEMORY */
const MEMO = ['🍎', '🚀', '🐱', '⭐', '🎈', '🐸', '🌸', '⚽', '🐶', '🦊', '🌈', '🍓'];
function Memory({ onFinish, diff }) {
  const pairs = lvl([6, 8, 10], diff);
  const cols = pairs >= 10 ? 5 : 4;
  const cell = pairs >= 10 ? 62 : pairs >= 8 ? 78 : 84;
  const [cards, setCards] = useState(() => { const set = shuffle(MEMO).slice(0, pairs); return shuffle([...set, ...set]).map((e, i) => ({ i, e, flip: false, done: false })); });
  const [sel, setSel] = useState([]); const [moves, setMoves] = useState(0); const lock = useRef(false);
  function flip(i) {
    if (lock.current) return; const c = cards[i]; if (c.flip || c.done) return; Sound.flip();
    const nc = cards.map(x => x.i === i ? { ...x, flip: true } : x); setCards(nc); const ns = [...sel, i]; setSel(ns);
    if (ns.length === 2) {
      setMoves(m => m + 1); lock.current = true; const [a, b] = ns;
      if (nc[a].e === nc[b].e) { Sound.correct(); setTimeout(() => { setCards(cs => cs.map(x => x.i === a || x.i === b ? { ...x, done: true } : x)); setSel([]); lock.current = false; win(a, b); }, 450); }
      else { setTimeout(() => { setCards(cs => cs.map(x => x.i === a || x.i === b ? { ...x, flip: false } : x)); setSel([]); lock.current = false; }, 800); }
    }
  }
  function win(a, b) { const done = cards.filter(x => x.done || x.i === a || x.i === b).length; if (done === cards.length) { const sc = Math.max(20, 200 - moves * 8); setTimeout(() => onFinish(sc), 500); } }
  return (
    <Shell score={moves} gear={false}>
      <div className="player-score">Yurishlar: {moves}</div>
      <div className="player-grid" style={{ gridTemplateColumns: `repeat(${cols},${cell}px)` }}>
        {cards.map(c => <button key={c.i} className="player-cell" onClick={() => flip(c.i)}
          style={{ background: c.done ? '#bbf7d0' : c.flip ? '#fff' : 'rgba(255,255,255,.35)', color: c.flip || c.done ? '#2b2b3a' : 'transparent' }}>
          {c.flip || c.done ? c.e : '?'}</button>)}
      </div>
    </Shell>
  );
}

/* ============================================================ NUMBER RECALL */
function NumRecall({ onFinish, diff }) {
  const ROUNDS = 6; const [round, setRound] = useState(0); const [score, setScore] = useState(0);
  const start = lvl([3, 4, 5], diff); const showK = lvl([1.25, 1, 0.78], diff);
  const [phase, setPhase] = useState('show'); const [num, setNum] = useState(''); const ref = useRef(null); const last = useRef(null);
  useEffect(() => { const len = start + Math.min(round, 5); let s = ''; for (let k = 0; k < len; k++) s += rnd(10); setNum(s); setPhase('show'); const tm = setTimeout(() => setPhase('input'), Math.round((900 + len * 130) * showK)); return () => clearTimeout(tm); }, [round]);
  function check() { const v = (ref.current.value || '').trim(); const ok = v === num; last.current = { ok, v }; if (ok) { setScore(s => s + 15 + round * 5); Sound.correct(); } else { Sound.wrong(); Speech.lose(); } setPhase('result'); }
  function next() { const r = round + 1; if (r >= ROUNDS) { onFinish(score); return; } setRound(r); }
  return (
    <Shell score={score} gear={false}>
      <div className="player-score">{round + 1}/{ROUNDS}</div>
      {phase === 'show' && <div className="player-flash" style={{ fontSize: 'min(20vh,120px)', letterSpacing: 12 }}>{num}</div>}
      {phase === 'input' && <><div className="player-title">Ko'rgan sonni yozing</div>
        <div className="player-answer"><input ref={ref} inputMode="numeric" autoFocus onKeyDown={e => e.key === 'Enter' && check()} /></div>
        <button className="player-startbtn mt-2" style={{ fontSize: 18, padding: '12px 30px' }} onClick={check}>Tekshirish</button></>}
      {phase === 'result' && <div className="player-result"><div style={{ fontSize: 48 }}>{last.current.ok ? '✅' : '❌'}</div><div className="eq" style={{ letterSpacing: 4 }}>{num}</div>{!last.current.ok && <div className="text-danger fw-bold">Sizniki: {last.current.v || '—'}</div>}<button className="player-startbtn mt-3" style={{ fontSize: 18, padding: '12px 26px' }} onClick={next}>{round + 1 >= ROUNDS ? '🏁 Yakun' : 'Keyingi →'}</button></div>}
    </Shell>
  );
}

/* ============================================================ WORD FLASH */
const WORDS = ['kitob', 'maktab', 'quyosh', 'daraxt', 'bola', 'olma', 'suv', 'non', 'gul', 'dengiz', 'yulduz', 'qalam', 'daftar', 'vatan', 'bahor'];
function WordFlash({ onFinish, diff }) {
  const ROUNDS = 8; const [round, setRound] = useState(0); const [score, setScore] = useState(0);
  const flashMs = lvl([900, 650, 430], diff); const optCount = lvl([3, 4, 5], diff);
  const [phase, setPhase] = useState('flash'); const [word, setWord] = useState(''); const [opts, setOpts] = useState([]); const [picked, setPicked] = useState(null);
  useEffect(() => { const w = WORDS[rnd(WORDS.length)]; setWord(w); setPhase('flash'); setPicked(null); setOpts(shuffle([w, ...shuffle(WORDS.filter(x => x !== w)).slice(0, optCount - 1)])); const tm = setTimeout(() => setPhase('pick'), flashMs); return () => clearTimeout(tm); }, [round]);
  function pick(o) { if (picked) return; setPicked(o); if (o === word) { setScore(s => s + 20); Sound.correct(); } else { Sound.wrong(); Speech.lose(); } setTimeout(() => { const r = round + 1; if (r >= ROUNDS) onFinish(score + (o === word ? 20 : 0)); else setRound(r); }, 700); }
  return (
    <Shell score={score} gear={false}>
      <div className="player-score">{round + 1}/{ROUNDS}</div>
      {phase === 'flash' ? <div className="player-flash" style={{ fontSize: 'min(14vh,80px)' }}>{word}</div>
        : <><div className="player-title">Qaysi so'zni ko'rdingiz?</div>
          <div className="quiz-opts">{opts.map(o => { let cls = 'quiz-opt'; if (picked) { if (o === word) cls += ' ok'; else if (o === picked) cls += ' no'; } return <button key={o} className={cls} style={{ fontSize: 20 }} disabled={!!picked} onClick={() => pick(o)}>{o}</button>; })}</div></>}
    </Shell>
  );
}

/* ============================================================ LETTER COUNT */
function LetterCount({ onFinish, diff }) {
  const ROUNDS = 6; const [round, setRound] = useState(0); const [score, setScore] = useState(0);
  const baseLen = lvl([6, 8, 11], diff); const showK = lvl([1.2, 1, 0.8], diff);
  const [phase, setPhase] = useState('show'); const [picked, setPicked] = useState(null); const [opts, setOpts] = useState([]); const d = useRef({});
  useEffect(() => {
    const L = 'ABEKMOPST'; const target = L[rnd(L.length)]; const len = baseLen + Math.min(round, 6); let str = '', cnt = 0;
    for (let k = 0; k < len; k++) { const c = L[rnd(L.length)]; str += c; if (c === target) cnt++; } if (cnt === 0) { str = target + str.slice(1); cnt = 1; } d.current = { str, target, cnt };
    const set = new Set([cnt]); let m = cnt; while (set.size < 4) { m++; set.add(m); } setOpts(shuffle([...set]).slice(0, 4)); setPhase('show'); setPicked(null);
    const tm = setTimeout(() => setPhase('ask'), Math.round((900 + len * 100) * showK)); return () => clearTimeout(tm);
  }, [round]);
  function pick(v) { if (picked !== null) return; setPicked(v); const ok = v === d.current.cnt; if (ok) { setScore(s => s + 15); Sound.correct(); } else { Sound.wrong(); Speech.lose(); } setTimeout(() => { const r = round + 1; if (r >= ROUNDS) onFinish(score + (ok ? 15 : 0)); else setRound(r); }, 650); }
  return (
    <Shell score={score} gear={false}>
      <div className="player-score">{round + 1}/{ROUNDS}</div>
      {phase === 'show' ? <div className="player-flash" style={{ fontSize: 'min(12vh,64px)', letterSpacing: 12 }}>{d.current.str}</div>
        : <><div className="player-title">«{d.current.target}» harfi nechta marta edi?</div>
          <div className="quiz-opts">{opts.map(o => { let cls = 'quiz-opt'; if (picked !== null) { if (o === d.current.cnt) cls += ' ok'; else if (o === picked) cls += ' no'; } return <button key={o} className={cls} disabled={picked !== null} onClick={() => pick(o)}>{o}</button>; })}</div></>}
    </Shell>
  );
}

/* ============================================================ SCHULTE */
function Schulte({ onFinish, diff }) {
  const cols = lvl([4, 5, 6], diff); const N = cols * cols; const cell = lvl([72, 66, 54], diff);
  const [nums] = useState(() => shuffle(Array.from({ length: N }, (_, i) => i + 1)));
  const [next, setNext] = useState(1); const [time, setTime] = useState(0); const [wrong, setWrong] = useState(null);
  const tm = useRef(null);
  useEffect(() => { tm.current = setInterval(() => setTime(t => t + 1), 1000); return () => clearInterval(tm.current); }, []);
  function tap(n) {
    if (n === next) { Sound.tick(); if (n === N) { clearInterval(tm.current); const sc = Math.max(30, N * 18 - time * 6); setTimeout(() => onFinish(sc), 300); } setNext(next + 1); }
    else { setWrong(n); Sound.wrong(); setTimeout(() => setWrong(null), 250); }
  }
  return (
    <Shell score={next - 1} gear={false}>
      <div className="d-flex justify-content-between fw-bold mb-2" style={{ maxWidth: 420, width: '92%' }}><span>Keyingi: <b>{next}</b></span><span>⏱️ {time}s</span></div>
      <div className="player-grid" style={{ gridTemplateColumns: `repeat(${cols},${cell}px)` }}>
        {nums.map(n => <button key={n} className="player-cell" style={{ fontSize: cell < 60 ? 18 : 22, background: n < next ? '#bbf7d0' : wrong === n ? '#fecaca' : 'rgba(255,255,255,.92)' }} onClick={() => tap(n)}>{n}</button>)}
      </div>
    </Shell>
  );
}

/* ============================================================ FIND DIFFERENT */
function FindDiff({ onFinish, diff }) {
  const ROUNDS = 6; const [round, setRound] = useState(0); const [score, setScore] = useState(0); const [d, setD] = useState(() => gen());
  function gen() { const map = { '🍎': '🍏', '🐱': '🐶', '⚽': '🏀', '🌟': '⭐', '🚗': '🚙', '🎈': '🎀' }; const ks = Object.keys(map); const base = ks[rnd(ks.length)]; const cols = lvl([3, 4, 5], diff); const n = cols * cols; const idx = rnd(n); return { cells: Array.from({ length: n }, (_, i) => i === idx ? map[base] : base), idx, cols }; }
  function tap(i) { if (i === d.idx) { Sound.correct(); const r = round + 1; setScore(s => s + 20); if (r >= ROUNDS) { onFinish(score + 20); return; } setRound(r); setD(gen()); } else Sound.wrong(); }
  return (
    <Shell score={score} gear={false}>
      <div className="player-score">{round + 1}/{ROUNDS} · Boshqacha belgini top</div>
      <div className="player-grid" style={{ gridTemplateColumns: `repeat(${d.cols},64px)` }}>
        {d.cells.map((c, i) => <button key={i} className="player-cell" style={{ fontSize: 30 }} onClick={() => tap(i)}>{c}</button>)}
      </div>
    </Shell>
  );
}

/* ============================================================ STROOP */
const SCOLORS = [['Qizil', '#e53935'], ['Yashil', '#43a047'], ["Ko'k", '#1e88e5'], ['Sariq', '#f9a825'], ['Binafsha', '#8e24aa']];
function Stroop({ onFinish, diff }) {
  const TOTAL = lvl([8, 12, 16], diff); const [i, setI] = useState(0); const [score, setScore] = useState(0); const [picked, setPicked] = useState(null);
  const [cur, setCur] = useState(() => ({ word: SCOLORS[rnd(5)], ink: SCOLORS[rnd(5)] }));
  function pick(c) { if (picked) return; setPicked(c); const ok = c[0] === cur.ink[0]; if (ok) { setScore(s => s + 15); Sound.correct(); } else { Sound.wrong(); Speech.lose(); } setTimeout(() => { const n = i + 1; if (n >= TOTAL) onFinish(score + (ok ? 15 : 0)); else { setPicked(null); setCur({ word: SCOLORS[rnd(5)], ink: SCOLORS[rnd(5)] }); setI(n); } }, 600); }
  return (
    <Shell score={score} gear={false}>
      <div className="player-score">{i + 1}/{TOTAL} · So'z YOZILGAN rangni tanlang</div>
      <div className="player-flash" style={{ fontSize: 'min(16vh,90px)', color: cur.ink[1] }}>{cur.word[0]}</div>
      <div className="quiz-opts" style={{ gridTemplateColumns: '1fr 1fr 1fr' }}>{SCOLORS.map(c => { let cls = 'quiz-opt'; if (picked) { if (c[0] === cur.ink[0]) cls += ' ok'; else if (c === picked) cls += ' no'; } return <button key={c[0]} className={cls} style={{ fontSize: 18 }} disabled={!!picked} onClick={() => pick(c)}>{c[0]}</button>; })}</div>
    </Shell>
  );
}

/* ============================================================ REACTION */
function Reaction({ onFinish, diff }) {
  const ROUNDS = lvl([4, 5, 6], diff); const base = lvl([100, 90, 80], diff); const kk = lvl([16, 12, 9], diff);
  const [round, setRound] = useState(0); const [att, setAtt] = useState(0); const [st, setSt] = useState('wait'); const [score, setScore] = useState(0); const t0 = useRef(0); const tm = useRef(null);
  useEffect(() => { setSt('wait'); tm.current = setTimeout(() => { setSt('go'); t0.current = Date.now(); }, 900 + rnd(2400)); return () => clearTimeout(tm.current); }, [round, att]);
  function click() {
    if (st === 'wait') { clearTimeout(tm.current); setSt('early'); }
    else if (st === 'early') { setAtt(a => a + 1); }
    else if (st === 'go') { const dt = Date.now() - t0.current; Sound.correct(); const sc = Math.max(5, base - Math.round(dt / kk)); const r = round + 1; if (r >= ROUNDS) { onFinish(score + sc); return; } setScore(s => s + sc); setRound(r); }
  }
  return (
    <Shell score={score} gear={false}>
      <div className="player-score">{round + 1}/{ROUNDS}</div>
      <button onClick={click} style={{ width: '70%', maxWidth: 480, height: 260, border: 0, borderRadius: 20, fontFamily: 'Fredoka', fontSize: 26, color: '#fff', cursor: 'pointer', background: st === 'go' ? '#22b07d' : st === 'early' ? '#ed1c24' : '#6b7280' }}>
        {st === 'wait' ? "Kuting… yashil bo'lganda bosing" : st === 'go' ? 'BOSING! 🟢' : 'Erta bosdingiz — qayta'}
      </button>
    </Shell>
  );
}

/* ============================================================ QIYINLIK TANLASH */
function DifficultyPicker({ onPick }) {
  const last = lastDiff();
  return (
    <div className="player">
      <div className="player-top">
        <a className="pbtn" href={window.BG_HOME} title="Chiqish"><i className="bi bi-house-door-fill" /></a>
        <span className="player-chip">{G.category_name || "O'yin"}</span>
        <span className="player-chip d-none d-md-inline">{G.name}</span>
        <span className="sp" />
        <button className="pbtn" onClick={toggleTheme} title="Mavzu"><i className="bi bi-brightness-high-fill" /></button>
        <button className="pbtn" onClick={fullscreen} title="To'liq ekran"><i className="bi bi-arrows-fullscreen" /></button>
      </div>
      <div className="player-body">
        <div className="player-stage">
          <div className={bgClass(true)} style={{ background: sceneFor() }}>
            {window.BG_BG_IMG && <img className="player-bg-photo" src={window.BG_BG_IMG} alt="" onError={e => { e.target.style.display = 'none'; }} />}
            <span className="player-bg-scrim" />
            <span className="pbg-a" /><span className="pbg-b" /><span className="pbg-c" />
          </div>
          <div className="diff-pick">
            <div className="diff-pick-icon">{G.icon || G.symbol || '🎮'}</div>
            <h2 className="diff-pick-title">{G.name}</h2>
            <p className="diff-pick-sub">Qiyinlik darajasini tanlang</p>
            <div className="diff-grid">
              {DIFFS.map(d => (
                <button key={d.id} type="button" className={'diff-card' + (d.id === last ? ' is-last' : '')}
                  style={{ '--dc': d.color }} onClick={() => onPick(d.id)}>
                  <span className="diff-card-icon">{d.icon}</span>
                  <span className="diff-card-name">{d.name}</span>
                  <span className="diff-card-desc">{d.desc}</span>
                  {d.id === last && <span className="diff-card-last">oxirgi tanlov</span>}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

/* ============================================================ ROOT */
function App() {
  const [finished, setFinished] = useState(null);
  const [diff, setDiff] = useState(null); // null = qiyinlik hali tanlanmagan
  openDiffPicker = () => { setFinished(null); setDiff(null); };
  const onFinish = s => setFinished(s);
  const choose = d => { localStorage.setItem('bg_difficulty', d); ACTIVE_DIFF = d; setDiff(d); };

  // Har bir tugma tanlashda "pufak" ovozi (global, React'dan keyin — bubble/passive)
  useEffect(() => {
    const h = e => { if (e.target && e.target.closest && e.target.closest('button')) Sound.pop(); };
    document.addEventListener('click', h, { passive: true });
    return () => document.removeEventListener('click', h);
  }, []);

  // O'yin davom etayotganda Kahoot uslubidagi fon musiqasi
  useEffect(() => {
    if (diff !== null && finished === null) Music.start(); else Music.stop();
    return () => Music.stop();
  }, [diff, finished]);

  if (diff === null) return <><Toasts /><DifficultyPicker onPick={choose} /></>;
  ACTIVE_DIFF = diff;
  if (finished !== null) return <><Toasts /><Finish score={finished} onAgain={() => setFinished(null)} /></>;
  const map = {
    forsaj: Mental, flash: Mental, kopaytir: Mental, columns: Columns, quiz: Quiz, subjectquiz: Quiz,
    memory: Memory, numrecall: NumRecall, wordflash: WordFlash, lettercount: LetterCount,
    schulte: Schulte, finddiff: FindDiff, stroop: Stroop, reaction: Reaction,
  };
  const C = map[G.kind] || Quiz;
  return <><Toasts /><C key={diff} onFinish={onFinish} diff={diff} /></>;
}

ReactDOM.createRoot(document.getElementById('player-root')).render(<App />);
