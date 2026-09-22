---
name: japanese-web-design
description: Use when designing, building, or reviewing a Japanese-language website, landing page, or UI — encodes Japanese typography rules (kinsoku, mixed-script spacing, mincho/gothic choice, vertical writing/縦組) plus real measured design data (color, font, tone, layout type) by 25 industry categories and 9 site types, sourced from curated Japanese design galleries, with both a "moderate" and a "bold" reference point per industry to avoid generic AI-looking output.
---

# 日本語Webデザイン Skill

このSkillは、散文型（判断原則）とデータ型（実測データ）のハイブリッドです。日本語のWebサイト・LP・UIをデザイン、実装、レビューするときに使ってください。

## 使い方（必ずこの順で実行する）

### ステップ1: 原則を読む

`references/principles.md` を読む。日本語の文字組み（禁則処理・約物のアキ・和欧混植・字間行間・明朝ゴシックの使い分け・全角半角・行末の孤立文字/泣き別れ防止）、縦組（縦書き）という選択肢、「AIっぽさ」を避けるための判断原則（陥りやすい定番パターンのチェックリスト含む）、moderate/boldダイアルの考え方が書かれている。ファイルは軽量なので、日本語デザインタスクでは毎回読んでよい。

新規にページ全体をレイアウトするとき、またはステップ7の最終確認のときは、業種を問わない一般原則（近接・整列・強弱・反復、配色比率、タイポグラフィ基本、モーションの節度、UIライティング）をまとめた `references/general-design-principles.md` も参照する。

### ステップ2: ブリーフから業種とタイプを特定する

ユーザーの依頼内容（業種、サイトの目的）を読み取り、`data/industry_taxonomy.csv`（25業種）と `data/type_taxonomy.csv`（9タイプ）の中から最も近いものを選ぶ。この2つのファイルは固定の制御語彙になっているので、検索アルゴリズムは不要。ファイルを直接読んで、該当する行を目視で選ぶだけでよい。

- 業種の例: 美容、IT・システム、不動産・建築・空間・施設、ウェディング、飲食・食品・飲料 など25種類
- タイプの例: コーポレートサイト、商品・製品紹介、店舗・施設紹介、サービス紹介、特設・キャンペーンサイト、EC・WEBサービス、メディア・ポータル、採用サイト、ポートフォリオ

ぴったり一致するものがなければ、最も性質が近いものを選び、その判断根拠を一言添える。

### ステップ3: 該当業種のデータを引く

特定した業種で、以下のCSVから該当行をフィルタする（pandasでもgrepでも、ファイルが小さいので全部読み込んでもよい）。

| ファイル | 内容 |
|---|---|
| `data/industry_keywords_moderate.csv` | 業種×デザインキーワード（シンプル・上品・にぎやか・高級リッチ等12項目）の出現率％。choooodoii.com 2,080件の母集団統計。 |
| `data/industry_tone_moderate.csv` | 業種×配色トーン（鮮やか・深い・くすんだ・渋い等12項目）の出現率％。同上。 |
| `data/type_keywords_moderate.csv` | サイトタイプ（9分類）×デザインキーワードの出現率％。業種が特定しづらい場合の補助データ。 |
| `data/industry_type_matrix.csv` | 業種×タイプの実件数クロス集計。その業種でどのサイトタイプが主流かを確認できる。 |
| `data/boldness_moderate_vs_bold.csv` | 6業種限定。choooodoii（moderate）と81-web（bold）の実測値比較（黒率・カラフル率・動きタグ保有率・キャンペーン型比率など）。 |
| `data/css_reference_examples.csv` | 6業種×3サイトの実測CSS値（背景色hex・文字色hex・font-family・ボタン角丸・動画/Canvas/アニメライブラリの有無）。 |
| `data/css_reference_examples_pilot20.csv` | 別ルートで集めた20サイトの実測CSS値と、投稿者コメント（短い一言）。参考の補強データ。 |
| `data/vertical_writing_examples.csv` | 縦組（`writing-mode: vertical-rl`）を効果的に使っている14サイトの実測値（font-family・font-size・letter-spacing・line-height・font-weight・使用範囲）。短い日本語コピーを縦組にするかどうかを判断する際の参照データ。 |

`boldness_moderate_vs_bold.csv` と `css_reference_examples.csv` は現時点で以下6業種のみ対応: 不動産・建築・空間・施設、ウェディング、暮らし商品・サービス、アート、美容、IT・システム。それ以外の業種は `industry_keywords_moderate.csv` と `industry_tone_moderate.csv` のみで判断する。

### ステップ4: moderate / bold の位置を決める

`references/principles.md` の「4. moderate / bold ダイアル」に従い、ユーザーの指定またはブリーフの文脈から、どちらに寄せるかを判断する。指定がなければ業種の性質から妥当な位置を選ぶ。

### ステップ5: 短い日本語コピーがあれば縦組を検討する

ヒーローのキャッチコピーや1〜2行程度の見出しなど、短い日本語コピーが含まれる場合は、横組にする前に縦組（`writing-mode: vertical-rl`）の可能性を必ず検討する。判断基準と実測値は `references/principles.md` の「2. 縦組（縦書き）という選択肢」と `data/vertical_writing_examples.csv` を参照。長文の本文・フォーム等、可読性重視の箇所は横組のままでよい。

### ステップ6: 数値を制約として反映し、根拠を明示する

実際のデザイン案（配色・フォント・レイアウト・モーション・文字組の向き）を生成するときは、ステップ3-5で得た数値・実測例を具体的な制約として使う。「上品な配色」のような抽象語で止めず、「業種○○はchoooodoii統計で上品%が49.6%と高く、実測例では白・ベージュ系＋ゴシック体が中心（`css_reference_examples.csv`のFANCL/sizero等参照）」のように、根拠となった数値・出典行を出力の中で簡潔に示す。これにより、ユーザーが提案の妥当性を検証できる。

### ステップ7: 最終確認（スクリーンショットでレビューする）

デザインを適用した後、必ずスクリーンショットを撮って（または実際にレンダリングして）目視で確認する。特に以下を確認する。

1. **行末の孤立文字（泣き別れ）チェック**：見出し・リード文・キャッチコピーで、行の最後に1〜数文字だけが送られていないか。あれば `references/principles.md` の「行末の孤立文字（泣き別れ）を防ぐ」の対処法（`text-wrap: pretty`/`text-wrap: balance`/手動`<br>`/微調整）を適用する。
2. **モバイル幅（375px前後）での崩れ**：折り返し・余白・タップ領域が破綻していないか。
3. **コントラスト比**：WCAG AAを満たしているか（特にブランドカラーに白文字を載せる場合）。
4. **「陥りやすいAI丸わかりパターン」チェック**：`references/principles.md` のチェックリストに複数該当していないか。
5. **大胆さの一点集中**：装飾・モーション・強調がページ全体に均等にばらまかれていないか。最後に、ブリーフに貢献していない装飾を一つ削れないか検討する。

詳しい進め方（計画→レビュー→実装→批評の4段階）は `references/general-design-principles.md` の「6. 進め方」を参照。

## データの出典・注意事項

`data/`以下のCSVはchoooodoii.com（バランス型ギャラリー）と81-web.com（実験型ギャラリー）という2つの日本語Webデザインギャラリーサイトの分類ラベル・集計値・および実サイトのCSS実測値から作成している。詳細と利用条件についての注意は `README.md` を参照。データが無い/薄い業種について、存在しない数値を作り出さないこと。「参考データがないため一般原則で判断する」と明示した上で、`references/principles.md` の原則パートのみで判断してよい。
