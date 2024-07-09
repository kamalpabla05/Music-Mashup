import streamlit as st
import os
import zipfile
from io import BytesIO
import smtplib
from email.message import EmailMessage
import subprocess
import shutil

def create_mashup(singer_name, num_videos, duration, output_filename):
    cmd = f"python Mashup.py \"{singer_name}\" {num_videos} {duration} {output_filename}"
    subprocess.run(cmd, shell=True)

def create_zip_and_send_email(mp3_filename, email):
    # Create a zip file
    zip_filename = mp3_filename.replace(".mp3", ".zip")
    with zipfile.ZipFile(zip_filename, "w") as zipf:
        zipf.write(mp3_filename)
    
    # Send email with zip file attachment
    msg = EmailMessage()
    msg["Subject"] = f"Mashup MP3 for {os.path.basename(mp3_filename)}"
    msg["From"] = "your_email@example.com"
    msg["To"] = email
    msg.set_content(f"Here is the mashup MP3 for {os.path.basename(mp3_filename)}")
    
    with open(zip_filename, "rb") as f:
        zip_content = f.read()
        msg.add_attachment(zip_content, maintype="application", subtype="zip", filename=zip_filename)
    
    with smtplib.SMTP("smtp.gmail.com", 587) as server:  
        server.starttls()
        server.login("sanchita5628@gmail.com", "poufjpkiwcyznnle")  
        server.send_message(msg)
    
    shutil.rmtree('Audios')
    shutil.rmtree('Videos')
    shutil.rmtree('Trim')
    os.remove(zip_filename)
    os.remove(mp3_filename)

def main():
    st.title("Welcome to Youtube Merger - Creating Mashups instantly")
    
    singer_name = st.text_input("Enter Singer Name")
    num_videos = st.number_input("Number of Videos", min_value=1, step=1)
    duration = st.number_input("Duration of Each Video (in seconds)", min_value=1, step=1)
    output_filename = st.text_input("Enter Output File Name (without extension, file will be mp3)")
    email = st.text_input("Enter Email")
    
    if st.button("Create Mashup and Send Email"):
        create_mashup(singer_name, num_videos, duration, output_filename + ".mp3")
        create_zip_and_send_email(output_filename + ".mp3", email)
        st.success("Mashup created and is sent over email!")

if __name__ == "__main__":
    main()

