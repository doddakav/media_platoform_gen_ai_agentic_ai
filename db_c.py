import mysql.connector
import streamlit as st

conn=mysql.connector.connect(
    host=st.secrets[""],
    user=st.secrets[""],
    password=st.secrets[""],
    database=st.secrets[""],
    port=st.secrets[""]
)

cursor=conn.cursor(dictionary=True)


 #FILES TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS files(
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    file_name VARCHAR(255),
    file_type VARCHAR(100),
    file_url TEXT,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

conn.commit()

print("Tables Created Successfully")



