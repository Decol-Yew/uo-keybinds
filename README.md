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

## データの流れ（端末間で同じ内容を表示）

- ページを開くと、リポジトリの **`data/keybinds.json`** を読み込んで表示します。
  → GitHub Pages で公開すれば、**どの端末で開いても同じ最新版**が出ます。
- ブラウザ上での編集は、その端末の **下書き（localStorage）** に保存されます（他端末には出ません）。
  上部のステータスバーが「未コミットの下書きを表示中」に変わります。
- 編集を**全端末へ反映**するには、
  1. 「**JSON 書出**」で `keybinds.json` をダウンロード
  2. それを `data/keybinds.json` として**コミット**（自分で push するか、内容を渡して反映してもらう）
  3. 各端末で再読込（または「**リポジトリ最新**」ボタン）
- 「**リポジトリ最新**」… 下書きを破棄してリポジトリの最新を取得
- 「**既定に戻す**」… 取り込み時の元データ（`keybinds.default.json`）に戻す

ローカルで `file://` で開いた場合はリポジトリを読めないため、埋め込みの初期データ＋その端末の下書きで動きます（オフライン表示）。

## 初期データ（取り込み元）

`data/MACROS.TXT` … UO クライアント（2D）のマクロファイル。
`tools/parse_macros.py` でこれを解析し、`data/keybinds.default.json`（元データ）を生成。
`data/keybinds.json` … ページが実際に読み込む**現行データ**（初期値は default のコピー。編集はここにコミットして更新する）。

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

## GitHub Pages で公開する（推奨・端末間同期のため）

端末をまたいで同じ内容を見るには Pages 公開が前提です。

1. リポジトリを **public** にする（無料プランで Pages を使う場合）
2. Settings → Pages → Source をブランチ `main` / `/ (root)` に設定
3. 数分後 `https://<ユーザー名>.github.io/uo-keybinds/` で開ける

ホストしない場合も `index.html` をローカルで開けば単体で使えます（この場合はオフライン表示）。

---

原文マクロは Ultima Online のゲーム内設定（Electronic Arts / Origin Systems）に由来します。
Ultima Online は Electronic Arts Inc. の商標です。
