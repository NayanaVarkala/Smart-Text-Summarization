# Smart Text Summarization

**Smart Text Summarization** is a web-based application that generates concise and meaningful summaries from large text inputs. It helps users quickly grasp the key points of articles, documents, PDFs, Word files, or web pages, saving time and improving productivity.

## Features
- Summarizes plain text, PDFs, DOCX files, and web URLs.
- Allows users to customize the summary length (number of words).
- Beautiful, user-friendly interface with a colorful, gradient background.
- Responsive design for desktop and mobile devices.
- Fast and efficient summarization using Python.

## Technologies Used
- **Backend:** Python, Flask
- **Frontend:** HTML, CSS
- **Libraries:** BeautifulSoup, PyPDF2, python-docx, Requests

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/NayanaVarkala/Smart-Text-Summarization.git
Navigate into the project directory:


*** cd Smart-Text-Summarization ***
Create and activate a virtual environment:
***
python3 -m venv venv
source venv/bin/activate 
***
Install required packages:

***
pip install -r requirements.txt
***
Run the application:
***
python3 app.py
***
Open your browser and go to:

http://127.0.0.1:5000/

Usage
Enter text, upload a TXT, PDF, or DOCX file, or provide a URL.

Specify the number of words for the summary (optional).

Click Summarize to view the summary on the results page.

Use the Go Back button to summarize more content.
