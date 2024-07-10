import streamlit as st
import time
import random
import string
import json
import os
import pandas as pd


# Function to generate a random keyword
def generate_keyword():
    length = random.randint(10, 20)
    characters = string.ascii_letters + string.digits
    keyword = ''.join(random.choice(characters) for _ in range(length))
    return keyword


def retry():
    st.session_state.keyword = generate_keyword()
    st.session_state.attempts = 0
    st.session_state.correct = False
    st.rerun()


# Initialize session state variables
if 'keyword' not in st.session_state:
    st.session_state.keyword = generate_keyword()
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'correct' not in st.session_state:
    st.session_state.correct = False
if 'godmode' not in st.session_state:
    st.session_state.godmode = False

keyword = st.session_state.keyword

st.set_page_config(page_title="TimePSW", page_icon="🔐", layout="wide")

cola, colb = st.columns([1, 1], gap="small")
cola.title("TimePSW 🔐")
colb.write("TimePSW is an engaging game designed to simulate a side-channel attack inspired by a vulnerability "
           "discovered in Apple's M1 and M2 chips. By analyzing the response time between requests, it is possible "
           "to determine various parameters. This game attempts to replicate that behavior, challenging players "
           "to guess a randomly generated password based on timing information alone.")
colb.link_button("Made w/ ❤️ | GitHub", "https://github.com/Jumitti")
cola.write("**Rules 🗒️**")
cola.write(
    "**1.** The length of the password varies between 10 and 15 characters.\n\n"
    "**2.** The password is composed of UPPER CASE, lower case and number.\n\n"
    "**3.** Length is the first parameter analyzed\n\n"
    "**4.** Your only clue... time... ⌚"
)

if st.session_state.godmode is True:
    cola.warning(f"💡The power of GODMODE gives you omniscience...and the password: {keyword}")

col1, col2, col3 = cola.columns([2, 0.5, 0.5], gap="small")
print(keyword)
user_input = col1.text_input("Try to guess the password:", max_chars=15, label_visibility="collapsed", placeholder="Try to guess the password")

if col2.button("Check"):
    start = time.time()

    if user_input == "Jumitti_ON":
        st.toast("GODMODE ACTIVATED")
        time.sleep(2)
        st.session_state.godmode = True
        retry()
    if user_input == "Jumitti_OFF":
        st.toast("GODMODE DEACTIVATED")
        time.sleep(2)
        st.session_state.godmode = False
        retry()

    correct = True
    if len(user_input) == len(keyword):
        for i in range(len(keyword)):
            time.sleep(0.01)
            if user_input[i] != keyword[i]:
                correct = False
                break
    else:
        correct = False

    end = time.time()
    elapsed_time = end - start

    st.session_state.attempts += 1

    cola.write(f'Attempts: {st.session_state.attempts} | Time (ms): {(elapsed_time * 1000):.5f}')
    if correct:
        cola.success("Congratulations! 🎉")
        st.balloons()
        st.session_state.correct = True
    else:
        cola.error("Incorrect password. Try again.")

if col3.button("Retry"):
    retry()

# Register winner
if st.session_state.correct and st.session_state.godmode is False:
    cola.write(f"You guessed the keyword {keyword} in {st.session_state.attempts} attempts.")
    colrs1, colrs2, colrs3 = cola.columns([2, 0.5, 0.5], gap="small")
    pseudo = colrs1.text_input("Enter your pseudo:", placeholder="Enter your pseudo", label_visibility="collapsed")
    if colrs2.button("Submit"):
        results = []
        if os.path.exists("results.json"):
            with open("results.json", "r") as file:
                results = json.load(file)
        results.append({"Pseudo": pseudo, "Attempts": st.session_state.attempts, "Password": keyword})
        with open("results.json", "w") as file:
            json.dump(results, file, indent=4)
        retry()
    if colrs3.button("Retry", key='1'):
        retry()

elif st.session_state.correct and st.session_state.godmode is True:
    colrs1, colrs2 = cola.columns([2, 0.5], gap="small")
    colrs1.warning("⚠️ GODMODE activated. You can't submit your result. Use Jumitti_OFF to leave GODMODE.")
    if colrs2.button("Retry", key='2'):
        retry()

# Display previous winners
if os.path.exists("results.json"):
    colb.write("**🕵🏽 Previous Winners:**")
    with open("results.json", "r") as file:
        results = json.load(file)
        df = pd.DataFrame(results)
        colb.dataframe(df, hide_index=True)
