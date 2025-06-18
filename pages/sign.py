import streamlit as st
from PIL import Image
import io
import uuid
from datetime import date
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

@st.cache_resource
def connect_to_services_M():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["google"], scope)
    client = gspread.authorize(creds)
    Male_sheet = client.open_by_key(st.secrets["Male"]["Male"]).sheet1
    drive_service = build("drive", "v3", credentials=creds)
    return Male_sheet, drive_service

def connect_to_services_F():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["google"], scope)
    client = gspread.authorize(creds)
    Female_sheet=client.open_by_key(st.secrets["Female"]["Female"]).sheet1

    drive_service = build("drive", "v3", credentials=creds)
    return Female_sheet, drive_service

def upload_image(image_data, drive_service, folder_id):
    image = Image.open(image_data)
    img_bytes = io.BytesIO()
    image.save(img_bytes, format='JPEG')
    img_bytes.seek(0)

    file_metadata = {
        'name': f"{uuid.uuid4().hex}.jpg",
        'parents': [folder_id]
    }
    media = MediaIoBaseUpload(img_bytes, mimetype='image/jpeg')
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    # Make the image public
    drive_service.permissions().create(fileId=file['id'], body={"role": "reader", "type": "anyone"}).execute()

    # Return the image link
    return f"https://drive.google.com/uc?id={file['id']}"

st.set_page_config(page_title="تسجيل البيانات ", layout="centered")
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
st.markdown("<h1 style='text-align: center;'> تسجيل البيانات</h1>", unsafe_allow_html=True)

name = st.text_input("أدخل الاسم ثلاثي ")

gender = st.radio("اختر النوع", options=["ذكر", "أنثى"], horizontal=True)

age= st.text_input("أدخل عمرك ")

id= st.text_input("أدخل رقم الهوية  ")

dateofbirth= st.date_input("أدخل تاريخ الميلاد ", date.today())

if "show_face_camera" not in st.session_state:
    st.session_state.show_face_camera = False

if "show_id_camera" not in st.session_state:
    st.session_state.show_id_camera = False

# Button to trigger face camera
if st.button(" صورة شخصية"):
    st.session_state.show_face_camera = True

# Show camera for face after button press
if st.session_state.show_face_camera:
    face = st.camera_input("قم بتصوير صورة شخصية")
    if face:
        st.success(" تم التقاط الصورة الشخصية")

# Button to trigger ID camera
if st.button(" صورة الهوية"):
    st.session_state.show_id_camera = True

# Show camera for ID after button press
if st.session_state.show_id_camera:
    id_photo = st.camera_input("قم بتصوير الهوية")
    if id_photo:
        st.success(" تم التقاط صورة الهوية")


if st.button(" إرسال البيانات"):
    if gender=="ذكر":
        if name and age and id and face and id_photo:
            sheet, drive_service = connect_to_services_M()
            folder_id = st.secrets["Male_Data"]["Male_Data"] 
            face_url = upload_image(face, drive_service, folder_id)
            id_url = upload_image(id_photo, drive_service, folder_id)

            sheet.append_row([name, gender, age, str(dateofbirth), id, face_url, id_url])
            st.success(" تم إرسال البيانات بنجاح إلى Google Sheet!")
        else:
            st.error(" يرجى تعبئة جميع الحقول والتقاط الصور أولاً.")
    else:
        if name and age and id and face and id_photo:
            sheet, drive_service = connect_to_services_F()
            folder_id = st.secrets["Female_Data"]["Female_Data"]
            face_url = upload_image(face, drive_service, folder_id)
            id_url = upload_image(id_photo, drive_service, folder_id)

            sheet.append_row([name, gender, age, str(dateofbirth), id, face_url, id_url])
            st.success(" تم إرسال البيانات بنجاح إلى Google Sheet!")
        else:
            st.error(" يرجى تعبئة جميع الحقول والتقاط الصور أولاً.")
