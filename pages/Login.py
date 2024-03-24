import streamlit as st
import yaml
from datetime import timedelta
import extra_streamlit_components as stx

from login.login_utils import check_password, token_decode, token_encode


config = yaml.safe_load(open('./data/mock_users.yaml'))
cookie_manager = stx.CookieManager()


st.session_state['authenticated'] = True
if st.button("jsmith"):
    st.session_state['user'] = 'jsmith'
    st.session_state['x'] = config['credentials']['usernames'][st.session_state['user']]['location_x']
    st.session_state['y'] = config['credentials']['usernames'][st.session_state['user']]['location_y']
    logged_in = st.session_state['user']
    st.success(f'Succesfully logged in User: {logged_in}')
    
if st.button("rbriggs"):
    st.session_state['user'] = 'rbriggs'
    st.session_state['x'] = config['credentials']['usernames'][st.session_state['user']]['location_x']
    st.session_state['y'] = config['credentials']['usernames'][st.session_state['user']]['location_y']
    logged_in = st.session_state['user']
    st.success(f'Succesfully logged in User: {logged_in}')

if st.button("jbiden"):
    st.session_state['user'] = 'jbiden'
    st.session_state['x'] = config['credentials']['usernames'][st.session_state['user']]['location_x']
    st.session_state['y'] = config['credentials']['usernames'][st.session_state['user']]['location_y']
    logged_in = st.session_state['user']
    st.success(f'Succesfully logged in User: {logged_in}')


# def authenticate_via_cookie():
#     token = cookie_manager.get(config['cookie']['name'])
#     if token:
#         decoded = token_decode(token, config['cookie']['key'])
#         if decoded:
#             st.session_state['authenticated'] = True
#             return True
#     st.session_state['authenticated'] = False
#     return False


# def login_user(username: str, password: str):
#     user_info = config['credentials']['usernames'].get(username, {})
#     hashed_password = user_info.get('password', '').encode('utf-8')

#     if user_info and check_password(password, hashed_password):
#         token = token_encode(username, config['cookie']['key'], config['cookie']['expiry_days'])
#         cookie_manager.set(config['cookie']['name'], token, max_age=int(timedelta(days=config['cookie']['expiry_days']).total_seconds()))
#         st.session_state['authenticated'] = True
#         return True
#     st.session_state['authenticated'] = False
#     return False


# def logout_user():
#     try:
#         cookie_manager.delete(config['cookie']['name'])
#     except KeyError as e:
#         st.warning(f"Attempted to delete a non-existing cookie: {e}")
#     st.session_state['authenticated'] = False
#     st.write("You have been logged out.")
#     st.experimental_rerun()


# st.title('Login Page')
# if 'authenticated' not in st.session_state:
#     authenticate_via_cookie()

# if st.session_state.get('authenticated', False):
#     st.success("Logged in.")
#     if st.button('Logout'):
#         logout_user()
#         st.experimental_rerun()
# else:
#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")
#     if st.button('Login'):
#         if login_user(username, password):
#             st.success('Login successful.')
#             st.session_state['user'] = username
#             st.experimental_rerun()
#         else:
#             st.error('Login failed.')
