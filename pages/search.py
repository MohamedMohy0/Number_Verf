import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re




st.set_page_config(page_title="Search", layout="centered")
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
st.markdown("<h1 style='text-align: center;'> البحث عن رقم</h1>", unsafe_allow_html=True)



# حقل إدخال مخصص بالاتجاه LTR
رقم_البحث = st.text_input("أدخل الرقم الذي ترغب في البحث عنه:")

@st.cache_resource
def connect_to_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["google"], scope)
    client = gspread.authorize(creds)
    sheet_id = st.secrets["Verf"]["Verf"]
    sheet = client.open_by_key(sheet_id).sheet1
    return sheet

sheet = connect_to_sheet()

def تنظيف_الرقم(رقم):
    # حذف كل ما ليس رقماً
    return re.sub(r"\D", "", رقم)
    
n=رقم_البحث.replace(" ","")
رقم_البحث= رقم_البحث.replace("+2","")
رقم_البحث= رقم_البحث.replace("+","")
n=n.replace("+2","")
n=n.replace("+","")
if st.button("بحث"):
    if not رقم_البحث:
        st.warning("يرجى إدخال رقم أولاً.")
    else:
        البيانات = sheet.col_values(1)[1:]  
        البيانات_المنظفة = [تنظيف_الرقم(رقم) for رقم in البيانات]
        if رقم_البحث in البيانات:
            رقم_الصف = البيانات.index(رقم_البحث) + 2
            الصف_الكامل = sheet.row_values(رقم_الصف)
            st.success(f"✅ الرقم{رقم_البحث} موثق وموجود في البيانات.")
        elif n in البيانات_المنظفة:
            رقم_الصف = البيانات_المنظفة.index(n) + 2
            الصف_الكامل = sheet.row_values(رقم_الصف)
            st.success(f"✅ الرقم{رقم_البحث} موثق وموجود في البيانات.")


        elif n in البيانات:
            رقم_الصف = البيانات.index(n) + 2
            الصف_الكامل = sheet.row_values(رقم_الصف)
            st.success(f"✅ الرقم{رقم_البحث} موثق وموجود في البيانات.")


        elif رقم_البحث in البيانات_المنظفة:
            رقم_الصف = البيانات_المنظفة.index(n) + 2
            الصف_الكامل = sheet.row_values(رقم_الصف)
            st.success(f"✅ الرقم{رقم_البحث} موثق وموجود في البيانات.")

        
        
        else:
            st.error(f"❌ الرقم {رقم_البحث} غير موجود.")


