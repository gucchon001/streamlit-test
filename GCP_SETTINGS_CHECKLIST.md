# 🔧 Google Cloud Platform OAuth設定チェックリスト

## 📍 現在の設定確認

### ユーザーから報告された設定
- ✅ **承認済みのJavaScript生成元**: `http://localhost:8601`
- ❓ **承認済みのリダイレクトURI**: 確認が必要

## 🎯 完全な設定要件

### OAuth 2.0 クライアントID設定画面で確認すべき項目

#### 1. 基本情報
- **名前**: `Streamlit Web Client` (任意の名前)
- **クライアントID**: `YOUR_CLIENT_ID.apps.googleusercontent.com`
- **クライアントシークレット**: `YOUR_CLIENT_SECRET`

#### 2. JavaScript生成元（Origins）
```
✅ 設定済み: http://localhost:8601
```

#### 3. リダイレクトURI（最重要）
```
⚠️ 確認必要: http://localhost:8601/oauth2callback
```

## 🔧 設定手順（再確認用）

### ステップ1: GCP Consoleアクセス
1. [Google Cloud Console](https://console.cloud.google.com/) を開く
2. 正しいプロジェクトが選択されていることを確認

### ステップ2: OAuth クライアント設定確認
1. **APIとサービス** → **認証情報** をクリック
2. **OAuth 2.0 クライアントID** セクションから該当のクライアントIDをクリック

### ステップ3: 詳細設定確認
#### JavaScript生成元
- ✅ `http://localhost:8601` が設定済み

#### 承認済みのリダイレクトURI
- ⚠️ **必須**: `http://localhost:8601/oauth2callback` が設定されているか確認

## 🎯 正しい設定例

```
【JavaScript 生成元】
http://localhost:8601

【承認済みのリダイレクトURI】  
http://localhost:8601/oauth2callback
```

## ❗ よくある設定ミス

### ❌ 間違った設定
```
【リダイレクトURI - 間違い】
http://localhost:8601           ← oauth2callbackがない
http://localhost:8501/oauth2callback  ← ポート番号が違う
https://localhost:8601/oauth2callback ← httpsになっている
```

### ✅ 正しい設定
```
【リダイレクトURI - 正しい】
http://localhost:8601/oauth2callback
```

## 🔍 設定確認方法

### GCP Console での確認
1. OAuth クライアントIDの詳細画面を開く
2. 以下の項目を確認：
   - **承認済みのJavaScript生成元**: `http://localhost:8601`
   - **承認済みのリダイレクトURI**: `http://localhost:8601/oauth2callback`

### 設定が正しい場合の動作
- Streamlitアプリで「Googleでログイン」ボタンをクリック
- Google認証画面が表示される
- 認証完了後、アプリに戻ってユーザー情報が表示される

### 設定が間違っている場合の症状
- `Error 400: redirect_uri_mismatch` エラーが発生
- Google認証画面が表示されない
- 認証後にエラーページが表示される

## 🚀 次のアクション

### すでに動作している場合
- ✅ 設定は正しく完了している
- 技術検証成功

### まだエラーが出る場合
1. **リダイレクトURI**に `http://localhost:8601/oauth2callback` を追加
2. 設定を**保存**
3. ブラウザを**リフレッシュ**してテスト

## 📝 メモ

- JavaScript生成元: フロントエンドからのリクエスト用
- リダイレクトURI: 認証後のコールバック用（**最も重要**）
- 両方とも設定が必要な場合が多い 