import streamlit as st
from streamlit_google_auth import Authenticate

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
    .user-info-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ヘッダー
st.markdown("""
# 🔐 Streamlit Google認証テストアプリ

このアプリケーションは、**streamlit-google-auth** ライブラリを使用してGoogle認証の動作を検証します。
""")

st.divider()

# 認証情報を取得
try:
    client_id = st.secrets["google_client_id"]
    client_secret = st.secrets["google_client_secret"]
    redirect_uri = st.secrets["redirect_uri"]
except KeyError as e:
    st.error(f"設定ファイルに必要な情報がありません: {e}")
    st.info("Streamlit CloudのSecretsに以下の設定が必要です：")
    st.code("""
google_client_id = "あなたのクライアントID"
google_client_secret = "あなたのクライアントシークレット"
redirect_uri = "https://app-test-ht4vcwnptswnt2adz8siev.streamlit.app"
    """)
    st.stop()

# 認証クラスの初期化
authenticator = Authenticate(
    secret_credentials_path=None,  # ファイルではなくsecretsから取得
    cookie_name='google_auth_cookie',
    cookie_key='google_auth_cookie_key',
    redirect_uri=redirect_uri,
    cookie_expiry_days=1
)

# 手動でクレデンシャルを設定
authenticator.client_id = client_id
authenticator.client_secret = client_secret

# 認証チェック
authenticator.check_authentification()

# 認証処理
try:
    # ログインボタンの表示
    authenticator.login()
    
    # ログイン状態の確認
    if st.session_state.get('connected', False):
        # ログイン成功時の表示
        user_info = st.session_state.get('user_info', {})
        
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
        
        with col2:
            st.info("**認証情報**")
            st.write(f"**🆔 OAuth ID:** {st.session_state.get('oauth_id', 'N/A')}")
        
        # 詳細なJSONデータの表示
        with st.expander("🔍 取得データの詳細（JSON形式）"):
            st.json(user_info)
        
        st.divider()
        
        # ログアウトボタン
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🚪 ログアウト", key="logout", help="Google認証からログアウトします"):
                authenticator.logout()
    
    else:
        # ログイン前の表示
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            ### 🚀 はじめましょう
            
            上の「Login with Google」ボタンをクリックして、Googleアカウントでログインしてください。
            認証が成功すると、あなたのプロフィール情報が表示されます。
            """)
            
            st.info("""
            **🔒 プライバシーについて**
            
            このアプリは技術検証用です。取得した情報は保存されません。
            """)

except Exception as e:
    st.error(f"認証処理中にエラーが発生しました: {str(e)}")
    st.warning("""
    **エラーの原因：**
    1. streamlit-google-authライブラリの問題
    2. Google Cloud Platform設定の問題
    3. Streamlit Cloud Secrets設定の問題
    """)

# フッター
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <small>🔧 Streamlit Google認証テスト | streamlit-google-auth ライブラリを使用</small>
</div>
""", unsafe_allow_html=True) 