# UO キーバインド配置盤

Ultima Online (1998) のキーバインドを、**ビジュアルなキーボード盤面**と**一覧表**の両方で
管理できる、備忘録兼・配置検討ツールです。UOAssist の導入に合わせてキー配置を
再設計するための下敷きとして作りました。

`index.html` は単体で完結しており、GitHub Pages でもローカルの `file://` でも動きます。

## できること

- **キーボード盤面**（JIS / US 切り替え）に、各キーの割り当てを色分け表示
- **レイヤー（修飾キー）切り替え**：なし / Ctrl / Alt / Shift / Ctrl+Alt / Ctrl+Shift / Alt+Shift / Ctrl+Alt+Shift
  - 「そのまま押し」はファンクションや低頻度キー、修飾つきはスキル発動・スペル詠唱などを想定
- キーをクリックして**その場で編集**（アクション・分類・系統・メモ）
- **一覧表**：検索・分類/系統フィルタ・並べ替え（＝備忘録）
- **系統タグ**：`UOクライアント` のマクロと `UOAssist` のホットキーを区別・色分け
- **重複検出**：同じキー＋修飾に2つ割り当てると赤くハイライト
- **JSON 書出 / 読込**：バックアップ・共有・バージョン管理用
- **印刷**：盤面を隠して一覧表だけを紙／PDF に
- **Ctrl↔Alt 入れ替え**：取り込み時の修飾解釈が逆だった場合のワンタッチ修正

## データの保存場所

個人の割り当ては**ブラウザ内（localStorage）にのみ**保存されます。公開ページには乗りません。
別端末へ移す・バックアップする・リポジトリで版管理する場合は「JSON 書出」を使ってください。

## 初期データ（取り込み元）

`data/MACROS.TXT` … UO クライアント（2D）のマクロファイル。
`tools/parse_macros.py` でこれを解析し、`data/keybinds.default.json`（盤面の初期データ）を生成しています。

### 修飾フラグの解釈

`MACROS.TXT` の各エントリ先頭行は `<キー> <f1> <f2> <f3>`（f は 0/1）です。
このデータでは順序を **`f1=Ctrl, f2=Alt, f3=Shift`** と解釈しています。根拠：

- `0 0 1`（f3のみ）は Esc の緊急マクロ（Guards!! / i ban thee）だけに使われる → **f3 = Shift**（緊急用に温存）
- 2つ立つ `1 1 0` は「Ctrl+Alt+◯」に相当（例 `R 1 1 0` = Open Overview）→ **f1・f2 = Ctrl と Alt**
- 単独 `1 0 0` は全て CastSpell、`0 1 0` は全て UseSkill → 慣例どおり **f1=Ctrl（詠唱）/ f2=Alt（スキル）**

> もし実際の Ctrl / Alt が逆であれば、ツール上部の **「Ctrl↔Alt」** ボタンで全件まとめて入れ替えられます。
> （`tools/parse_macros.py` の `MOD_ORDER` を変えて再生成しても構いません）

## 再生成の手順

```sh
python3 tools/parse_macros.py data/MACROS.TXT data/keybinds.default.json
python3 tools/build.py    # keybinds.default.json を埋め込んだ index.html を生成
```

## GitHub Pages で公開したい場合

このリポジトリは既定で **private** です。Pages でホストする場合は
Settings → Pages で公開ブランチ（例：`main` / ルート）を指定してください。
無料プランで Pages を使うにはリポジトリを public にする必要があります。
ホストしなくても `index.html` をローカルで開けばそのまま使えます。

---

原文マクロは Ultima Online のゲーム内設定（Electronic Arts / Origin Systems）に由来します。
Ultima Online は Electronic Arts Inc. の商標です。
