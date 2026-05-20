import streamlit as st
from db_c import conn,cursor
import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name=st.secrets["cloud_name"],
    api_key=st.secrets["api_key"],
    api_secret=st.secrets["api_secrets"]
)
if "user" not in st.session_state:
    st.session_state.user=None

def dashboard():
    st.sidebar.success("Welcome to Dashboard")
    opt=st.sidebar.selectbox("choose",["upload Files","View Files","Logout"])
    st.header("Dashboard")
    if opt=="upload Files":
        st.header("Upload Files")
        choose_file=st.file_uploader("choose file",type=["pdf","jpg","jpeg","png","mp3","mp4"])
        if choose_file:
            st.write(choose_file.name)
            st.write(choose_file.type)
        if choose_file is not None:
            if "image" in choose_file.type:
                st.image(choose_file,width=200)
            elif "video" in choose_file.type:
                st.video(choose_file)
            elif "audio" in choose_file.type:
                st.audio(choose_file)

        if st.button("upload file to cloudinary"):
            uploaded_dict_obj=cloudinary.uploader.upload(choose_file,resource_type="auto") 
            url=uploaded_dict_obj["secure_url"]             
            
            
            cursor.execute("insert into files(user_id,file_name,file_type,file_url) values(%s,%s,%s,%s)",(
                st.session_state.user["id"],choose_file.name,choose_file.type,url))
            conn.commit()
            st.success("file uploaded to cloudinary")
    elif opt=="View Files":
        st.header("Your Files")
        cursor.execute("select * from files where user_id=%s",(st.session_state.user["id"],))
        files=cursor.fetchall()
        if files:
            for file in files:
                st.write("File", file["file_name"])
                st.write("Uploaded",file["upload_date"])
                if "image" in file["file_type"]:
                    st.image(file["file_url"])
                elif "video" in file["file_type"]:
                    st.video(file["file_url"])

                elif "audio" in file["file_type"]:
                    st.audio(file["file_url"])
                else:
                    st.link_button("open_file",file["file_url"])
        else:
            st.warning("Non files Uploaded")


    elif opt == "Logout":
        st.session_state.user=None
        st.success("logout successfully...")
        st.rerun()
st.title("Media Platform")

def Signup_function():
    with st.form("Signup form"):
        st.header("Signup form")
        name=st.text_input("Name")
        email=st.text_input("Email")
        password=st.text_input("password",type="password")
        btn=st.form_submit_button("Signup")
        if btn:
            cursor.execute("""insert into users (name,email,password)values(%s,%s,%s)""",(name,email,password)
            )
            conn.commit()
            st.success("Signup successfull")

def Login_function():
    with st.form("Login form"):
        st.header("Login form")
        email=st.text_input("Email")
        password=st.text_input("password",type="password")
        btn=st.form_submit_button("Login")

        if btn:
            cursor.execute("""select * from users where email=%s and password=%s""",(email,password)
            )
            logged_user=cursor.fetchone()
            st.session_state.user = logged_user
            st.write("loggedin succesfully")
            st.rerun()

            if logged_user:
                st.success("Login successful")
            else:
                st.error("Invalid Credential")
if st.session_state.user==None:
    Login,Signup=st.tabs(
        ["Login","Signup"]
    )
    with Signup:
        Signup_function()
    with Login:
        Login_function()
else:
    dashboard()




