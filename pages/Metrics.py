import streamlit as st
import pandas as pd
import altair as alt


if not st.session_state['authenticated']:
    st.write("You must be logged in to view this page")
    exit()

st.set_page_config(page_title="State of Charge", page_icon="📊")
st.title('State of Charge')

user = st.session_state.get('user')
csv_file_path = f'./mock_data/{user}_soc.csv' 

df = pd.read_csv(csv_file_path)
df['time'] = pd.to_datetime(df['time'])

chart = (
        alt.Chart(
            data=df,
            title="Current State of Charge",
        )
        .mark_line()
        .encode(
            x=alt.X("time", axis=alt.Axis(title="Time", format="%H:%M"), type="temporal"),
            y=alt.Y("soc", axis=alt.Axis(title="State of Charge")),
        )
)

st.altair_chart(chart, use_container_width=True)


st.write("raw CSV data:")
st.dataframe(df) 