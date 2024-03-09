import streamlit as st
import yaml
from datetime import timedelta
import extra_streamlit_components as stx

from login.login_utils import check_password, hash_password, token_decode, token_encode


config = yaml.safe_load(open('./mock_data/mock_users.yaml'))
cookie_manager = stx.CookieManager()


def authenticate_via_cookie():
    token = cookie_manager.get(config['cookie']['name'])
    if token:
        decoded = token_decode(token, config['cookie']['key'])
        if decoded:
            st.session_state['authenticated'] = True
            return True
    st.session_state['authenticated'] = False
    return False


def login_user(username: str, password: str):
    user_info = config['credentials']['usernames'].get(username, {})
    hashed_password = user_info.get('password', '').encode('utf-8')

    if user_info and check_password(password, hashed_password):
        token = token_encode(username, config['cookie']['key'], config['cookie']['expiry_days'])
        cookie_manager.set(config['cookie']['name'], token, max_age=int(timedelta(days=config['cookie']['expiry_days']).total_seconds()))
        st.session_state['authenticated'] = True
        return True
    st.session_state['authenticated'] = False
    return False


def logout_user():
    cookie_manager.delete(config['cookie']['name'])
    st.session_state['authenticated'] = False


st.title('Login Page')
if 'authenticated' not in st.session_state:
    authenticate_via_cookie()

if st.session_state.get('authenticated', False):
    st.success("You're already logged in.")
    if st.button('Logout'):
        logout_user()
        st.experimental_rerun()
else:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button('Login'):
        if login_user(username, password):  # Here, we pass the plaintext password.
            st.success('Login successful.')
            st.experimental_rerun()
        else:
            st.error('Login failed.')
