# 🔐 Streamlit Google認証 技術検証レポート

**作成日**: 2025年1月18日  
**検証者**: 技術検証チーム  
**検証内容**: StreamlitネイティブGoogle認証機能の実装と動作確認

## 📋 検証概要

### 目的
- Streamlit 1.47.0以降のネイティブGoogle認証機能の検証
- 実用的なGoogle OAuth 2.0 / OpenID Connect実装の確立
- 本番環境への適用可能性の評価

### 結果サマリー
✅ **検証成功**  
- Streamlitネイティブ認証機能が正常に動作
- Google OAuth 2.0による認証フローが完全に機能
- ユーザー情報の取得と表示が正常に動作
- ログイン・ログアウト機能が期待通りに動作

## 🛠️ 技術仕様

### 環境
- **Streamlit**: 1.47.0
- **Python**: 3.13
- **認証ライブラリ**: authlib>=1.3.2
- **プロトコル**: OpenID Connect (OIDC)
- **プロバイダー**: Google Identity

### アーキテクチャ
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   Google OAuth   │    │   Google        │
│   Application   │◄──►│   2.0 / OIDC     │◄──►│   Identity      │
│                 │    │   Flow           │    │   Provider      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
          │                       │                       │
          ▼                       ▼                       ▼
    ┌─────────────┐      ┌─────────────────┐      ┌─────────────┐
    │  User       │      │  Authorization  │      │  User       │
    │  Interface  │      │  Server        │      │  Profile    │
    └─────────────┘      └─────────────────┘      └─────────────┘
```

### セキュリティ機能
- **CORS保護**: 自動有効化
- **XSRF保護**: 自動有効化  
- **Cookie暗号化**: 強力な秘密鍵による暗号化
- **セッション管理**: 30日間の自動有効期限
- **State/Nonce検証**: 自動処理

## 🚀 実装手順

### 1. 依存関係のインストール

```bash
# 必要なライブラリをインストール
pip install streamlit>=1.47.0 authlib>=1.3.2
```

### 2. Google Cloud Platform 設定

#### 2.1 プロジェクト作成・選択
1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. 新しいプロジェクトを作成または既存プロジェクトを選択

#### 2.2 OAuth同意画面の設定
1. **「APIとサービス」** → **「OAuth同意画面」**
2. **User Type**: 「外部」を選択
3. **アプリ情報**を入力:
   - アプリ名: `Streamlit Google Auth Demo`
   - ユーザーサポートメール: 開発者メールアドレス
   - 承認済みドメイン: （ローカル開発では不要）
   - デベロッパーの連絡先情報: 開発者メールアドレス

#### 2.3 認証情報の作成
1. **「APIとサービス」** → **「認証情報」**
2. **「+ 認証情報を作成」** → **「OAuth クライアントID」**
3. **アプリケーションの種類**: 「ウェブ アプリケーション」
4. **名前**: `Streamlit Web Client`
5. **承認済みのリダイレクトURI**:
   ```
   http://localhost:8601/oauth2callback
   ```
   ⚠️ **重要**: 末尾の `/oauth2callback` は必須

#### 2.4 認証情報の取得
- **クライアントID**: `YOUR_CLIENT_ID.apps.googleusercontent.com`
- **クライアントシークレット**: `YOUR_CLIENT_SECRET`

### 3. Streamlit アプリケーション設定

#### 3.1 秘密情報の設定
`.streamlit/secrets.toml`
```toml
# Streamlitネイティブ認証設定
[auth]
redirect_uri = "http://localhost:8601/oauth2callback"
cookie_secret = "YOUR_STRONG_RANDOM_SECRET"
client_id = "YOUR_CLIENT_ID.apps.googleusercontent.com"
client_secret = "YOUR_CLIENT_SECRET"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
```

#### 3.2 メインアプリケーション
`app.py`
```python
import streamlit as st

# ページ設定
st.set_page_config(
    page_title="Google認証テスト",
    page_icon="🔐",
    layout="wide"
)

# 認証フロー
if not st.user.is_logged_in:
    st.markdown("### 🚀 Google認証テスト")
    if st.button("🔐 Googleでログイン"):
        st.login()
else:
    user_info = st.user.to_dict()
    st.success("ログイン成功！")
    st.write(f"ようこそ、{user_info.get('name')}さん！")
    
    if st.button("🚪 ログアウト"):
        st.logout()
```

### 4. アプリケーション実行

```bash
# アプリケーション起動
streamlit run app.py --server.port 8601

# アクセスURL
# http://localhost:8601
```

## 🔍 検証結果詳細

### 機能テスト結果

| 機能 | 結果 | 詳細 |
|------|------|------|
| ログインボタン表示 | ✅ 成功 | Googleログインボタンが正常に表示 |
| Google認証リダイレクト | ✅ 成功 | Googleログイン画面へのリダイレクト正常 |
| 認証コールバック | ✅ 成功 | `/oauth2callback` エンドポイント正常動作 |
| ユーザー情報取得 | ✅ 成功 | 名前、メール、プロフィール画像等を取得 |
| セッション維持 | ✅ 成功 | ページリロード後もログイン状態維持 |
| ログアウト機能 | ✅ 成功 | ログアウト後の状態遷移正常 |

### 取得可能なユーザー情報

```json
{
    "is_logged_in": true,
    "iss": "https://accounts.google.com",
    "azp": "{client_id}.apps.googleusercontent.com",
    "aud": "{client_id}.apps.googleusercontent.com", 
    "sub": "{unique_user_id}",
    "email": "{user}@gmail.com",
    "email_verified": true,
    "name": "{full_name}",
    "picture": "https://lh3.googleusercontent.com/a/{content_path}",
    "given_name": "{given_name}",
    "family_name": "{family_name}",
    "locale": "ja",
    "iat": {issued_time},
    "exp": {expiration_time}
}
```

### パフォーマンス

- **初回ログイン時間**: 約3-5秒
- **ページロード時間**: 約1-2秒
- **認証状態確認**: 即座（Cookie読み込み）
- **ログアウト処理**: 約1秒

## 🐛 トラブルシューティング

### よくある問題と解決方法

#### 1. redirect_uri_mismatch エラー
**原因**: GCPでのリダイレクトURI設定不備

**解決方法**:
```
❌ 間違い: http://localhost:8601
✅ 正しい: http://localhost:8601/oauth2callback
```

#### 2. Streamlitバージョンエラー
**原因**: 古いStreamlitバージョン

**解決方法**:
```bash
pip install streamlit>=1.47.0
```

#### 3. authlib未インストールエラー
**原因**: 必要な認証ライブラリ不足

**解決方法**:
```bash
pip install authlib>=1.3.2
```

#### 4. Cookie設定エラー
**原因**: cookie_secret未設定

**解決方法**:
```toml
[auth]
cookie_secret = "強力なランダム文字列"
```

### エラーコード対応表

| エラーコード | 原因 | 解決方法 |
|-------------|------|---------|
| 400: redirect_uri_mismatch | リダイレクトURI不一致 | GCP設定確認 |
| 401: invalid_client | クライアント認証失敗 | クライアントID/シークレット確認 |
| 403: access_denied | アクセス拒否 | OAuth同意画面設定確認 |

## 📊 セキュリティ評価

### セキュリティ強度
- **認証プロトコル**: OpenID Connect (業界標準) ⭐⭐⭐⭐⭐
- **暗号化**: AES暗号化Cookie ⭐⭐⭐⭐⭐
- **CSRF保護**: 自動有効化 ⭐⭐⭐⭐⭐
- **セッション管理**: 30日自動期限 ⭐⭐⭐⭐⭐

### セキュリティ推奨事項
1. **本番環境**: 強力なcookie_secretの使用
2. **HTTPS**: 本番環境では必須
3. **ドメイン制限**: 本番用ドメインの明示的設定
4. **監査ログ**: アクセスログの記録

## 🚀 本番環境への適用

### 設定変更項目

#### 1. secrets.toml 更新
```toml
[auth]
redirect_uri = "https://yourdomain.com/oauth2callback"  # HTTPS化
cookie_secret = "production_strong_random_secret_key"    # 強力な秘密鍵
client_id = "production_client_id"
client_secret = "production_client_secret"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
```

#### 2. GCP設定更新
- **承認済みドメイン**: 本番ドメインを追加
- **リダイレクトURI**: `https://yourdomain.com/oauth2callback`
- **OAuth同意画面**: 本番用情報に更新

#### 3. デプロイ考慮事項
- **環境変数**: secrets.tomlを環境変数で管理
- **SSL証明書**: HTTPS必須
- **ロードバランサー**: セッション永続化設定

## 📈 今後の展開

### 機能拡張案
1. **マルチプロバイダー対応**: Microsoft, GitHub等
2. **ロールベースアクセス制御**: 管理者・一般ユーザー分離
3. **ユーザー管理画面**: 登録ユーザー一覧・管理
4. **監査ログ**: ログイン履歴・アクセス記録

### 技術改善案
1. **カスタムUI**: ログインボタンのデザイン改善
2. **エラーハンドリング**: より詳細なエラー処理
3. **テストスイート**: 自動テストの実装
4. **CI/CD**: 自動デプロイパイプライン

## 🎯 結論

### 検証結果まとめ
- ✅ **技術的実現性**: 高い
- ✅ **実装の簡単さ**: 非常に簡単
- ✅ **セキュリティ**: 業界標準レベル
- ✅ **保守性**: Streamlit公式サポートで安心
- ✅ **拡張性**: マルチプロバイダー対応可能

### 推奨事項
1. **本格採用**: Streamlitプロジェクトでの標準認証方法として採用推奨
2. **サードパーティライブラリ**: 不要（ネイティブ機能で十分）
3. **学習コスト**: 低い（従来のStreamlit知識で対応可能）

### 次のアクション
1. 本番環境でのパイロット実装
2. チーム内での技術共有セッション
3. 認証機能の標準化ドキュメント作成
4. 他プロジェクトへの横展開検討

---

**📝 Note**: この検証は2025年1月時点の情報に基づいています。Streamlitの更新に伴い、機能や設定方法が変更される可能性があります。

**🔗 参考資料**:
- [Streamlit Authentication Documentation](https://docs.streamlit.io/develop/concepts/connections/authentication)
- [Google Identity OpenID Connect](https://developers.google.com/identity/protocols/oauth2/openid-connect)
- [Streamlit st.login API Reference](https://docs.streamlit.io/develop/api-reference/user/st.login) 