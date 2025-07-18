import streamlit as st

# ページ設定
st.set_page_config(
    page_title="Google認証テスト",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# カスタムCSS
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .stButton > button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background: linear-gradient(90deg, #4285F4, #34A853, #FBBC05, #EA4335);
        color: white;
        border: none;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .user-info-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .logout-btn {
        background-color: #ff4757 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ヘッダー
st.markdown("""
# 🔐 Streamlit Google認証テストアプリ

このアプリケーションは、**streamlit-google-auth** ライブラリを使用してGoogle認証の動作を検証します。
""")

st.divider()

# 認証処理
try:
    # Streamlitネイティブ認証を使用
    if not st.user.is_logged_in:
        # ログイン前の表示
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            ### 🚀 はじめましょう
            
            下のボタンをクリックして、Googleアカウントでログインしてください。
            認証が成功すると、あなたのプロフィール情報が表示されます。
            """)
            
            # Googleログインボタン
            if st.button("🔐 Googleでログイン", key="login_btn", help="Googleアカウントでログインします"):
                st.login()
            
            st.info("""
            **🔒 プライバシーについて**
            
            このアプリは技術検証用です。取得した情報は保存されません。
            """)
    
    else:
        # ログイン成功時の表示
        user_info = st.user.to_dict()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown(f"""
            <div class="user-info-card">
                <h2>🎉 ログイン成功！</h2>
                <p>ようこそ、<strong>{user_info.get('name', 'ユーザー')}さん</strong>！</p>
            </div>
            """, unsafe_allow_html=True)
            
            # プロフィール画像を表示
            if user_info.get('picture'):
                st.image(
                    user_info.get('picture'), 
                    width=150, 
                    caption=f"{user_info.get('name')}さんのプロフィール画像"
                )
        
        # ユーザー情報の詳細表示
        st.subheader("📋 取得されたユーザー情報")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("**基本情報**")
            st.write(f"**👤 名前:** {user_info.get('name', 'N/A')}")
            st.write(f"**📧 メールアドレス:** {user_info.get('email', 'N/A')}")
            st.write(f"**✅ メール認証済み:** {'はい' if user_info.get('email_verified') else 'いいえ'}")
        
        with col2:
            st.info("**認証情報**")
            st.write(f"**🆔 ユーザーID:** {user_info.get('sub', 'N/A')}")
            st.write(f"**🌐 ロケール:** {user_info.get('locale', 'N/A')}")
            st.write(f"**👥 ファミリーネーム:** {user_info.get('family_name', 'N/A')}")
            st.write(f"**👤 名:** {user_info.get('given_name', 'N/A')}")
        
        # 詳細なJSONデータの表示
        with st.expander("🔍 取得データの詳細（JSON形式）"):
            st.json(user_info)
        
        st.divider()
        
        # ログアウトボタン
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🚪 ログアウト", key="logout", help="Google認証からログアウトします"):
                st.logout()

except Exception as e:
    st.error(f"認証処理中にエラーが発生しました: {str(e)}")
    st.warning("""
    **よくあるエラーの原因：**
    1. Streamlitのバージョンが1.47.0未満
    2. `.streamlit/secrets.toml` の設定が正しくない
    3. GCPのOAuth設定でリダイレクトURIが正しく設定されていない
    4. `Authlib>=1.3.2` がインストールされていない
    """)
    
    with st.expander("🛠️ トラブルシューティング"):
        st.markdown("""
        **設定を確認してください：**
        
        1. **Streamlitのバージョン確認**
           ```bash
           pip install streamlit>=1.47.0
           pip install authlib>=1.3.2
           ```
        
        2. **secrets.toml**ファイルの更新
           ```toml
           [auth]
           redirect_uri = "http://localhost:8601/oauth2callback"
           cookie_secret = "強力なランダムな文字列"
           client_id = "あなたのクライアントID"
           client_secret = "あなたのクライアントシークレット"
           server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
           ```
        
        3. **GCP Console**での設定確認
           - OAuth 2.0 クライアントIDが正しく作成されている
           - 承認済みリダイレクトURIに `http://localhost:8601/oauth2callback` が追加されている（末尾の`/oauth2callback`が重要）
        """)

# フッター
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <small>🔧 Streamlit Google認証テスト | streamlit-google-auth ライブラリを使用</small>
</div>
""", unsafe_allow_html=True) 