import streamlit as st

st.set_page_config(page_title="وثقها", layout="centered")
hide_sidebar = """
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        .main {
            margin-left: 0;
        }
    </style>
"""
st.markdown(hide_sidebar, unsafe_allow_html=True)
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.markdown(
    """
    <style>
        body, .stApp {
            direction: rtl;
            text-align: right;
            font-family: 'Arial', sans-serif;
        }
        .css-1d391kg {
            text-align: right;
        }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown("<div style='height:15vh'></div>", unsafe_allow_html=True)

# Title centered
st.markdown("<h1 style='text-align: center;'> وثقها</h1>", unsafe_allow_html=True)

# Center buttons using columns
st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
col = st.columns(5)[2]  # center column out of 3

with col:
    if st.button("البحث عن رقم"):
        st.switch_page("pages/search.py")
    st.markdown("<div style='height: 1em;'></div>", unsafe_allow_html=True)  # Spacer
    if st.button("تسجيل البيانات"):
        st.switch_page("pages/sign.py")

st.markdown("</div>", unsafe_allow_html=True)
