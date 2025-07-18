# 🔐 Streamlit Google認証テストアプリ

このプロジェクトは、Streamlitを使用してGoogle認証機能を検証するためのテストアプリケーションです。

## 📋 概要

- **Streamlitネイティブ認証機能** を使用（v1.47.0以降）
- Google OpenID Connect (OIDC) による認証機能
- ユーザープロフィール情報の取得と表示
- 日本語対応のユーザーフレンドリーなUI

## 🚀 セットアップ手順

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. Google Cloud Platform (GCP) の設定

1. [Google Cloud Console](https://console.cloud.google.com/)にアクセス
2. 新しいプロジェクトを作成または既存のプロジェクトを選択
3. **APIとサービス** > **OAuth同意画面** から同意画面を設定
4. **APIとサービス** > **認証情報** からOAuth 2.0クライアントIDを作成
5. **承認済みのリダイレクトURI**に以下を追加（末尾の`/oauth2callback`が重要）：
   ```
   http://localhost:8601/oauth2callback
   ```

### 3. 認証情報の設定

`.streamlit/secrets.toml` ファイルを以下の形式で設定してください：

```toml
# Streamlitネイティブ認証設定
[auth]
redirect_uri = "http://localhost:8601/oauth2callback"
cookie_secret = "強力なランダム文字列"  # 本番では必ず変更してください
client_id = "942242923452-n9nm94dnt8uhcdpoal7vpq1ta33folg0.apps.googleusercontent.com"
client_secret = "YOUR_GOOGLE_CLIENT_SECRET_HERE"  # ここを実際の値に置き換え
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
```

**重要**: 
- `client_secret` を、GCPで取得した実際のクライアントシークレットに置き換えてください
- `cookie_secret` は本番環境では強力なランダム文字列に変更してください

## 🎯 使用方法

### アプリケーションの起動

```bash
streamlit run app.py --server.port 8601
```

### 動作確認

1. ブラウザで `http://localhost:8601` にアクセス
2. **Login with Google** ボタンをクリック
3. Googleアカウントでログイン
4. 認証成功後、ユーザー情報が表示されます

## 📁 ファイル構成

```
streamlit_google_auth_test/
├── .streamlit/
│   └── secrets.toml          # Google認証設定（秘密情報）
├── app.py                    # メインアプリケーション
├── requirements.txt          # 依存関係
└── README.md                # このファイル
```

## ✨ 機能

- 🔐 Google OpenID Connect (OIDC) 認証
- 👤 ユーザープロフィール情報の表示
- 🖼️ プロフィール画像の表示
- 📧 メールアドレス、名前などの基本情報取得
- 🚪 ログアウト機能（クッキー管理）
- 📱 レスポンシブデザイン
- 🛠️ エラーハンドリングとトラブルシューティング
- 🔄 セッション永続化（30日間有効）

## 🐛 トラブルシューティング

### よくある問題

1. **認証エラーが発生する場合**
   - `secrets.toml` のクライアントシークレットが正しく設定されているか確認
   - GCPのリダイレクトURIが `http://localhost:8601` に設定されているか確認

2. **ライブラリのインポートエラー**
   ```bash
   pip install --upgrade streamlit streamlit-google-auth
   ```

3. **ポート8601が使用中の場合**
   ```bash
   streamlit run app.py --server.port 8602
   ```
   その場合、GCPのリダイレクトURIも `http://localhost:8602` に変更してください。

## 🔒 セキュリティ注意事項

- `secrets.toml` ファイルは絶対にGitにコミットしないでください
- クライアントシークレットは安全に管理してください
- 本番環境では適切な環境変数管理を使用してください

## 📚 参考資料

- [streamlit-google-auth Documentation](https://github.com/mkhorasani/streamlit-google-auth)
- [Google OAuth 2.0 Documentation](https://developers.google.com/identity/protocols/oauth2)
- [Streamlit Documentation](https://docs.streamlit.io/) 