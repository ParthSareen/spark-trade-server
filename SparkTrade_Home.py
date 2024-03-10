import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

# set all the states here, so we can check them later without it screaming at us
st.session_state['authenticated'] = False
st.session_state['user'] = ''

# track total discharged
# track total amount traded
# -> create endpoint that arduino can hit to push this data
# this will be used for actual state of charge and total discharge graphs

# streamlit doesn't work for a restful api
# strap a flask server onto this

st.write("# Welcome to Streamlit! 👋")
