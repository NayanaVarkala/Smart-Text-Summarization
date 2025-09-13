from flask import Flask, render_template, request
from text_summarizer import TextSummarizer
import os
import requests
from bs4 import BeautifulSoup
import docx
from PyPDF2 import PdfReader

app = Flask(__name__)
summarizer = TextSummarizer()

# -------- Helper Functions ----------
def read_file(file):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext == ".txt":
        return file.read().decode("utf-8")
    elif ext == ".pdf":
        reader = PdfReader(file)
        return " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif ext == ".docx":
        doc = docx.Document(file)
        return " ".join([para.text for para in doc.paragraphs])
    return ""

def fetch_website(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = [p.get_text() for p in soup.find_all("p")]
        return " ".join(paragraphs)
    except Exception as e:
        return f"⚠️ Failed to fetch website: {e}"

# -------- Routes ----------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    text = request.form.get("text", "").strip()
    url = request.form.get("url", "").strip()
    file = request.files.get("file")
    num_words = request.form.get("num_words", "").strip()

    # Convert num_words to integer, default 100
    try:
        num_words = int(num_words)
    except:
        num_words = 100

    # File input
    if file and file.filename != "":
        text = read_file(file)

    # URL input
    if url and text == "":
        text = fetch_website(url)

    # Generate full summary
    summary = summarizer.summarize(text) if text else "⚠️ No content provided."

    # Truncate to user-specified number of words
    words = summary.split()
    if len(words) > num_words:
        summary = " ".join(words[:num_words]) + "..."

    return render_template('result.html', summary=summary)

if __name__ == "__main__":
    app.run(debug=True)
