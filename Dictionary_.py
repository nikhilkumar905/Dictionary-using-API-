import requests
import logging
import tkinter as tk
from tkinter import messagebox
import pyttsx3
import threading
import speech_recognition as sr

# Logging setup
logging.basicConfig(filename="dictionary.log", level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# TTS setup
engine = pyttsx3.init()
speak_thread = None
stop_speech_event = threading.Event()
last_result = ""

# Dictionary class
class Dictionary:
    def __init__(self, word):
        self.word = word.lower()
        self.api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{self.word}"

    def get_meaning(self):
        try:
            response = requests.get(self.api_url)
            if response.status_code == 200:
                data = response.json()
                meanings = data[0]["meanings"]
                definitions = []
                all_synonyms = set()
                all_antonyms = set()

                for meaning in meanings:
                    part_of_speech = meaning["partOfSpeech"]
                    all_synonyms.update(meaning.get("synonyms", []))
                    all_antonyms.update(meaning.get("antonyms", []))

                    for definition in meaning["definitions"]:
                        definition_text = definition["definition"]
                        all_synonyms.update(definition.get("synonyms", []))
                        all_antonyms.update(definition.get("antonyms", []))
                        definitions.append(f"({part_of_speech}) {definition_text}")

                synonyms_text = ", ".join(all_synonyms) if all_synonyms else "No synonyms available"
                antonyms_text = ", ".join(all_antonyms) if all_antonyms else "No antonyms available"

                result = "\n".join(definitions)
                result += f"\n\nSynonyms: {synonyms_text}\nAntonyms: {antonyms_text}"

                self.save_to_file(self.word)
                return result
            else:
                return "Word not found in the dictionary."
        except Exception as e:
            logging.error(str(e))
            return "An error occurred while fetching the meaning."

    def save_to_file(self, word):
        with open("word_history.txt", "a", encoding="utf-8") as file:
            file.write(f"{word}\n")

def search_word():
    global last_result
    word = entry.get().strip()
    if not word:
        messagebox.showerror("Input Error", "Please enter a word!")
        return

    dictionary = Dictionary(word)
    last_result = dictionary.get_meaning()
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, last_result)

def speak_meaning():
    global speak_thread, stop_speech_event

    if not last_result.strip():
        messagebox.showerror("Error", "Please search a word first before using text-to-speech.")
        return

    if speak_button.cget("text") == "⏹ Stop":
        stop_speech_event.set()
        engine.stop()
        speak_button.config(text="🔊 Speak")
    else:
        stop_speech_event.clear()

        def run_speak():
            speak_button.config(text="⏹ Stop")
            try:
                for line in last_result.splitlines():
                    if stop_speech_event.is_set():
                        break
                    engine.say(line)
                    engine.runAndWait()
            except Exception as e:
                logging.error(str(e))
            finally:
                speak_button.config(text="🔊 Speak")
                stop_speech_event.clear()

        speak_thread = threading.Thread(target=run_speak)
        speak_thread.start()

def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            messagebox.showinfo("Voice Input", "Speak the word now...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
            spoken_text = recognizer.recognize_google(audio)
            entry.delete(0, tk.END)
            entry.insert(0, spoken_text)
            search_word()
        except sr.UnknownValueError:
            messagebox.showerror("Voice Input", "Could not understand the audio.")
        except sr.RequestError:
            messagebox.showerror("Voice Input", "Could not connect to the speech recognition service.")
        except Exception as e:
            messagebox.showerror("Voice Input", f"Error: {str(e)}")

def show_history():
    try:
        with open("word_history.txt", "r", encoding="utf-8") as file:
            history = file.readlines()

        if not history:
            messagebox.showinfo("Search History", "No history found.")
            return

        history_window = tk.Toplevel(root)
        history_window.title("Search History")
        history_window.geometry("400x300")

        frame = tk.Frame(history_window)
        frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        history_text = tk.Text(frame, height=15, width=50, yscrollcommand=scrollbar.set)
        history_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=history_text.yview)

        for word in history:
            history_text.insert(tk.END, word)

        history_text.config(state=tk.DISABLED)

    except FileNotFoundError:
        messagebox.showinfo("Search History", "No history found.")
    except UnicodeDecodeError:
        messagebox.showerror("Error", "Could not read the history file due to encoding issues.")

def clear_history():
    confirm = messagebox.askyesno("Clear History", "Are you sure you want to delete the search history?")
    if confirm:
        try:
            open("word_history.txt", "w").close()
            messagebox.showinfo("Clear History", "Search history cleared successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

# GUI Setup
root = tk.Tk()
root.title("📘 Stylish Dictionary")
root.geometry("600x560")
root.config(bg="#1f1f2e")
root.resizable(False, False)

font_title = ("Helvetica", 16, "bold")
font_button = ("Helvetica", 11, "bold")

bg_frame = tk.Frame(root, bg="#2c3e50", bd=0)
bg_frame.place(relwidth=1, relheight=1)

card = tk.Frame(bg_frame, bg="#ffffff", bd=0, relief=tk.RAISED)
card.place(relx=0.5, rely=0.08, anchor="n", width=500, height=480)
card.configure(highlightbackground="#aaa", highlightthickness=1)

tk.Label(card, text="💡 Enter a Word", font=font_title, bg="#ffffff", fg="#2c3e50").pack(pady=10)
entry = tk.Entry(card, width=35, font=("Helvetica", 13), bd=2, relief=tk.GROOVE, justify="center")
entry.pack(pady=5)

def styled_btn(text, command, color):
    return tk.Button(card, text=text, width=20, height=1, command=command,
                     bg=color, fg="white", font=font_button,
                     activebackground="#000", activeforeground="white",
                     relief="flat", cursor="hand2")

styled_btn("🔍 Search", search_word, "#4CAF50").pack(pady=5)
speak_button = styled_btn("🔊 Speak", speak_meaning, "#2196F3")
speak_button.pack(pady=5)
styled_btn("🎤 Voice Input", voice_input, "#FF9800").pack(pady=5)
styled_btn("📜 View History", show_history, "#9C27B0").pack(pady=5)
styled_btn("🗑️ Clear History", clear_history, "#f44336").pack(pady=5)

result_text = tk.Text(card, height=10, width=60, font=("Courier New", 10),
                      wrap=tk.WORD, bg="#f7f9fa", fg="#333", bd=1, relief=tk.GROOVE)
result_text.pack(pady=10)

def on_enter(e): e.widget.config(bg="#111")
def on_leave(e): e.widget.config(bg=e.widget.original_color)

for widget in card.winfo_children():
    if isinstance(widget, tk.Button):
        widget.original_color = widget.cget("bg")
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

def pulse():
    current = card.cget("highlightbackground")
    next_color = "#ff6f61" if current == "#aaa" else "#aaa"
    card.config(highlightbackground=next_color)
    root.after(800, pulse)

pulse()
root.mainloop()
