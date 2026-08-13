# おはぎ防災ウォッチ（無料版・第1号）

取手市・柏市・流山市とJR東日本 常磐線の公式情報を定期確認し、重要な災害・交通情報だけをTelegramへ通知する試作版です。

## 監視対象
- 柏市 公式RSS
- 流山市 公式RSS
- 取手市 公式サイト
- JR東日本 常磐線 公式運行情報

## 無料構成
GitHub Actions + Telegram Bot。

1. GitHubで公開リポジトリを作る
2. このフォルダの中身をアップロード
3. TelegramでBotFatherからBotを作る
4. GitHub Secretsに `TELEGRAM_BOT_TOKEN` と `TELEGRAM_CHAT_ID` を登録
5. Actionsを有効化
6. `Run workflow` でテスト

通常は5分ごとに確認します。GitHub Actionsの実行には遅延があり得るため、自治体・気象庁・JR東日本の公式緊急情報の代替にはしません。

## 次の拡張
守谷市、柏市管路内水位、雨量、河川水位、道路冠水など。
