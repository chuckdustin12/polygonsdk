
import requests
from bs4 import BeautifulSoup
import pdfplumber
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from urllib.request import url2pathname
import torch
import concurrent.futures
if torch.cuda.is_available():
    print("CUDA is enabled and available.")
    print("GPU:", torch.cuda.get_device_name(0))
else:
    print("CUDA is not available.")
from transformers import pipeline

import asyncio

async def summarize_url_or_path(url_or_path):
    loop = asyncio.get_event_loop()

    if url_or_path.lower().endswith('.html'):
        if url_or_path.startswith('http://') or url_or_path.startswith('https://'):
            text = await loop.run_in_executor(None, extract_html_text, url_or_path)
        else:
            if url_or_path.startswith('file://'):
                url_or_path = url_or_path[7:]
            file_path = url2pathname(url_or_path)
            text = await loop.run_in_executor(None, extract_html_text_from_file, file_path)
    elif url_or_path.lower().endswith('.pdf'):
        if url_or_path.startswith('http://') or url_or_path.startswith('https://'):
            text = await loop.run_in_executor(None, extract_pdf_text_from_url, url_or_path)
        else:
            if url_or_path.startswith('file://'):
                url_or_path = url_or_path[7:]
            file_path = url2pathname(url_or_path)
            text = await loop.run_in_executor(None, extract_pdf_text, file_path)
    else:
        return "Unsupported file format"

    summary = await loop.run_in_executor(None, create_summary, text)
        # Perform Sentiment Analysis on the original text
    sentiment_label, sentiment_score = await loop.run_in_executor(None, analyze_sentiment, text)
    
    # Perform Named Entity Recognition on the original text

    
    return {
        "summary": summary,
        "sentiment_label": sentiment_label,
        "sentiment_score": sentiment_score
    }

def create_sentiment_pipeline():
    sentiment_model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    sentiment_tokenizer = AutoTokenizer.from_pretrained(sentiment_model_name)
    sentiment_model = AutoModelForSequenceClassification.from_pretrained(sentiment_model_name)
    sentiment_pipeline = pipeline("sentiment-analysis", model=sentiment_model, tokenizer=sentiment_tokenizer)
    return sentiment_pipeline

sentiment_pipeline = create_sentiment_pipeline()
def analyze_sentiment(text):
    sentiment_results = []
    for i in range(0, len(text), 512):
        chunk = text[i:i+512]
        sentiment_results.extend(sentiment_pipeline(chunk))
    sentiment_label = [result['label'] for result in sentiment_results]
    sentiment_score = [result['score'] for result in sentiment_results]
    # You may decide how to aggregate the results - here just the most common label and average score are returned
    most_common_label = max(set(sentiment_label), key = sentiment_label.count)
    average_score = sum(sentiment_score)/len(sentiment_score)
    return most_common_label, average_score

def extract_html_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for script in soup(["script", "style"]):
        script.decompose()
    return ' '.join(soup.stripped_strings)

def extract_html_text_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    soup = BeautifulSoup(content, 'html.parser')
    for script in soup(["script", "style"]):
        script.decompose()
    return ' '.join(soup.stripped_strings)
def extract_pdf_text(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ' '.join(page.extract_text() for page in pdf.pages)
    return text
def extract_pdf_text_from_url(url):
    response = requests.get(url)
    with open("temp_pdf.pdf", "wb") as f:
        f.write(response.content)

    with pdfplumber.open("temp_pdf.pdf") as pdf:
        text = ' '.join(page.extract_text() for page in pdf.pages)
    return text
def tokenize(text, tokenizer):
    return tokenizer.encode(text, return_tensors="pt", add_special_tokens=True)

def split_text(text, tokenizer, max_length=1024):
    tokens = tokenize(text, tokenizer)
    token_chunks = []
    current_chunk = []

    for token in tokens[0]:
        if len(current_chunk) + 1 <= max_length:
            current_chunk.append(token.item())
        else:
            token_chunks.append(current_chunk)
            current_chunk = [token.item()]

    if current_chunk:
        token_chunks.append(current_chunk)

    return token_chunks



def create_summary(text):
    device = 0 if torch.cuda.is_available() else -1
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", device=device, framework="pt")
    tokenizer = summarizer.tokenizer
    token_chunks = split_text(text, tokenizer, max_length=1000)

    # Define a function to summarize a single chunk
    def summarize_chunk(chunk):
        chunk_text = tokenizer.decode(chunk, skip_special_tokens=True)
        summary_output = summarizer(chunk_text, max_length=100, min_length=25,batch_size=16, do_sample=False)
        return summary_output[0]['summary_text'].strip() if summary_output else ""

    summaries = []
    # Use a ThreadPoolExecutor to parallelize the summarization process
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        summaries = list(executor.map(summarize_chunk, token_chunks))

    # Join the summaries with newline characters to create paragraphs
    return "\n\n".join(summaries)

def save_summary_as_pdf(summary, filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    Story = []
    styles = getSampleStyleSheet()
    style = styles["BodyText"]

    lines = summary.split('\n')
    for line in lines:
        Story.append(Paragraph(line, style))
        Story.append(Spacer(1, 0.2 * inch))
    
    doc.build(Story)

# modify the main function
async def main():
    url_or_path = input("Please enter a URL or file path: ")
    result = await summarize_url_or_path(url_or_path)

    print("Summary: ", result['summary'])
    print("Sentiment Label: ", result['sentiment_label'])
    print("Sentiment Score: ", result['sentiment_score'])

    # Save the summary to a PDF
    save_summary_as_pdf(result['summary'], "files/summarized_pdfs/nscc_doc.pdf")

# Run the main function
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())