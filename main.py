import requests
import json
import os
import webbrowser
import sqlite3
import csv
from datetime import datetime

DB_FILE = "database.sqlite"
JSON_LOG_FILE = "word_log.json"

# ===========================
# DATABASE SETUP
# ===========================

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS words (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    word TEXT,
                    meaning TEXT,
                    sentences TEXT,
                    tags TEXT,
                    time TEXT
                )''')

    # Add tags column if missing (for upgrades)
    try:
        c.execute("ALTER TABLE words ADD COLUMN tags TEXT")
    except sqlite3.OperationalError:
        pass  # Already exists

    conn.commit()
    conn.close()

# ===========================
# API CALLS
# ===========================

def lookup_word(word):
    url = f"https://jisho.org/api/v1/search/words?keyword={word}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["data"]:
            entry = data["data"][0]
            meaning = ", ".join(entry["senses"][0]["english_definitions"])

            # Extract tags
            tags = set()

            # Add part of speech
            for pos in entry["senses"][0].get("parts_of_speech", []):
                tags.add(pos.lower().replace(" ", "_"))

            # Add JLPT tag
            for jlpt_tag in entry.get("jlpt", []):
                tags.add(jlpt_tag.lower())

            # Common word check
            if entry.get("is_common"):
                tags.add("common_word")

            return {
                "word": word,
                "meaning": meaning,
                "auto_tags": sorted(tags)
            }

    return {"word": word, "meaning": "Meaning not found.", "auto_tags": []}

def get_example_sentences(word, max_examples=2):
    url = f"https://tatoeba.org/eng/api_v0/search?query={word}&from=jpn&to=eng"
    response = requests.get(url)
    sentences = []
    if response.status_code == 200:
        data = response.json()
        for result in data.get("results", []):
            jp = result.get("text", "")
            translations = result.get("translations", [])
            flat_translations = []
            for item in translations:
                if isinstance(item, list):
                    flat_translations.extend(item)
                elif isinstance(item, dict):
                    flat_translations.append(item)
            for t in flat_translations:
                eng = t.get("text", "")
                if jp and eng:
                    sentences.append(f"{jp} - {eng}")
                    break
            if len(sentences) >= max_examples:
                break
    return sentences

def open_jpdb(word):
    url = f"https://jpdb.io/search?q={word}"
    print(f"🌐 Opening JPDB.io in your browser: {url}")
    webbrowser.open(url)

# ===========================
# JSON LOG FUNCTIONS
# ===========================

def load_json_log():
    if not os.path.exists(JSON_LOG_FILE):
        return {}
    with open(JSON_LOG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json_log(log_data):
    with open(JSON_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=4)

# ===========================
# EXPORT TO CSV
# ===========================

def export_log_to_csv(filename="word_log_export.csv"):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT date, word, meaning, sentences, tags, time FROM words ORDER BY date")
    entries = c.fetchall()
    conn.close()

    if not entries:
        print("📭 No entries to export.")
        return

    with open(filename, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Word", "Meaning", "Sentences", "Tags", "Time"])
        for date, word, meaning, sentences, tags, time in entries:
            sentence_str = " | ".join(json.loads(sentences))
            writer.writerow([date, word, meaning, sentence_str, tags, time])

    print(f"✅ Log exported to {filename}")

# ===========================
# LOGGING FUNCTION
# ===========================

def log_word(word_data, sentences, tags):
    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%H:%M")
    tag_string = ", ".join(tags)

    # Save to SQLite
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO words (date, word, meaning, sentences, tags, time) VALUES (?, ?, ?, ?, ?, ?)",
              (today, word_data["word"], word_data["meaning"],
               json.dumps(sentences, ensure_ascii=False), tag_string, now))
    conn.commit()
    conn.close()

    # Save to JSON
    log = load_json_log()
    entry = {
        "word": word_data["word"],
        "meaning": word_data["meaning"],
        "sentences": sentences,
        "tags": tags,
        "time": now
    }
    log.setdefault(today, []).append(entry)
    save_json_log(log)

    print(f"✅ Logged: {word_data['word']} - {word_data['meaning']} (tags: {tag_string})")

# ===========================
# LOG VIEWERS
# ===========================

def get_todays_log():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    c.execute("SELECT word, meaning, sentences, tags, time FROM words WHERE date = ?", (today,))
    entries = c.fetchall()
    conn.close()
    if not entries:
        print("📭 No words logged today.")
        return
    print(f"\n📅 Today's Log ({today}):")
    for word, meaning, sentences, tags, time in entries:
        sentence_list = json.loads(sentences)
        print(f"- {word}: {meaning}")
        print(f"  🔖 Tags: {tags}")
        for s in sentence_list:
            print(f"    • {s} ({time})")

def view_full_log():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT date, word, meaning, sentences, tags, time FROM words ORDER BY date")
    entries = c.fetchall()
    conn.close()
    if not entries:
        print("📘 Log is empty.")
        return
    print("\n📖 Full Log:")
    for date, word, meaning, sentences, tags, time in entries:
        print(f"{date} - {word}: {meaning}")
        print(f"  🔖 Tags: {tags}")
        for s in json.loads(sentences):
            print(f"    • {s} ({time})")

# ===========================
# MAIN CLI
# ===========================

def main():
    init_db()
    while True:
        print("\n--- Japanese Dictionary Logger ---")
        print("1. Look up a word")
        print("2. View today's log")
        print("3. View full log")
        print("4. Export log to CSV")
        print("5. Quit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            word = input("Enter Japanese word: ").strip()
            result = lookup_word(word)
            print(f"🈶 Meaning: {result['meaning']}")
            print("🔎 Fetching example sentences from Tatoeba...")
            sentences = get_example_sentences(word)

            if sentences:
                print("📖 Examples:")
                for i, s in enumerate(sentences, 1):
                    print(f"{i}. {s}")
            else:
                print("⚠️ No example sentences found.")

            auto_tags = result.get("auto_tags", [])
            print(f"🔖 Auto-tags: {', '.join(auto_tags) if auto_tags else 'None found'}")

            tag_input = input("Add more tags? (comma-separated or leave blank): ").strip()
            user_tags = [tag.strip().lower().replace(" ", "_") for tag in tag_input.split(",") if tag.strip()]
            tags = sorted(set(auto_tags + user_tags))

            while True:
                followup = input("Would you like a (c)ustom sentence, a (j)pdb lookup, or (n)one? ").lower().strip()
                if followup == "c":
                    custom_sentence = input("Enter your sentence: ").strip()
                    if custom_sentence:
                        sentences.append(custom_sentence)
                    break
                elif followup == "j":
                    open_jpdb(word)
                    break
                elif followup == "n":
                    break
                else:
                    print("❌ Invalid option. Choose c, j, or n.")

            log_word(result, sentences, tags)

        elif choice == "2":
            get_todays_log()

        elif choice == "3":
            view_full_log()

        elif choice == "4":
            export_log_to_csv()

        elif choice == "5":
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
