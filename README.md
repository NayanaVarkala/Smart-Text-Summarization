# Smart Text Summarizer 💡

A full-stack web application that instantly generates concise, accurate summaries from text, URLs, PDFs, and Word documents — with user accounts, saved history, and adjustable summary length.

 was a static HTML prototype. **v2** is a complete Flask application with a database, authentication, and multi-format file support.



## 📸 Screenshots

### 🏠 Dashboard — Paste Text
![Dashboard Text](screenshots/dashboard-text.png)
![Dashboard Text Result](screenshots/dashboard-text-result.png)

### 🌐 Dashboard — From URL
![Dashboard URL](screenshots/dashboard-url.png)
![Dashboard URL Result](screenshots/dashboard-url-result.png)

### 📂 Dashboard — Upload File (PDF / DOCX)
![Dashboard File](screenshots/dashboard-file.png)
![Dashboard File Result](screenshots/dashboard-file-result.png)

### 📚 Summary History
![History](screenshots/history.png)
![History Detail](screenshots/history-detail.png)

---

## ✨ What's New in v2

| Feature | v1 (HTML only) | v2 (Flask + Python) |
|---|---|---|
| Summarization | Basic client-side | Custom Python TF-IDF algorithm |
| Input types | Text only | Text, URL, PDF, DOCX, TXT |
| User accounts | ❌ | ✅ Register, login, logout |
| Save summaries | ❌ | ✅ Stored per user in SQLite |
| Summary history | ❌ | ✅ View and delete past summaries |
| Summary length | Fixed | Adjustable (30–500 words) |
| Data privacy | ❌ | ✅ Each user sees only their own data |

---

## 🚀 Features

- **Multi-format input** — paste text, enter a URL, or upload PDF / DOCX / TXT files
- **Custom summarization engine** — built from scratch in Python using TF-IDF style sentence scoring (no paid AI API)
- **User authentication** — register and log in to your private account
- **Summary history** — all summaries saved to your account; delete anytime
- **Adjustable length** — choose summary length from 30 to 500 words using an interactive slider
- **Responsive UI** — clean, mobile-friendly design built with vanilla HTML & CSS

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | SQLite (built into Python) |
| Frontend | HTML, CSS (vanilla) |
| Summarization | Custom Python algorithm |
| Web scraping | BeautifulSoup, Requests |
| PDF parsing | pypdf |
| DOCX parsing | python-docx |

---

## ⚙️ How to Run

### 1. Clone the repo
```bash
git clone https://github.com/NayanaVarkala/Smart-Text-Summarization.git
cd Smart-Text-Summarization
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Start the app
```bash
python app.py
```

### 4. Open in browser
```
http://localhost:5000
```

No API keys. No paid services. No extra setup.

---

## 🧠 How the Summarizer Works

1. Splits the input into individual sentences
2. Counts word frequencies (ignoring common stop words like "the", "is", etc.)
3. Scores each sentence by how many high-frequency words it contains
4. Selects the top-scoring sentences up to your chosen word limit
5. Returns them in original order for a natural-reading summary

This is the same fundamental approach used by many professional summarization tools — built entirely from scratch in plain Python.

---

## 📁 Project Structure

```
Smart-Text-Summarization/
├── app.py                      ← All backend logic (routes + summarizer)
├── requirements.txt            ← Python dependencies
├── static/
│   └── style.css               ← All styles
├── templates/
│   ├── home.html               ← Landing page
│   ├── register.html           ← Sign up
│   ├── login.html              ← Log in
│   ├── dashboard.html          ← Summarize (text / URL / file)
│   └── history.html            ← View & delete saved summaries
└── screenshots/                ← App screenshots for README
```

---

## 📄 Pages

- **Home** — landing page with feature overview and how-it-works steps
- **Register / Login** — create an account or sign in
- **Dashboard** — choose input type, set summary length, generate summary
- **History** — view all past summaries with source type, word count, and date
