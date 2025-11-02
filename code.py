
import PyPDF2
import docx
from transformers import pipeline
import os


SUMMARIZER_MODEL = "sshleifer/distilbart-cnn-12-6"

# --- File Reading Functions ---

def read_text_file(file_path):
    """Reads and returns text from a .txt file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading .txt file: {e}")
        return None

def read_pdf_file(file_path):
    """Reads and returns text from a .pdf file."""
    text = ""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page_num].extract_text() or "" # Handle potential None from extract_text
        return text
    except Exception as e:
        print(f"Error reading .pdf file: {e}")
        return None

def read_docx_file(file_path):
    """Reads and returns text from a .docx file."""
    text = ""
    try:
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        print(f"Error reading .docx file: {e}")
        return None

# --- Main Summarizer Class ---

class SimpleTextSummarizer:
    def __init__(self, model_name=SUMMARIZER_MODEL):
        """Initializes the summarizer with a specified model."""
        print(f"Loading summarization model: {model_name}...")
        try:
            self.summarizer_pipeline = pipeline("summarization", model=model_name)
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Failed to load model {model_name}. Please check your internet connection or model name. Error: {e}")
            self.summarizer_pipeline = None

    def summarize(self, text, max_length=150, min_length=50):
        """
        Summarizes the given text using the loaded ML model.

        Args:
            text (str): The input text to summarize.
            max_length (int): Maximum length of the generated summary.
            min_length (int): Minimum length of the generated summary.

        Returns:
            str: The generated summary, or None if an error occurred.
        """
        if not self.summarizer_pipeline:
            return "Summarization model not loaded. Cannot summarize."
        
        if not text or len(text.strip()) == 0:
            return "Input text is empty. Nothing to summarize."

        print(f"Summarizing text of length {len(text)} characters...")
        try:
         
            # though extremely long texts might still hit model limits.
            summary_list = self.summarizer_pipeline(
                text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False  # Set to True for more varied summaries
            )
            return summary_list[0]['summary_text']
        except Exception as e:
            print(f"Error during summarization: {e}")
            return None

# --- Example Usage ---

if __name__ == "__main__":
    # --- Step 0: Ensure libraries are installed ---
    print("Checking for required libraries. If this is the first run, it might download the model.")
    print("Please install them if you haven't: pip install transformers torch PyPDF2 python-docx")
    print("-" * 50)

    # Initialize the summarizer
    summarizer = SimpleTextSummarizer()

    if not summarizer.summarizer_pipeline:
        print("\nExiting because the summarizer model could not be loaded.")
    else:
        # --- Example 1: Summarize a direct string ---
        print("\n--- Example 1: Summarizing a direct string ---")
        long_string = """
        Artificial intelligence (AI) is intelligence demonstrated by machines, unlike the natural intelligence
        displayed by humans and animals. Leading AI textbooks define the field as the study of "intelligent agents":
        any device that perceives its environment and takes actions that maximize its chance of successfully
        achieving its goals. Colloquially, the term "artificial intelligence" is often used to describe machines
        (or computers) that mimic "cognitive" functions that humans associate with the human mind, such
        as "learning" and "problem-solving".

        AI applications include advanced web search engines (e.g., Google Search), recommendation systems
        (used by YouTube, Amazon, and Netflix), understanding human speech (such as Siri and Alexa), self-driving
        cars (e.g., Waymo), generative AI like ChatGPT, and competing at the highest level in strategic
        game systems (such as chess and Go).

        As machines become increasingly capable, tasks considered to require "intelligence" are often removed
        from the definition of AI. For example, optical character recognition is frequently excluded, having
        become a routine technology. This phenomenon is known as the AI effect.

        Artificial intelligence was founded as an academic discipline in 1956, and in the decades since has
        experienced several waves of optimism followed by disappointment and loss of funding (known as an
        "AI winter"), followed by new approaches, success, and renewed funding. AI research has received
        and continues to receive criticism for various reasons, including the potential for job displacement,
        bias in algorithms, and its potential misuse in surveillance and warfare.
        """
        summary1 = summarizer.summarize(long_string)
        print("\nOriginal Text (snippet):", long_string[:200] + "...")
        print("Summary:", summary1)
        print("-" * 50)

       
        print("\n--- Example 2: Summarizing from a .txt file ---")
        # Create a dummy .txt file for demonstration
        txt_file_path = "sample_text.txt"
        with open(txt_file_path, "w", encoding="utf-8") as f:
            f.write("The quick brown fox jumps over the lazy dog. This is a very long sentence " * 20 + " It is designed to be summarized.")
        
        txt_content = read_text_file(txt_file_path)
        if txt_content:
            summary2 = summarizer.summarize(txt_content, max_length=60, min_length=20)
            print(f"\nOriginal Text from {txt_file_path} (snippet):", txt_content[:150] + "...")
            print("Summary:", summary2)
        os.remove(txt_file_path) # Clean up dummy file
        print("-" * 50)

        # --- Example 3: Summarize from a .pdf file (Requires a dummy PDF) ---
        print("\n--- Example 3: Summarizing from a .pdf file ---")
        pdf_file_path = "sample_document.pdf"
      
        if os.path.exists(pdf_file_path):
            pdf_content = read_pdf_file(pdf_file_path)
            if pdf_content:
                summary3 = summarizer.summarize(pdf_content, max_length=200, min_length=80)
                print(f"\nOriginal Text from {pdf_file_path} (snippet):", pdf_content[:200] + "...")
                print("Summary:", summary3)
            else:
                print(f"Could not read content from {pdf_file_path}")
        else:
            print(f"Skipping PDF example: '{pdf_file_path}' not found. Please create one to test.")
        print("-" * 50)

        # --- Example 4: Summarize from a .docx file (Requires a dummy DOCX) ---
        print("\n--- Example 4: Summarizing from a .docx file ---")
        docx_file_path = "sample_report.docx"
       
        # in the same directory as this script, or change the path.
        if os.path.exists(docx_file_path):
            docx_content = read_docx_file(docx_file_path)
            if docx_content:
                summary4 = summarizer.summarize(docx_content, max_length=180, min_length=60)
                print(f"\nOriginal Text from {docx_file_path} (snippet):", docx_content[:200] + "...")
                print("Summary:", summary4)
            else:
                print(f"Could not read content from {docx_file_path}")
        else:
            print(f"Skipping DOCX example: '{docx_file_path}' not found. Please create one to test.")
        print("-" * 50)

    print("\nProject execution finished.")
