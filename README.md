# text-summarizer-2

Here is a shorter, more professional version of the README with all emojis removed.

SimpleTextSummarizer
A Python script to generate abstractive summaries from text, .pdf, and .docx files using Hugging Face Transformers.

This project is a single script (text_summarizer.py) intended for command-line use or as a module. It has no web interface or API.

Features
Multi-Format Input: Handles raw text, .txt, .pdf, and .docx files.

Abstractive Summarization: Uses the sshleifer/distilbart-cnn-12-6 model (a fast and effective DistilBART variant) to generate fluent, new sentences.

Self-Contained: All logic is in one Python file.

Customizable: Easily change the model or summary length parameters.

Setup
1. Get the Code: Clone the repository or download text_summarizer.py.

2. Install Dependencies: Install the required libraries via pip:

Bash

pip install transformers torch PyPDF2 python-docx
transformers: For the ML model.

torch: The PyTorch backend.

PyPDF2: For reading PDF files.

python-docx: For reading DOCX files.

How to Use
The script can be run directly from the terminal.

1. Run the Script:

Bash

python text_summarizer.py
First-Time Run: The script will download the pre-trained model (approx. 400-500MB).

Output: The script will run built-in examples, summarizing a hard-coded string and a sample .txt file. It will also attempt to summarize sample_document.pdf and sample_report.docx if they are present.

2. Summarize Your Own Files:

Edit text_summarizer.py and go to the if __name__ == "__main__": section.

Change the pdf_file_path or docx_file_path variables to point to your files.

Run the script again: python text_summarizer.py

Customization
Changing the Model
Change the SUMMARIZER_MODEL variable at the top of the script to any summarization model from the Hugging Face Hub (e.g., t5-small).

Python

SUMMARIZER_MODEL = "t5-small"
Adjusting Summary Length
Pass max_length and min_length arguments to the summarize method.

Python

# Get a short summary
summary = summarizer.summarize(my_text, max_length=50, min_length=20)
