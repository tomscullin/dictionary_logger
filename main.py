# Japanese-to-English Dictionary Logger

import json
import os
from datetime import datetime

LOG_FILE = "word_log.json"

# ===========================
# MVP FUNCTIONALITY TODOs
# ===========================
# TODO-1: Replace dummy data with API call to Jisho or JMdict for lookup_word function
# TODO-2: Use Jisho or Tatoeba API to auto-generate example sentences

# ===========================
# NICE-TO-HAVE TODOs
# ===========================
# TODO-A1: Add option to log multiple example sentences
# TODO-A2: Add "View full log" option
# TODO-A3: Add option to edit or delete entries
# TODO-A4: Switch from JSON to SQLite for data storage
# TODO-A5: Add export feature to CSV/Anki-friendly format

# ===========================
# STRETCH GOALS / ADVANCED
# ===========================
# TODO-B1: Add tags/categories (noun, verb, grammar, slang, etc.)
# TODO-B2: Add search/filter options (by date, tag, frequency)
# TODO-B3: Build a simple GUI version (Tkinter, PySimpleGUI)

def load_log():
    if not os.path.exists(LOG_FILE):
        return {}
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_log(log_data):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=4)


def lookup_word(word):
    # Dummy data for MVP. Replace with API call later.
    # Use API or hardcoded dictionary for MVP
    return {"word": word, "meaning": "(English meaning placeholder)"}


def log_word(word_data, sentence=None):
    # Save word, meaning, sentence, date/time to SQLite
    log = load_log()
    today = datetime.now().strftime("%Y-%m-%d")
    entry = {
        "word": word_data["word"],
        "meaning": word_data["meaning"],
        "sentence": sentence or "",
        "time": datetime.now().strftime("%H:%M")
    }
    log.setdefault(today, []).append(entry)
    save_log(log)
    print(f"Logged: {entry['word']} - {entry['meaning']}")


def get_todays_log():
     # Fetch and display today's lookups
    log = load_log()
    today = datetime.now().strftime("%Y-%m-%d")
    entries = log.get(today, [])
    if not entries:
        print("No words logged today.")
        return
    print(f"\nToday's Log ({today}):")
    for entry in entries:
        print(f"- {entry['word']}: {entry['meaning']} | {entry['sentence']} ({entry['time']})")


def main():
    # CLI loop
    while True:
        print("\n--- Japanese Dictionary Logger ---")
        print("1. Look up a word")
        print("2. View today's log")
        print("3. Quit")
        choice = input("Choose an option: ")

        if choice == "1":
            word = input("Enter Japanese word: ")
            result = lookup_word(word)
            print(f"Meaning: {result['meaning']}")
            sentence = input("Add an example sentence? (optional): ")
            log_word(result, sentence)
        elif choice == "2":
            get_todays_log()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
