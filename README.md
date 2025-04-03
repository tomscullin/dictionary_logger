# 📓 Japanese-to-English Dictionary Logger

A simple Python app to help Japanese learners track the words they look up and collect example sentences for later review or flashcard creation.  
This project is part of my **"Learning Python in Public"** journey and builds toward my long-term goal of creating language analysis and study tools.

---

## 🚀 Project Goals

- Look up Japanese words and store their meanings.
- Automatically log each lookup with the date, time, and an optional example sentence.
- Make it easy to review all the words you looked up today.
- Help Japanese learners collect real, meaningful data from their own studies.

---

## 🌱 Why I’m Building This

I'm learning Python with the goal of building better language-learning tools, like media study guides and language analysis apps.  
This is a small, real-world project that helps me practice:

- File handling
- Databases
- Command-line interfaces
- Handling Japanese text (UTF-8)
- Organizing data for language learning

---

## ✅ Current Features

- Lookup a word (dummy data for now — real dictionary API coming soon!)
- Log word, meaning, date/time, and optional example sentence
- View today’s log
- Simple, clean CLI interface

---

## 🔥 Planned Features (Coming Soon!)

- Real Japanese dictionary lookup using Jisho API or JMdict
- SQLite database storage
- Search and filter by date, tag, or frequency
- Export to CSV or Anki-friendly format
- Optional tags/labels for each word (e.g., grammar, slang, media source)
- Auto-suggest example sentences
- GUI version (stretch goal)

---

## 📝 TODO List

### MVP Completion (Week 1)

- [x] Project setup and README
- [x] Basic JSON file storage
- [x] `lookup_word()` function (dummy data)
- [x] `log_word()` function
- [x] `get_todays_log()` function
- [x] Simple CLI interface
- [x] Basic error handling
- [x] Testing

### Next Steps

- [ ] Add “View full log” option
- [ ] Add option to edit/delete entries
- [ ] Switch to SQLite
- [ ] Integrate real dictionary API
- [ ] Add search/filter options
- [ ] Export feature
- [ ] Optional: Build GUI

---

## 🧩 How to Use (MVP)

Clone the repo:

```bash
git clone https://github.com/YOUR_USERNAME/dictionary-logger.git
cd dictionary-logger
```

Run the app:

```bash
python main.py
```

Follow the prompts to look up and log new words.

---

## 📣 Follow My Learning Journey

I’m documenting my progress, mistakes, and what I learn as I build this project.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
