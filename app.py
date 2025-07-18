import streamlit as st
import requests
from authlib.integrations.requests_client import OAuth2Session
from urllib.parse import urlencode, parse_qs
import json

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
    .success-box {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
    }
    .info-box {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Google OAuth2設定
GOOGLE_CLIENT_ID = st.secrets.get("google_client_id", "")
GOOGLE_CLIENT_SECRET = st.secrets.get("google_client_secret", "")
REDIRECT_URI = st.secrets.get("redirect_uri", "")

AUTHORIZATION_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
USERINFO_ENDPOINT = "https://www.googleapis.com/oauth2/v1/userinfo"

def get_google_oauth_url():
    """Google OAuth認証URLを生成"""
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "openid email profile",
        "response_type": "code",
        "access_type": "offline",
        "include_granted_scopes": "true"
    }
    return f"{AUTHORIZATION_ENDPOINT}?{urlencode(params)}"

def exchange_code_for_token(code):
    """認証コードをアクセストークンに交換"""
    data = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI
    }
    
    response = requests.post(TOKEN_ENDPOINT, data=data)
    return response.json()

def get_user_info(access_token):
    """アクセストークンを使ってユーザー情報を取得"""
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(USERINFO_ENDPOINT, headers=headers)
    return response.json()

# ヘッダー
st.markdown("""
# 🔐 Streamlit Google認証テストアプリ

このアプリケーションは、**authlib** ライブラリを使用してGoogle認証の動作を検証します。
""")

st.divider()

# 認証情報確認
if not all([GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, REDIRECT_URI]):
    st.error("⚠️ 設定ファイルに必要な情報がありません")
    st.info("Streamlit CloudのSecretsに以下の設定が必要です：")
    st.code("""
google_client_id = "あなたのクライアントID"
google_client_secret = "あなたのクライアントシークレット"
redirect_uri = "https://app-test-ht4vcwnptswnt2adz8siev.streamlit.app"
    """)
    st.stop()

# セッション状態の初期化
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_info" not in st.session_state:
    st.session_state.user_info = None

# 認証コードの処理
if not st.session_state.authenticated:
    # URLパラメータから認証コードを取得
    if "code" in st.query_params:
        try:
            with st.spinner("認証処理中..."):
                code = st.query_params["code"]
                
                # アクセストークンを取得
                token_response = exchange_code_for_token(code)
                
                if "access_token" in token_response:
                    # ユーザー情報を取得
                    user_info = get_user_info(token_response["access_token"])
                    
                    # セッション状態を更新
                    st.session_state.authenticated = True
                    st.session_state.user_info = user_info
                    
                    # URLをクリーンアップ
                    st.query_params.clear()
                    st.rerun()
                else:
                    st.error(f"トークン取得エラー: {token_response}")
        except Exception as e:
            st.error(f"認証エラー: {str(e)}")

# メインコンテンツ
if st.session_state.authenticated:
    # 認証済みユーザー向けコンテンツ
    user_info = st.session_state.user_info
    
    st.markdown('<div class="success-box">', unsafe_allow_html=True)
    st.markdown("### ✅ 認証に成功しました！")
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if user_info.get("picture"):
            st.image(user_info["picture"], width=150, caption="プロフィール画像")
    
    with col2:
        st.markdown('<div class="user-info-card">', unsafe_allow_html=True)
        st.markdown("### 👤 ユーザー情報")
        st.write(f"**名前:** {user_info.get('name', 'N/A')}")
        st.write(f"**メール:** {user_info.get('email', 'N/A')}")
        st.write(f"**ID:** {user_info.get('id', 'N/A')}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.divider()
    
    # 詳細情報
    st.markdown("### 📊 認証情報詳細")
    with st.expander("ユーザー情報（JSON）"):
        st.json(user_info)
    
    # ログアウトボタン
    if st.button("🚪 ログアウト", type="primary"):
        st.session_state.authenticated = False
        st.session_state.user_info = None
        st.rerun()

else:
    # 未認証ユーザー向けコンテンツ
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("### 🔒 認証が必要です")
    st.markdown("Googleアカウントでログインしてアプリケーションを使用してください。")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 認証URL生成とボタン表示
    auth_url = get_google_oauth_url()
    
    st.markdown("---")
    
    # ログインボタン（リンク）
    st.markdown(f"""
    <div style="text-align: center; margin: 2rem 0;">
        <a href="{auth_url}" target="_self" style="
            background: linear-gradient(45deg, #4285f4, #34a853);
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            display: inline-block;
            transition: transform 0.2s;
        " onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
            🚀 Googleでログイン
        </a>
    </div>
    """, unsafe_allow_html=True)

# フッター
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9em;">
    ⚡ Powered by Streamlit & Google OAuth 2.0<br>
    🔒 セキュアな認証システムのテスト
</div>
""", unsafe_allow_html=True) 