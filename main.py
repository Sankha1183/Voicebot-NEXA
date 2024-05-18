import streamlit as st
import requests
import webbrowser
import pyttsx3
import speech_recognition as sr
import googletrans
import re
from pytube import YouTube


# Function to perform Google search
def google_search(query, num_results=2):
    api_key = "AIzaSyA-WZ9vzyRjKpnJVH_uuWXg0LLM7K3ocfE"
    search_engine_id = "04ff519ffa85f48c6"

    url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={query}&num={num_results}"
    response = requests.get(url)
    data = response.json()

    if 'items' in data:
        results = data['items']
        formatted_snippets = []
        for result in results:
            snippet = result.get('snippet', 'No snippet available')
            snippet_without_dates = re.sub(
                r'\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2},?\s+\d{4}\b',
                '', snippet, flags=re.IGNORECASE)
            snippet_without_dates = re.sub(r'\b\d{4}\b', '', snippet_without_dates)
            sentences = re.split(r'[.;]', snippet_without_dates)
            bullet_points = "\n".join([f"- {sentence.strip()}" for sentence in sentences if sentence.strip()])
            formatted_snippets.append(bullet_points.strip())
        return "\n\n".join(formatted_snippets)
    else:
        return "Sorry, I couldn't find an answer to your question."


# Function to perform medical Google search
def medical_google_search(query, site="medlineplus.gov", num_results=3):
    api_key = "AIzaSyA-WZ9vzyRjKpnJVH_uuWXg0LLM7K3ocfE"
    search_engine_id = "04ff519ffa85f48c6"

    url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={query}&siteSearch={site}&num={num_results}"
    response = requests.get(url)
    data = response.json()

    if 'items' in data:
        results = data['items']
        formatted_snippets = []
        for result in results:
            snippet = result.get('snippet', 'No snippet available')
            snippet_without_dates = re.sub(
                r'\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2},?\s+\d{4}\b',
                '', snippet, flags=re.IGNORECASE)
            snippet_without_dates = re.sub(r'\b\d{4}\b', '', snippet_without_dates)
            sentences = re.split(r'[.;]', snippet_without_dates)
            bullet_points = "\n".join([f"- {sentence.strip()}" for sentence in sentences if sentence.strip()])
            formatted_snippets.append(bullet_points.strip())
        return "\n\n".join(formatted_snippets)
    else:
        return "Sorry, I couldn't find an answer to your medical query."


# Function to convert text to speech
def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()


# Function to listen to user input
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        st.write("Listening...")

        try:
            audio = recognizer.listen(source, timeout=7)
            st.write("Analyzing...")
            query = recognizer.recognize_google(audio)
            return query
        except sr.WaitTimeoutError:
            st.write("No speech detected within the timeout.")
            return ""
        except sr.UnknownValueError:
            st.write("Sorry, I couldn't understand what you said.")
            return ""
        except sr.RequestError as e:
            st.write(f"Could not request results from Google Speech Recognition service; {e}")
            return ""


# Streamlit UI
def main():
    st.title("VoiceMate - Your Personal Voice Assistant")

    st.sidebar.title("Menu")
    menu_choice = st.sidebar.radio("Select Option",
                                   ["Text Input", "Voice Input", "Medical Query", "Play YouTube Video"])

    if menu_choice == "Text Input":
        user_input = st.text_input("You:", "")
        if st.button("Send"):
            answer = google_search(user_input)
            speak(answer)

    elif menu_choice == "Voice Input":
        if st.button("Activate Mic"):
            st.write("Listening...")
            user_input = listen()
            st.write(f"You said: {user_input}")
            answer = google_search(user_input)
            speak(answer)

    elif menu_choice == "Medical Query":
        st.write("Please state your medical query:")
        if st.button("Start Recording"):
            st.write("Speak now...")
            query = listen()
            st.write(f"Your query: {query}")
            if st.button("Search"):
                answer = medical_google_search(query)
                speak(answer)

    elif menu_choice == "Play YouTube Video":
        st.write("Please say the name of the YouTube video you want to play:")
        if st.button("Start Recording"):
            st.write("Speak now...")
            video_query = listen()
            st.write(f"You said: {video_query}")
            if st.button("Search"):
                url = f"https://www.youtube.com/results?search_query={video_query}"
                webbrowser.open(url)


if __name__ == "__main__":
    main()
