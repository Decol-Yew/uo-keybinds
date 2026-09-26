#!/usr/bin/env python3
"""Generate index.html from data/keybinds.default.json.

The page is fully self-contained (the default data set is embedded inline) so
it works both on GitHub Pages and when opened as a local file:// document.
Run from the repository root::

    python3 tools/build.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "keybinds.default.json"
OUT = ROOT / "index.html"

TEMPLATE = r"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UO キーバインド配置盤</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=IM+Fell+English:ital@0;1&family=Shippori+Mincho:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{
  --gold:#c9a15a; --gold-soft:#e0c887; --paper:#e6d6ad; --ink:#3b2612;
  --bg:#151009; --panel:#211a10; --panel-2:#2b2115; --line:#4a3820;
  --text:#d8c9a3; --text-dim:#9a8a68; --text-faint:#6d5f45;
  --serif-en:"IM Fell English","Palatino Linotype",Georgia,serif;
  --serif-ja:"Shippori Mincho","Yu Mincho","Hiragino Mincho ProN","Noto Serif JP",serif;
  /* category colors */
  --c-spell:#8f7bff; --c-skill:#5bbd86; --c-say:#dcab4c; --c-command:#59b0d1;
  --c-uoassist:#d76b7f; --c-other:#9a8f7a;
}
*{box-sizing:border-box}
html,body{margin:0;min-height:100%}
body{
  background:#151009;
  background-image:
    radial-gradient(ellipse at 50% -10%, rgba(120,80,40,.30), rgba(0,0,0,0) 55%),
    url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .08 0'/></filter><rect width='200' height='200' filter='url(%23n)'/></svg>");
  color:var(--text); font-family:var(--serif-ja);
  padding:22px 16px 80px; line-height:1.5;
}
.wrap{max-width:1180px;margin:0 auto}
header.page{text-align:center;margin-bottom:18px}
header.page h1{font-family:var(--serif-en);font-weight:400;color:var(--gold);
  font-size:1.8rem;letter-spacing:.05em;margin:0}
header.page .sub{color:var(--text-dim);font-size:.9rem;margin-top:4px}
header.page .rule{width:200px;height:1px;margin:12px auto 0;
  background:linear-gradient(90deg,transparent,var(--gold),transparent);opacity:.6}

.toolbar{display:flex;flex-wrap:wrap;gap:10px 14px;align-items:center;
  justify-content:center;margin:16px 0 10px}
.group{display:flex;gap:6px;align-items:center;background:var(--panel);
  border:1px solid var(--line);border-radius:8px;padding:5px 8px}
.group .lbl{font-size:.72rem;color:var(--text-faint);letter-spacing:.04em;margin-right:2px}
button,select,input[type=text]{font-family:var(--serif-ja);color:var(--text);
  background:var(--panel-2);border:1px solid var(--line);border-radius:6px;
  padding:6px 10px;font-size:.85rem;cursor:pointer}
button:hover{border-color:var(--gold);color:var(--gold-soft)}
input[type=text]{cursor:text;min-width:150px}
select{cursor:pointer}
.btn-primary{background:linear-gradient(180deg,#5b4526,#3d2c14);border-color:var(--gold)}
.btn-danger:hover{border-color:#d76b7f;color:#e79aa8}

/* layer selector */
.layers{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;margin:6px 0 14px}
.layer-btn{position:relative;padding:7px 14px;font-size:.9rem;border-radius:7px}
.layer-btn.active{background:linear-gradient(180deg,#6f5227,#48331a);
  border-color:var(--gold);color:var(--gold-soft);box-shadow:0 0 0 1px var(--gold) inset}
.layer-btn .cnt{font-size:.68rem;color:var(--text-faint);margin-left:6px}
.layer-btn.active .cnt{color:var(--gold)}

/* keyboard */
.kb-scroll{overflow-x:auto;padding:4px 0 8px}
.keyboard{--u:46px;--gap:6px;display:inline-flex;flex-direction:column;gap:var(--gap);
  background:linear-gradient(180deg,#241a0f,#191207);border:1px solid var(--line);
  border-radius:12px;padding:14px;box-shadow:0 14px 30px rgba(0,0,0,.5),inset 0 1px 0 rgba(255,220,160,.06);
  min-width:min-content;margin:0 auto}
.kb-main{display:flex;gap:22px;align-items:flex-start}
.kb-section{display:flex;flex-direction:column;gap:var(--gap)}
.krow{display:flex;gap:var(--gap)}
.spacer{width:calc(var(--u)*var(--w,1) + (var(--w,1) - 1)*var(--gap))}
.key{
  width:calc(var(--u)*var(--w,1) + (var(--w,1) - 1)*var(--gap));
  height:var(--u);border-radius:7px;border:1px solid #4a3820;
  background:linear-gradient(180deg,#33281a,#241a10);
  color:var(--text-dim);position:relative;cursor:pointer;
  display:flex;flex-direction:column;justify-content:flex-start;
  padding:4px 5px;overflow:hidden;transition:transform .08s,border-color .12s;
  text-align:left;font-size:.7rem;line-height:1.05;
}
.key:hover{transform:translateY(-2px);border-color:var(--gold)}
.key .face{font-family:var(--serif-en);font-size:.72rem;color:var(--text);opacity:.85;
  letter-spacing:.02em;white-space:nowrap}
.key .val{margin-top:auto;font-size:.62rem;line-height:1.08;color:#efe4c4;
  display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.key.assigned{background:linear-gradient(180deg,#3a2c19,#2a2012)}
.key.assigned .face{opacity:.6;font-size:.62rem}
.key.mod{background:linear-gradient(180deg,#241d13,#1a140b);color:var(--text-faint);cursor:pointer}
.key.mod.on{border-color:var(--gold);color:var(--gold-soft);
  box-shadow:0 0 0 1px var(--gold) inset}
.key.conflict{border-color:#d76b7f !important;box-shadow:0 0 0 1px #d76b7f inset}
/* colored left bar by category */
.key.assigned::before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;
  background:var(--cat,transparent)}
/* dot: has binding in other layers */
.key .other{position:absolute;top:3px;right:4px;display:flex;gap:2px}
.key .other i{width:5px;height:5px;border-radius:50%;background:var(--od,#7a6a48);opacity:.85}

.cat-spell{--cat:var(--c-spell)} .cat-skill{--cat:var(--c-skill)}
.cat-say{--cat:var(--c-say)} .cat-command{--cat:var(--c-command)}
.cat-uoassist{--cat:var(--c-uoassist)} .cat-other{--cat:var(--c-other)}

/* legend */
.legend{display:flex;flex-wrap:wrap;gap:8px 16px;justify-content:center;
  margin:14px 0 4px;font-size:.78rem;color:var(--text-dim)}
.legend .chip{display:inline-flex;align-items:center;gap:6px}
.legend .sw{width:12px;height:12px;border-radius:3px;background:var(--cat)}
.hint{text-align:center;color:var(--text-faint);font-size:.76rem;margin-top:6px}

/* table */
.table-tools{display:flex;flex-wrap:wrap;gap:10px;align-items:center;
  justify-content:space-between;margin:26px 0 8px}
.table-tools h2{font-family:var(--serif-en);font-weight:400;color:var(--gold);
  font-size:1.15rem;margin:0}
.filters{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
table{width:100%;border-collapse:collapse;font-size:.84rem;
  background:var(--panel);border:1px solid var(--line);border-radius:8px;overflow:hidden}
th,td{padding:7px 10px;text-align:left;border-bottom:1px solid rgba(74,56,32,.5);vertical-align:top}
th{color:var(--gold-soft);font-weight:500;font-size:.76rem;letter-spacing:.03em;
  cursor:pointer;user-select:none;white-space:nowrap;background:var(--panel-2)}
th:hover{color:var(--gold)}
tr:hover td{background:rgba(201,161,90,.05)}
td.combo{font-family:var(--serif-en);color:var(--gold-soft);white-space:nowrap}
td.actions-cell{color:#efe4c4}
.badge{display:inline-block;font-size:.68rem;padding:1px 7px;border-radius:10px;
  border:1px solid var(--cat,var(--line));color:var(--cat,var(--text-dim));white-space:nowrap}
.src{font-size:.7rem;color:var(--text-faint)}
.src.uoassist{color:var(--c-uoassist)}
.row-actions button{padding:3px 8px;font-size:.72rem}
tr.conflict td{background:rgba(215,107,127,.10)}
.note-cell{color:var(--text-dim);font-size:.78rem;font-style:italic}
.empty-row td{text-align:center;color:var(--text-faint);padding:20px}

/* stats */
.stats{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin:14px 0}
.stat{background:var(--panel);border:1px solid var(--line);border-radius:8px;
  padding:8px 14px;text-align:center;min-width:92px}
.stat .n{font-family:var(--serif-en);font-size:1.3rem;color:var(--gold-soft)}
.stat .k{font-size:.7rem;color:var(--text-faint)}

/* editor modal */
.modal-bg{position:fixed;inset:0;background:rgba(10,7,3,.72);display:none;
  align-items:center;justify-content:center;z-index:50;padding:16px}
.modal-bg.show{display:flex}
.modal{background:linear-gradient(180deg,#2a2013,#1d1509);border:1px solid var(--gold);
  border-radius:12px;padding:22px;width:min(460px,100%);
  box-shadow:0 24px 60px rgba(0,0,0,.7)}
.modal h3{font-family:var(--serif-en);font-weight:400;color:var(--gold);margin:0 0 4px;font-size:1.2rem}
.modal .combo-preview{font-family:var(--serif-en);color:var(--gold-soft);font-size:1rem;margin-bottom:14px}
.field{margin-bottom:12px}
.field label{display:block;font-size:.74rem;color:var(--text-dim);margin-bottom:4px;letter-spacing:.03em}
.field textarea,.field select,.field input{width:100%;background:var(--panel-2);
  color:var(--text);border:1px solid var(--line);border-radius:6px;padding:8px;
  font-family:var(--serif-ja);font-size:.88rem}
.field textarea{min-height:64px;resize:vertical;font-family:var(--serif-en)}
.modal-actions{display:flex;gap:8px;justify-content:flex-end;margin-top:16px}
.modal-actions .spacer-fill{flex:1}

footer.page{text-align:center;color:var(--text-faint);font-size:.72rem;margin-top:40px;line-height:1.7}
a{color:var(--gold)}
.toast{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);
  background:var(--panel-2);border:1px solid var(--gold);color:var(--gold-soft);
  padding:9px 18px;border-radius:8px;font-size:.85rem;opacity:0;transition:opacity .3s;
  pointer-events:none;z-index:60}
.toast.show{opacity:1}
@media print{
  body{background:#fff;color:#000;padding:0}
  .toolbar,.layers,.modal-bg,.kb-scroll,.legend,.hint,.table-tools .filters,.row-actions,footer.page .noprint{display:none !important}
  th,td{border-color:#999}
}
@media (max-width:640px){
  .keyboard{--u:34px}
  header.page h1{font-size:1.4rem}
}
</style>
</head>
<body>
<div class="wrap">
  <header class="page">
    <h1>UO キーバインド配置盤</h1>
    <div class="sub">Ultima Online (1998) — 備忘録 &amp; 配置検討ボード</div>
    <div class="rule"></div>
  </header>

  <div class="toolbar">
    <div class="group">
      <span class="lbl">配列</span>
      <button id="layout-toggle" title="JIS / US を切り替え">JIS</button>
    </div>
    <div class="group">
      <input type="text" id="search" placeholder="検索(アクション/メモ/キー)">
    </div>
    <div class="group">
      <span class="lbl">分類</span>
      <select id="filter-cat">
        <option value="">すべて</option>
        <option value="spell">詠唱</option>
        <option value="skill">スキル</option>
        <option value="say">発話</option>
        <option value="command">操作</option>
        <option value="uoassist">UOAssist</option>
        <option value="other">その他</option>
      </select>
      <select id="filter-src">
        <option value="">系統すべて</option>
        <option value="client">UOクライアント</option>
        <option value="uoassist">UOAssist</option>
      </select>
    </div>
    <div class="group">
      <button id="add-btn" class="btn-primary">＋ 追加</button>
    </div>
    <div class="group">
      <span class="lbl">データ</span>
      <button id="export-btn">JSON書出</button>
      <button id="import-btn">読込</button>
      <input type="file" id="import-file" accept="application/json,.json" style="display:none">
      <button id="print-btn">印刷</button>
    </div>
    <div class="group">
      <button id="swap-btn" title="Ctrl と Alt の割り当てを全件入れ替え(取り込み時の解釈が逆だった場合)">Ctrl↔Alt</button>
      <button id="reset-btn" class="btn-danger" title="取り込んだ既定データに戻す">初期化</button>
    </div>
  </div>

  <div class="layers" id="layers"></div>

  <div class="kb-scroll">
    <div class="keyboard" id="keyboard"></div>
  </div>

  <div class="legend" id="legend"></div>
  <div class="hint">キーをクリックすると、現在のレイヤー(修飾キー)での割り当てを編集できます。修飾キー(Ctrl/Alt/Shift)を押すとレイヤーが切り替わります。右上の点は「他のレイヤーにも割り当てあり」の印です。</div>

  <div class="stats" id="stats"></div>

  <div class="table-tools">
    <h2>一覧(備忘録)</h2>
    <div class="filters">
      <span class="src" id="table-count"></span>
    </div>
  </div>
  <table id="table">
    <thead>
      <tr>
        <th data-sort="combo">組合せ</th>
        <th data-sort="key">キー</th>
        <th data-sort="category">分類</th>
        <th data-sort="source">系統</th>
        <th data-sort="actions">アクション</th>
        <th data-sort="note">メモ</th>
        <th></th>
      </tr>
    </thead>
    <tbody id="tbody"></tbody>
  </table>

  <footer class="page">
    <div>割り当てデータはこのブラウザ内(localStorage)にのみ保存されます。バックアップ・共有は「JSON書出」を使ってください。</div>
    <div class="noprint">取り込み元: UOクライアントの MACROS.TXT / 修飾フラグ順の解釈 = Ctrl, Alt, Shift。Ultima Online は Electronic Arts Inc. の商標です。</div>
  </footer>
</div>

<div class="modal-bg" id="modal-bg">
  <div class="modal">
    <h3 id="modal-title">割り当ての編集</h3>
    <div class="combo-preview" id="modal-combo"></div>
    <div class="field">
      <label for="f-actions">アクション(1行に1つ)</label>
      <textarea id="f-actions" placeholder="CastSpell Recall"></textarea>
    </div>
    <div class="field">
      <label for="f-cat">分類</label>
      <select id="f-cat">
        <option value="spell">詠唱 (CastSpell)</option>
        <option value="skill">スキル (UseSkill)</option>
        <option value="say">発話 (Say/Yell)</option>
        <option value="command">操作 (Open/War 他)</option>
        <option value="uoassist">UOAssist</option>
        <option value="other">その他</option>
      </select>
    </div>
    <div class="field">
      <label for="f-src">系統</label>
      <select id="f-src">
        <option value="client">UOクライアント</option>
        <option value="uoassist">UOAssist</option>
      </select>
    </div>
    <div class="field">
      <label for="f-note">メモ(任意)</label>
      <input type="text" id="f-note" placeholder="使用頻度・優先度・検討メモなど">
    </div>
    <div class="modal-actions">
      <button id="f-delete" class="btn-danger">削除</button>
      <span class="spacer-fill"></span>
      <button id="f-cancel">キャンセル</button>
      <button id="f-save" class="btn-primary">保存</button>
    </div>
  </div>
</div>

<div class="toast" id="toast"></div>

<script id="default-data" type="application/json">__DEFAULT_DATA__</script>
<script>
"use strict";
const DEFAULT_DATA = JSON.parse(document.getElementById('default-data').textContent);
const STORAGE_KEY = 'uo-keybinds:v1';
const MODS = ['ctrl','alt','shift'];
const CAT_LABEL = {spell:'詠唱',skill:'スキル',say:'発話',command:'操作',uoassist:'UOAssist',other:'その他'};
const CAT_ORDER = ['spell','skill','say','command','uoassist','other'];

/* ---- keyboard layouts ---- */
// item: [code, face, width]  |  {mod:'ctrl'|'alt'|'shift', face, w}  |  {sp:w} spacer
const FROW = [['Esc','Esc',1],{sp:0.5},['F1','F1',1],['F2','F2',1],['F3','F3',1],['F4','F4',1],{sp:0.4},
  ['F5','F5',1],['F6','F6',1],['F7','F7',1],['F8','F8',1],{sp:0.4},
  ['F9','F9',1],['F10','F10',1],['F11','F11',1],['F12','F12',1]];

const US_ROWS = [
  FROW,
  [['`','`',1],['1','1',1],['2','2',1],['3','3',1],['4','4',1],['5','5',1],['6','6',1],['7','7',1],['8','8',1],['9','9',1],['0','0',1],['-','-',1],['=','=',1],['Backspace','Back',2]],
  [['Tab','Tab',1.5],['Q','Q',1],['W','W',1],['E','E',1],['R','R',1],['T','T',1],['Y','Y',1],['U','U',1],['I','I',1],['O','O',1],['P','P',1],['[','[',1],[']',']',1],['\\','\\',1.5]],
  [['CapsLock','Caps',1.75],['A','A',1],['S','S',1],['D','D',1],['F','F',1],['G','G',1],['H','H',1],['J','J',1],['K','K',1],['L','L',1],[';',';',1],["'","'",1],['Enter','Enter',2.25]],
  [{mod:'shift',face:'Shift',w:2.25},['Z','Z',1],['X','X',1],['C','C',1],['V','V',1],['B','B',1],['N','N',1],['M','M',1],[',',',',1],['.','.',1],['/','/',1],{mod:'shift',face:'Shift',w:2.75}],
  [{mod:'ctrl',face:'Ctrl',w:1.5},{mod:'alt',face:'Alt',w:1.5},['Space','Space',6],{mod:'alt',face:'Alt',w:1.5},{mod:'ctrl',face:'Ctrl',w:1.5}]
];

const JIS_ROWS = [
  FROW,
  [['Zenkaku','半/全',1],['1','1',1],['2','2',1],['3','3',1],['4','4',1],['5','5',1],['6','6',1],['7','7',1],['8','8',1],['9','9',1],['0','0',1],['-','-',1],['^','^',1],['\\','¥',1],['Backspace','Back',1]],
  [['Tab','Tab',1.5],['Q','Q',1],['W','W',1],['E','E',1],['R','R',1],['T','T',1],['Y','Y',1],['U','U',1],['I','I',1],['O','O',1],['P','P',1],['@','@',1],['[','[',1],['Enter','Enter',1.5]],
  [['CapsLock','英数',1.75],['A','A',1],['S','S',1],['D','D',1],['F','F',1],['G','G',1],['H','H',1],['J','J',1],['K','K',1],['L','L',1],[';',';',1],[':',':',1],[']',']',1]],
  [{mod:'shift',face:'Shift',w:2.25},['Z','Z',1],['X','X',1],['C','C',1],['V','V',1],['B','B',1],['N','N',1],['M','M',1],[',',',',1],['.','.',1],['/','/',1],['Ro','ろ',1],{mod:'shift',face:'Shift',w:1.75}],
  [{mod:'ctrl',face:'Ctrl',w:1.5},{mod:'alt',face:'Alt',w:1.25},['Muhenkan','無変換',1.25],['Space','Space',3],['Henkan','変換',1.25],['Kana','かな',1.25],{mod:'alt',face:'Alt',w:1.25},{mod:'ctrl',face:'Ctrl',w:1.25}]
];

const NUMPAD = [
  [['NumLock','Num',1],['Num /','/',1],['Num *','*',1],['Num -','-',1]],
  [['Num 7','7',1],['Num 8','8',1],['Num 9','9',1],['Num +','+',1]],
  [['Num 4','4',1],['Num 5','5',1],['Num 6','6',1],{sp:1}],
  [['Num 1','1',1],['Num 2','2',1],['Num 3','3',1],['Num Enter','Ent',1]],
  [['Num 0','0',2],['Num .','.',1],{sp:1}]
];

/* ---- state ---- */
let state = load();
let layout = localStorage.getItem('uo-keybinds:layout') || 'JIS';
let curLayer = {ctrl:false,alt:false,shift:false};
let sortKey = 'combo', sortDir = 1;
let editing = null; // {index} or {key,mods} for new

function load(){
  try{
    const raw = localStorage.getItem(STORAGE_KEY);
    if(raw) return JSON.parse(raw);
  }catch(e){}
  return deepClone(DEFAULT_DATA);
}
function save(){
  try{ localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); }catch(e){}
}
function deepClone(o){ return JSON.parse(JSON.stringify(o)); }

/* ---- helpers ---- */
function modsEqual(a,b){ return MODS.every(m => !!a[m] === !!b[m]); }
function comboString(key, mods){
  const parts = MODS.filter(m=>mods[m]).map(m=>m[0].toUpperCase()+m.slice(1));
  parts.push(key);
  return parts.join('+');
}
function layerLabel(mods){
  const parts = MODS.filter(m=>mods[m]).map(m=>({ctrl:'Ctrl',alt:'Alt',shift:'Shift'}[m]));
  return parts.length ? parts.join('+') : 'なし(そのまま押し)';
}
function findBinding(key, mods){
  return state.bindings.findIndex(b => b.key===key && modsEqual(b.mods,mods));
}
function bindingsForKeyOtherLayers(key){
  return state.bindings.filter(b => b.key===key && !modsEqual(b.mods,curLayer));
}

/* ---- layer bar ---- */
const LAYER_DEFS = [
  {ctrl:false,alt:false,shift:false},
  {ctrl:true,alt:false,shift:false},
  {ctrl:false,alt:true,shift:false},
  {ctrl:false,alt:false,shift:true},
  {ctrl:true,alt:true,shift:false},
  {ctrl:true,alt:false,shift:true},
  {ctrl:false,alt:true,shift:true},
  {ctrl:true,alt:true,shift:true},
];
function renderLayers(){
  const el = document.getElementById('layers');
  el.innerHTML = '';
  LAYER_DEFS.forEach(def=>{
    const n = state.bindings.filter(b=>modsEqual(b.mods,def)).length;
    const btn = document.createElement('button');
    btn.className = 'layer-btn' + (modsEqual(def,curLayer)?' active':'');
    btn.innerHTML = escapeHtml(layerLabel(def)) + '<span class="cnt">'+n+'</span>';
    btn.onclick = ()=>{ curLayer = {...def}; renderAll(); };
    el.appendChild(btn);
  });
}

/* ---- keyboard ---- */
function renderKeyboard(){
  const kb = document.getElementById('keyboard');
  kb.innerHTML='';
  const main = document.createElement('div'); main.className='kb-main';
  const left = document.createElement('div'); left.className='kb-section';
  const rows = layout==='JIS' ? JIS_ROWS : US_ROWS;
  rows.forEach(r=>left.appendChild(buildRow(r)));
  main.appendChild(left);
  const pad = document.createElement('div'); pad.className='kb-section';
  // align numpad with the rows below the function row
  const padSpacerRow = document.createElement('div'); padSpacerRow.className='krow';
  const sp = document.createElement('div'); sp.className='spacer'; sp.style.setProperty('--w','1'); sp.style.height='1px';
  padSpacerRow.appendChild(sp); pad.appendChild(padSpacerRow);
  NUMPAD.forEach(r=>pad.appendChild(buildRow(r)));
  main.appendChild(pad);
  kb.appendChild(main);
}
function buildRow(items){
  const row = document.createElement('div'); row.className='krow';
  items.forEach(it=>{
    if(it.sp!==undefined){
      const s=document.createElement('div'); s.className='spacer'; s.style.setProperty('--w',it.sp); row.appendChild(s); return;
    }
    if(it.mod){
      const k=document.createElement('div');
      k.className='key mod'+(curLayer[it.mod]?' on':'');
      k.style.setProperty('--w',it.w);
      k.innerHTML='<span class="face">'+escapeHtml(it.face)+'</span>';
      k.onclick=()=>{ curLayer={...curLayer,[it.mod]:!curLayer[it.mod]}; renderAll(); };
      row.appendChild(k); return;
    }
    const [code,face,w]=it;
    const k=document.createElement('div');
    k.className='key'; k.style.setProperty('--w',w||1);
    const idx=findBinding(code,curLayer);
    let inner='<span class="face">'+escapeHtml(face)+'</span>';
    if(idx>=0){
      const b=state.bindings[idx];
      k.classList.add('assigned','cat-'+b.category);
      if(isConflict(idx)) k.classList.add('conflict');
      inner+='<span class="val">'+escapeHtml(shortActions(b.actions))+'</span>';
    }
    const others=bindingsForKeyOtherLayers(code);
    if(others.length){
      const seen=new Set(); let dots='';
      others.forEach(o=>{ if(!seen.has(o.category)){seen.add(o.category);
        dots+='<i style="--od:var(--c-'+o.category+')"></i>';}});
      inner+='<span class="other">'+dots+'</span>';
    }
    k.innerHTML=inner;
    k.onclick=()=>openEditor(code,curLayer);
    row.appendChild(k);
  });
  return row;
}
function shortActions(a){ return (a&&a.length)?a.join(' / '):''; }

/* ---- conflicts ---- */
function isConflict(index){
  const b=state.bindings[index];
  return state.bindings.some((o,i)=> i!==index && o.key===b.key && modsEqual(o.mods,b.mods));
}

/* ---- legend & stats ---- */
function renderLegend(){
  const el=document.getElementById('legend'); el.innerHTML='';
  CAT_ORDER.forEach(c=>{
    const chip=document.createElement('span'); chip.className='chip cat-'+c;
    chip.innerHTML='<span class="sw" style="background:var(--cat)"></span>'+CAT_LABEL[c];
    el.appendChild(chip);
  });
}
function renderStats(){
  const el=document.getElementById('stats'); el.innerHTML='';
  const total=state.bindings.length;
  const counts={}; CAT_ORDER.forEach(c=>counts[c]=0);
  state.bindings.forEach(b=>{counts[b.category]=(counts[b.category]||0)+1;});
  const items=[['合計',total]];
  CAT_ORDER.forEach(c=>{ if(counts[c]) items.push([CAT_LABEL[c],counts[c]]); });
  items.forEach(([k,n])=>{
    const s=document.createElement('div'); s.className='stat';
    s.innerHTML='<div class="n">'+n+'</div><div class="k">'+escapeHtml(k)+'</div>';
    el.appendChild(s);
  });
}

/* ---- table ---- */
function renderTable(){
  const tbody=document.getElementById('tbody'); tbody.innerHTML='';
  const q=document.getElementById('search').value.trim().toLowerCase();
  const fc=document.getElementById('filter-cat').value;
  const fs=document.getElementById('filter-src').value;
  let rows=state.bindings.map((b,i)=>({b,i}));
  rows=rows.filter(({b})=>{
    if(fc && b.category!==fc) return false;
    if(fs && (b.source||'client')!==fs) return false;
    if(q){
      const hay=(comboString(b.key,b.mods)+' '+(b.actions||[]).join(' ')+' '+(b.note||'')).toLowerCase();
      if(!hay.includes(q)) return false;
    }
    return true;
  });
  rows.sort((x,y)=>cmp(x.b,y.b)*sortDir);
  document.getElementById('table-count').textContent=rows.length+' / '+state.bindings.length+' 件';
  if(!rows.length){
    tbody.innerHTML='<tr class="empty-row"><td colspan="7">該当なし</td></tr>'; return;
  }
  rows.forEach(({b,i})=>{
    const tr=document.createElement('tr');
    if(isConflict(i)) tr.className='conflict';
    const src=b.source||'client';
    tr.innerHTML=
      '<td class="combo">'+escapeHtml(comboString(b.key,b.mods))+'</td>'+
      '<td>'+escapeHtml(b.key)+'</td>'+
      '<td><span class="badge cat-'+b.category+'" style="--cat:var(--c-'+b.category+')">'+CAT_LABEL[b.category]+'</span></td>'+
      '<td><span class="src '+(src==='uoassist'?'uoassist':'')+'">'+(src==='uoassist'?'UOAssist':'Client')+'</span></td>'+
      '<td class="actions-cell">'+escapeHtml((b.actions||[]).join(' / '))+'</td>'+
      '<td class="note-cell">'+escapeHtml(b.note||'')+'</td>'+
      '<td class="row-actions"><button data-edit="'+i+'">編集</button></td>';
    tr.querySelector('[data-edit]').onclick=()=>openEditorByIndex(i);
    tbody.appendChild(tr);
  });
}
function cmp(a,b){
  let va,vb;
  if(sortKey==='combo'){ va=comboString(a.key,a.mods); vb=comboString(b.key,b.mods); }
  else if(sortKey==='actions'){ va=(a.actions||[]).join(' '); vb=(b.actions||[]).join(' '); }
  else if(sortKey==='note'){ va=a.note||''; vb=b.note||''; }
  else { va=a[sortKey]||''; vb=b[sortKey]||''; }
  return String(va).localeCompare(String(vb),'ja');
}

/* ---- editor ---- */
function openEditor(key,mods){
  const idx=findBinding(key,mods);
  editing = idx>=0 ? {index:idx} : {key, mods:{...mods}};
  const b = idx>=0 ? state.bindings[idx] : {key,mods:{...mods},actions:[],category:guessCat(mods),source:'client',note:''};
  document.getElementById('modal-title').textContent = idx>=0?'割り当ての編集':'新規割り当て';
  document.getElementById('modal-combo').textContent = comboString(key,mods)+'  （'+layerLabel(mods)+'）';
  document.getElementById('f-actions').value = (b.actions||[]).join('\n');
  document.getElementById('f-cat').value = b.category||'other';
  document.getElementById('f-src').value = b.source||'client';
  document.getElementById('f-note').value = b.note||'';
  document.getElementById('f-delete').style.display = idx>=0?'':'none';
  document.getElementById('modal-bg').classList.add('show');
  document.getElementById('f-actions').focus();
}
function openEditorByIndex(i){
  const b=state.bindings[i];
  curLayer={...b.mods};
  openEditor(b.key,b.mods);
}
function guessCat(mods){
  if(mods.ctrl && !mods.alt && !mods.shift) return 'spell';
  if(mods.alt && !mods.ctrl && !mods.shift) return 'skill';
  return 'command';
}
function closeEditor(){ document.getElementById('modal-bg').classList.remove('show'); editing=null; }
function saveEditor(){
  const actions=document.getElementById('f-actions').value.split('\n').map(s=>s.trim()).filter(Boolean);
  const cat=document.getElementById('f-cat').value;
  const src=document.getElementById('f-src').value;
  const note=document.getElementById('f-note').value.trim();
  if(!actions.length){ toast('アクションを入力してください'); return; }
  if(editing.index!==undefined){
    const b=state.bindings[editing.index];
    b.actions=actions; b.category=cat; b.source=src; b.note=note;
  }else{
    state.bindings.push({key:editing.key,mods:{...editing.mods},actions,category:cat,source:src,note});
  }
  save(); closeEditor(); renderAll(); toast('保存しました');
}
function deleteEditor(){
  if(editing.index!==undefined){
    state.bindings.splice(editing.index,1);
    save(); closeEditor(); renderAll(); toast('削除しました');
  }else closeEditor();
}

/* ---- toolbar actions ---- */
function exportJSON(){
  state.meta = state.meta || {};
  state.meta.exported = new Date().toISOString().slice(0,10);
  const blob=new Blob([JSON.stringify(state,null,2)],{type:'application/json'});
  const a=document.createElement('a');
  a.href=URL.createObjectURL(blob);
  a.download='uo-keybinds.json';
  a.click(); URL.revokeObjectURL(a.href);
  toast('JSONを書き出しました');
}
function importJSON(file){
  const r=new FileReader();
  r.onload=()=>{
    try{
      const d=JSON.parse(r.result);
      if(!d.bindings||!Array.isArray(d.bindings)) throw new Error('bindings がありません');
      state=d; save(); renderAll(); toast('読み込みました('+d.bindings.length+'件)');
    }catch(e){ toast('読み込み失敗: '+e.message); }
  };
  r.readAsText(file);
}
function swapCtrlAlt(){
  if(!confirm('全ての割り当てで Ctrl と Alt を入れ替えます。よろしいですか?')) return;
  state.bindings.forEach(b=>{ const t=b.mods.ctrl; b.mods.ctrl=b.mods.alt; b.mods.alt=t; });
  save(); renderAll(); toast('Ctrl と Alt を入れ替えました');
}
function resetData(){
  if(!confirm('取り込んだ既定データに戻します。現在の編集内容は失われます。よろしいですか?')) return;
  state=deepClone(DEFAULT_DATA); save(); renderAll(); toast('初期化しました');
}

/* ---- misc ---- */
function escapeHtml(s){ return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
let toastTimer;
function toast(msg){
  const t=document.getElementById('toast'); t.textContent=msg; t.classList.add('show');
  clearTimeout(toastTimer); toastTimer=setTimeout(()=>t.classList.remove('show'),1800);
}

function renderAll(){ renderLayers(); renderKeyboard(); renderLegend(); renderStats(); renderTable(); }

/* ---- wire up ---- */
document.getElementById('layout-toggle').onclick=function(){
  layout = layout==='JIS'?'US':'JIS';
  this.textContent=layout;
  localStorage.setItem('uo-keybinds:layout',layout);
  renderKeyboard();
};
document.getElementById('layout-toggle').textContent=layout;
document.getElementById('search').oninput=renderTable;
document.getElementById('filter-cat').onchange=renderTable;
document.getElementById('filter-src').onchange=renderTable;
document.getElementById('add-btn').onclick=()=>openEditor('',{...curLayer});
document.getElementById('export-btn').onclick=exportJSON;
document.getElementById('import-btn').onclick=()=>document.getElementById('import-file').click();
document.getElementById('import-file').onchange=function(){ if(this.files[0]) importJSON(this.files[0]); this.value=''; };
document.getElementById('print-btn').onclick=()=>window.print();
document.getElementById('swap-btn').onclick=swapCtrlAlt;
document.getElementById('reset-btn').onclick=resetData;
document.getElementById('f-save').onclick=saveEditor;
document.getElementById('f-cancel').onclick=closeEditor;
document.getElementById('f-delete').onclick=deleteEditor;
document.getElementById('modal-bg').onclick=(e)=>{ if(e.target.id==='modal-bg') closeEditor(); };
document.addEventListener('keydown',(e)=>{ if(e.key==='Escape') closeEditor(); });
document.querySelectorAll('th[data-sort]').forEach(th=>{
  th.onclick=()=>{ const k=th.dataset.sort; if(sortKey===k) sortDir*=-1; else {sortKey=k;sortDir=1;} renderTable(); };
});

renderAll();
</script>
</body>
</html>
"""


def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    payload = json.dumps(data, ensure_ascii=False)
    # keep it safe inside a <script> block
    payload = payload.replace("</", "<\\/")
    html = TEMPLATE.replace("__DEFAULT_DATA__", payload)
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT} ({len(html)} bytes, {len(data['bindings'])} bindings)")


if __name__ == "__main__":
    main()
