# japanese-web-design

日本語のWebサイト・LP・UIをデザインするためのClaude Skillです。「散文型」（日本語の文字組み・判断原則）と「データ型」（業種25分類×サイトタイプ9分類の実測デザインデータ）のハイブリッド構成になっています。

## これは何か

汎用のデザインSkillは欧文（主に英語）を前提に作られていることが多く、禁則処理・約物のアキ・和欧混植・明朝ゴシックの使い分けといった日本語特有の文字組みルールが抜け落ちています。また、AIに「上品に」「かっこよく」のような抽象的な指示だけを与えると、学習データの中でもっとも"それっぽい"平均的なデザインに収束しがちです（いわゆる「AIっぽさ」）。

このSkillは、この2つの問題に対応します。

1. **日本語の文字組み原則**（`references/principles.md`）— 縦組（縦書き）という選択肢、行末の孤立文字（泣き別れ）を防ぐ実装ルールを含む
2. **業種別の実測デザインデータ**（`data/*.csv`）— 実在する日本語Webデザインギャラリーサイトを分析し、業種25分類×サイトタイプ9分類ごとに、実際のデザイン傾向（配色・フォント・トーン・レイアウト）を数値化したもの
3. **業種を問わない一般デザイン原則**（`references/general-design-principles.md`）— 近接・整列・強弱・反復、配色比率、タイポグラフィ基本、モーションの節度（スクロール連動フェードインの具体的なCSS/JS実装例・実測値つき）、UIライティング、計画→レビュー→実装→批評の進め方。Anthropicの`frontend-design` Skillと一般的なWebデザイン解説記事、実在サイトのCSS実測を参考に構成

さらに、同じ業種について「moderate（堅実・王道）」と「bold（大胆・実験的）」という2つの参照点を持たせているのが特徴です（6業種で対応済み、詳細は下記）。

このSkillを作ろうと思ったきっかけは、日本語の縦組（縦書き）タイポグラフィでした。Webでは横組が圧倒的多数派のため、縦組を使うだけで際立った特徴になります。明朝体の縦組は気品・高級感を、ゴシック体の縦組は素直な可愛らしさ・誠実さを伝えやすく、短い日本語コピーがある場面では縦組も選択肢に入れて検討する価値があります。このSkillでは、縦組を効果的に使っている14サイトを実測し、`references/principles.md`の判断基準と`data/vertical_writing_examples.csv`のデータに反映しています。

## インストール方法

このリポジトリを clone し、`.claude/skills/japanese-web-design/` フォルダをそのまま自分のプロジェクトの `.claude/skills/` 以下にコピーしてください。Claude Codeであれば、プロジェクトルートに `.claude/skills/japanese-web-design/SKILL.md` が存在すれば自動的に認識されます。

```bash
git clone https://github.com/<your-account>/japanese-web-design-skill.git
cp -r japanese-web-design-skill/.claude/skills/japanese-web-design /path/to/your-project/.claude/skills/
```

## 使い方

日本語のWebサイト・LP・UIのデザイン/実装/レビューを依頼すると、Skillが自動的に発動します（`description` にトリガー条件を記載しています）。動作の流れは `SKILL.md` に記載の通りで、大まかには以下の順です。

1. `references/principles.md` を読み、日本語の文字組み原則を確認
2. 依頼内容から業種（25分類）とサイトタイプ（9分類）を特定
3. 該当する `data/` 以下のCSVを参照し、実測の配色・フォント・トーンを取得
4. moderate（堅実）/ bold（大胆）のどちらに寄せるかを判断
5. 具体的な数値・実例を根拠として提示しながらデザイン案を生成

## データの構成

| ファイル | 内容 |
|---|---|
| `data/industry_taxonomy.csv` | 業種25分類のマスタ（id・slug・名称・件数） |
| `data/type_taxonomy.csv` | サイトタイプ9分類のマスタ |
| `data/industry_type_matrix.csv` | 業種×タイプの実件数クロス集計 |
| `data/industry_keywords_moderate.csv` | 業種×デザインキーワード（12項目）の出現率％ |
| `data/industry_tone_moderate.csv` | 業種×配色トーン（12項目）の出現率％ |
| `data/type_keywords_moderate.csv` | サイトタイプ×デザインキーワードの出現率％ |
| `data/boldness_moderate_vs_bold.csv` | 6業種限定。moderate/boldの実測値比較 |
| `data/css_reference_examples.csv` | 6業種×3サイトの実測CSS値（色hex・font-family・角丸など） |
| `data/css_reference_examples_pilot20.csv` | 20サイトの実測CSS値・投稿者コメント |
| `data/vertical_writing_examples.csv` | 縦組（`writing-mode: vertical-rl`）を効果的に使っている14サイトの実測値（font-family・font-size・letter-spacing・line-height・font-weight・使用範囲・本人コメント） |

moderate/bold双方のデータが揃っているのは現時点で以下6業種のみです: 不動産・建築・空間・施設、ウェディング、暮らし商品・サービス、アート、美容、IT・システム。それ以外の19業種はmoderate（choooodoii由来）のデータのみとなります。

## スクリプト

| ファイル | 内容 |
|---|---|
| `scripts/hero_text_zone.py` | ヒーロー画像の中で文字（縦組・横組コピー）を乗せるのに適したエリア（情報密度が低く、コントラストを確保しやすい場所）を検出するPythonスクリプト。`pip install pillow numpy` が必要。使い方は `SKILL.md` ステップ5を参照 |

## データの出典と利用について

`data/`以下のCSVは、以下2つの日本語Webデザインギャラリーサイトを分析対象として作成しました。

- [choooodoii.com](https://choooodoii.com/) — バランスの取れた、着実に実装された良質サイトを集めたギャラリー（WordPress公式REST APIの`design`/`tone`タクソノミーを利用し、2,080件の母集団を集計）
- [81-web.com](https://81-web.com/) — 大胆なレイアウト・実験的な表現に振ったサイトを集めたギャラリー（サイト内検索機能が呼んでいる内部APIエンドポイントを利用し、6業種1,401件を集計）

取得したのは、各サイトが自ら付与している分類ラベル（業種・サイトタイプ・トーン・配色・フォント名など）とその集計値、および実サイト自体の公開されたCSS（`getComputedStyle`による実測）です。両サイトのサムネイル画像やキュレーターの紹介文をそのまま複製・転載したものはこのリポジトリに含まれていません。両サイトの`robots.txt`も確認していますが、この用途を明示的に制限する記述はありませんでした。

こうした集計・分析目的での利用は日本の著作権法30条の4（情報解析のための利用）の範囲内と理解していますが、法的な最終判断について保証するものではありません。もし両サイトの運営者の方でこのリポジトリの内容についてご懸念があれば、Issueを立てるか、リポジトリオーナーまでご連絡ください。対応いたします。

### 縦組（縦書き）データについて

`data/vertical_writing_examples.csv` は、上記2サイトとは別に、プロジェクトオーナーが個別に選定した14の実在サイト（企業・店舗・教育機関・神社などの公式サイト）を対象としています。各サイトについて取得したのは、縦組テキスト要素の`getComputedStyle`による計測値（font-family・font-size・letter-spacing・line-height・font-weight）のみで、識別のためのごく短いテキストサンプル（数文字〜1行程度の見出し）をCSVに含めていますが、画像・デザイン全体・本文の複製や転載は行っていません。個別サイトの`robots.txt`の網羅的な確認は行っていませんが、通常の閲覧と同じ方法（ブラウザでページを開き、公開されているCSSを読み取る）でのアクセスに留めています。こちらについても、掲載サイトの運営者の方でご懸念があれば、Issueを立てるか、リポジトリオーナーまでご連絡ください。対応いたします。

## ライセンス

MIT License（`LICENSE`参照）。`data/`以下の集計データの再配布・改変も、出典（choooodoii.com / 81-web.com）を明記いただければ自由に行っていただいて構いません。

## 制作の経緯

このSkillを作る過程は、以下のQiita記事にまとめています。

- 前編: Claude Skillの仕組みと実例解剖
- 中編: 業種別デザインデータの基盤構築
- 後編: 本Skillの実装とここまでの振り返り（本リポジトリ）
