from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
import datetime
import re
from collections import Counter
import requests
from bs4 import BeautifulSoup
import PyPDF2
from docx import Document

app = Flask(__name__)
app.secret_key = "resumeproject2024"
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

def setup_database():
    conn = sqlite3.connect("summaries.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            source_type TEXT NOT NULL DEFAULT 'text',
            source_label TEXT NOT NULL DEFAULT '',
            original_text TEXT NOT NULL,
            summary TEXT NOT NULL,
            word_count INTEGER,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

setup_database()

STOP_WORDS = {
    "a","an","the","and","or","but","in","on","at","to","for","of","with","by","from",
    "is","was","are","were","be","been","being","have","has","had","do","does","did",
    "will","would","could","should","may","might","shall","can","that","this","these",
    "those","it","its","i","we","you","he","she","they","me","him","her","us","them",
    "my","your","his","our","their","not","no","so","as","if","then","than","when",
    "which","who","what","where","how","also","just","more","about","up","out","into",
    "over","after","before","between","through","during","s"
}

def summarize_text(text, target_words=100):
    text = text.strip()
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    if not sentences:
        return text[:500]
    all_words = re.findall(r'\b[a-z]{3,}\b', text.lower())
    word_freq = Counter(w for w in all_words if w not in STOP_WORDS)
    def score(s):
        words = re.findall(r'\b[a-z]{3,}\b', s.lower())
        return sum(word_freq.get(w,0) for w in words if w not in STOP_WORDS) - len(words)/20
    scored = sorted([(score(s), i, s) for i, s in enumerate(sentences)], reverse=True)
    selected, total = set(), 0
    for sc, idx, sentence in scored:
        wc = len(sentence.split())
        if total + wc <= target_words * 1.2:
            selected.add(idx)
            total += wc
        if total >= target_words:
            break
    if not selected:
        selected.add(0)
    return " ".join(sentences[i] for i in sorted(selected))

def extract_from_url(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script","style","nav","footer","header","aside","form"]):
            tag.decompose()
        text = re.sub(r'\s+', ' ', soup.get_text(separator=" ", strip=True)).strip()
        return text[:8000], None
    except requests.exceptions.MissingSchema:
        return None, "Invalid URL. Make sure it starts with http:// or https://"
    except requests.exceptions.ConnectionError:
        return None, "Could not connect to that website. Please check the URL."
    except requests.exceptions.Timeout:
        return None, "The website took too long to respond. Please try again."
    except Exception as e:
        return None, f"Could not fetch the URL: {str(e)}"

def extract_from_pdf(file):
    try:
        reader = PyPDF2.PdfReader(file)
        text = "".join((page.extract_text() or "") + "\n" for page in reader.pages).strip()
        if not text:
            return None, "Could not read text from this PDF. It may be a scanned image."
        return text, None
    except Exception as e:
        return None, f"Error reading PDF: {str(e)}"

def extract_from_docx(file):
    try:
        doc = Document(file)
        text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
        if not text:
            return None, "The Word document appears to be empty."
        return text, None
    except Exception as e:
        return None, f"Error reading Word document: {str(e)}"

def extract_from_txt(file):
    try:
        text = file.read().decode("utf-8", errors="ignore").strip()
        if not text:
            return None, "The text file appears to be empty."
        return text, None
    except Exception as e:
        return None, f"Error reading file: {str(e)}"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET","POST"])
def register():
    error = ""
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        if not username or not password:
            error = "Please fill in all fields."
        elif len(username) < 3:
            error = "Username must be at least 3 characters."
        elif len(password) < 4:
            error = "Password must be at least 4 characters."
        else:
            conn = sqlite3.connect("summaries.db")
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                session["username"] = username
                return redirect(url_for("dashboard"))
            except sqlite3.IntegrityError:
                error = "That username is already taken. Please choose another."
            finally:
                conn.close()
    return render_template("register.html", error=error)

@app.route("/login", methods=["GET","POST"])
def login():
    error = ""
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        conn = sqlite3.connect("summaries.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            error = "Wrong username or password. Please try again."
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("home"))

@app.route("/dashboard", methods=["GET","POST"])
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    summary = ""
    error = ""
    original = ""
    word_count = 0
    active_tab = "text"
    if request.method == "POST":
        source_type = request.form.get("source_type", "text")
        active_tab = source_type
        target = int(request.form.get("word_count", 100))
        content = ""
        source_label = ""
        if source_type == "text":
            content = request.form.get("text_input", "").strip()
            source_label = "Pasted Text"
            if not content:
                error = "Please enter some text to summarize."
            elif len(content.split()) < 10:
                error = "Please enter at least 10 words for a meaningful summary."
        elif source_type == "url":
            url = request.form.get("url_input", "").strip()
            source_label = url[:80] if url else "URL"
            if not url:
                error = "Please enter a URL."
            else:
                content, error = extract_from_url(url)
        elif source_type == "file":
            file = request.files.get("file_upload")
            if not file or file.filename == "":
                error = "Please choose a file to upload."
            else:
                source_label = file.filename
                ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
                if ext == "pdf":
                    content, error = extract_from_pdf(file)
                elif ext == "docx":
                    content, error = extract_from_docx(file)
                elif ext in ("txt","md"):
                    content, error = extract_from_txt(file)
                else:
                    error = f"Unsupported file type '.{ext}'. Please upload PDF, DOCX, or TXT."
        if not error and content:
            original = content
            summary = summarize_text(content, target)
            word_count = len(summary.split())
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            conn = sqlite3.connect("summaries.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO summaries (username, source_type, source_label, original_text, summary, word_count, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (session["username"], source_type, source_label, original[:3000], summary, word_count, now)
            )
            conn.commit()
            conn.close()
    return render_template("dashboard.html", summary=summary, error=error, original=original,
                           word_count=word_count, username=session["username"], active_tab=active_tab)

@app.route("/history")
def history():
    if "username" not in session:
        return redirect(url_for("login"))
    conn = sqlite3.connect("summaries.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, source_type, source_label, summary, word_count, created_at FROM summaries WHERE username=? ORDER BY id DESC",
        (session["username"],)
    )
    rows = cursor.fetchall()
    conn.close()
    return render_template("history.html", rows=rows, username=session["username"])

@app.route("/delete/<int:summary_id>")
def delete(summary_id):
    if "username" not in session:
        return redirect(url_for("login"))
    conn = sqlite3.connect("summaries.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM summaries WHERE id=? AND username=?", (summary_id, session["username"]))
    conn.commit()
    conn.close()
    return redirect(url_for("history"))

if __name__ == "__main__":
    app.run(debug=True)
