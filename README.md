Dictionary using API!

A sleek, modern dictionary desktop app built using Python's tkinter GUI, powered by the Free Dictionary API. It allows you to search for word meanings, synonyms, antonyms, and even hear the results aloud. It also supports voice input and keeps track of your search history.

✨ Features
🔍 Search Meaning: Enter a word to get definitions, synonyms, and antonyms.

🔊 Text-to-Speech: Hear the meaning read aloud.

🎤 Voice Input: Speak a word to search using your microphone.

📜 Search History: View all previously searched words.

🗑️ Clear History: Remove all saved search history.

📁 Logging: Logs any unexpected errors to dictionary.log for easy debugging.

🛠️ Technologies Used
Python 3

tkinter – GUI

requests – API calls

pyttsx3 – Offline Text-to-Speech

speech_recognition – Voice input

logging – Error logging

📷 GUI Preview
<img src="https://via.placeholder.com/600x400?text=Add+Screenshot+Here" alt="App Screenshot" />
💡 You can replace the image link with a real screenshot of your app.

🚀 Getting Started
🔧 Prerequisites
Make sure you have the following Python libraries installed:

bash
Copy
Edit
pip install requests pyttsx3 SpeechRecognition
If using voice input, you may also need:

bash
Copy
Edit
pip install pyaudio
For Windows, if pyaudio gives errors, install it using:

bash
Copy
Edit
pip install pipwin
pipwin install pyaudio
🧩 How to Run
bash
Copy
Edit
python your_script_name.py
📂 Files
main.py – Your main GUI and app logic

dictionary.log – Stores runtime errors
[Screenshot 2025-04-14 125808](https://github.com/user-attachments/assets/24d88d94-88dc-4dea-b326-3ab18e47a5dc)

word_history.txt – Keeps a record of searched words

🧠 Inspiration
This project was built to provide a beautiful, beginner-friendly dictionary tool with modern features like voice input and TTS, ideal for learners and developers alike.

