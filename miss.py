import streamlit as st
import base64
import random
import time
import pandas as pd

from face_match import compare_faces
from database import init_db, insert_person, get_all_persons, mark_found
from email_utils import send_email
from face_detection import detect_face
from translations import translations

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(page_title="Missing Person Finder", layout="wide")

# ---------------------------------------------------
# LOAD CSS
# ---------------------------------------------------
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

init_db()

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------
if "intro" not in st.session_state:
    st.session_state.intro = True

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------------------------------------------
# LANGUAGE
# ---------------------------------------------------
language = st.sidebar.selectbox("Language", ["English", "Telugu", "Hindi"])
t = translations[language]

# ---------------------------------------------------
# SPLASH SCREEN
# ---------------------------------------------------
if st.session_state.intro:

    st.markdown(f"<div class='title'>{t['title']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='subtitle'>{t['subtitle']}</div>", unsafe_allow_html=True)

    progress = st.progress(0)

    for i in range(100):
        time.sleep(0.02)
        progress.progress(i + 1)

    st.session_state.intro = False
    st.rerun()

# ---------------------------------------------------
# MAIN TITLE
# ---------------------------------------------------
st.title(t["title"])

role = st.sidebar.radio("Select Role", ["Family", "Police Camp"])

# ===================================================
# FAMILY SIDE
# ===================================================
if role == "Family":

    name = st.text_input(t["name"])
    location = st.text_input(t["location"])
    email = st.text_input(t["email"])
    uploaded_file = st.file_uploader(t["upload"], type=["jpg", "png", "jpeg"])

    if uploaded_file:

        st.image(uploaded_file, width=200)

        if detect_face(uploaded_file):
            st.success("Face detected")
        else:
            st.warning("No face detected")

    if "otp" not in st.session_state:
        st.session_state.otp = None
        st.session_state.otp_sent = False
        st.session_state.submitted = False

    if st.button(t["submit"]) and not st.session_state.otp_sent:

        if not uploaded_file or not name or not email:
            st.warning("Please fill all details")

        else:

            st.session_state.otp = random.randint(100000, 999999)

            send_email(
                email,
                "OTP Verification",
                f"Your OTP is {st.session_state.otp}\n--- Rescue Team"
            )

            st.session_state.otp_sent = True
            st.success("OTP sent to your email!")

    if st.session_state.otp_sent and not st.session_state.submitted:

        entered = st.text_input("Enter OTP")

        if st.button("Verify OTP"):

            if entered == str(st.session_state.otp):

                img_str = base64.b64encode(uploaded_file.getvalue()).decode()

                insert_person(name, email, location, img_str)

                st.success("Report Submitted Successfully")

                st.session_state.submitted = True

            else:
                st.error("Incorrect OTP")

# ===================================================
# POLICE SIDE
# ===================================================
elif role == "Police Camp":

    st.subheader(t["police_dashboard"])

    # -----------------------------
    # LOGIN
    # -----------------------------
    if not st.session_state.logged_in:

        user = st.text_input(t["username"])
        pw = st.text_input(t["password"], type="password")

        if st.button(t["login"]):

            if user == "admin" and pw == "admin123":

                st.session_state.logged_in = True
                st.success("Login Successful")
                st.rerun()

            else:
                st.error("Invalid credentials")

    else:

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

        persons = get_all_persons()

        if persons:

            df = pd.DataFrame(persons)

            # -----------------------------
            # DASHBOARD STATS
            # -----------------------------
            total = len(df)
            missing = len(df[df["status"] == "Missing"])
            found = len(df[df["status"] == "Found"])

            col1, col2, col3 = st.columns(3)

            col1.metric(t["total_cases"], total)
            col2.metric(t["missing_cases"], missing)
            col3.metric(t["solved_cases"], found)

            st.divider()

            # -----------------------------
            # GALLERY
            # -----------------------------
            st.subheader(t["gallery"])

            cols = st.columns(4)

            for i, person in enumerate(persons):

                with cols[i % 4]:

                    if person["image_data"]:
                        st.image(base64.b64decode(person["image_data"]))
                        st.caption(person["name"])

            st.divider()

            # -----------------------------
            # AI FACE MATCHING
            # -----------------------------
            st.subheader(t["ai_checker"])

            match_img = st.file_uploader(
                "Upload photo to check",
                type=["jpg", "png", "jpeg"],
                key="match"
            )

            if match_img:

                st.image(match_img, width=200)

                if st.button("Find Match"):

                    result = compare_faces(match_img, persons)

                    if result:

                        st.success("Possible Match Found!")

                        st.image(base64.b64decode(result["image_data"]), width=200)

                        st.write("Name:", result["name"])
                        st.write("Location:", result["location"])
                        st.write("Email:", result["email"])

                    else:
                        st.warning("No match found")

            st.divider()

            # -----------------------------
            # DATABASE RECORDS
            # -----------------------------
            st.write("### Records")

            for person in persons:

                with st.expander(person["name"]):

                    col1, col2 = st.columns([1, 2])

                    with col1:

                        if person["image_data"]:
                            st.image(base64.b64decode(person["image_data"]), width=150)

                    with col2:

                        st.write("Location:", person["location"])
                        st.write("Email:", person["email"])
                        st.write("Status:", person["status"])

                        if person["status"] == "Missing":

                            if st.button(
                                f"Mark {person['name']} as Found",
                                key=person["id"]
                            ):

                                mark_found(person["id"])

                                send_email(
                                    person["email"],
                                    "Good News!",
                                    f"{person['name']} has been found!"
                                )

                                st.success("Marked as Found")
                                st.rerun()

        else:
            st.info("No records found")

