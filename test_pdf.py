from langchain_community.document_loaders import PyPDFLoader
import tempfile
import os


def test_pdf_processing(pdf_content, filename):
    """Test PDF processing without MongoDB"""
    tmp_file_path = None
    try:
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(pdf_content)
            tmp_file_path = tmp_file.name

        # Try to load PDF
        loader = PyPDFLoader(tmp_file_path)
        documents = loader.load()

        print(f"✅ Successfully loaded PDF: {filename}")
        print(f"📄 Number of pages: {len(documents)}")

        total_text = 0
        for i, doc in enumerate(documents):
            text_length = len(doc.page_content)
            total_text += text_length
            print(f"Page {i + 1}: {text_length} characters")

        print(f"📊 Total text: {total_text} characters")

        if total_text == 0:
            print("❌ Warning: No text extracted from PDF")
            return False
        else:
            return True

    except Exception as e:
        print(f"❌ PDF processing failed: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False
    finally:
        if tmp_file_path and os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)


# Test with a sample PDF or your actual PDF
if __name__ == "__main__":
    print("Testing PDF processing...")

    # You can test with your actual PDF file
    test_file_path = "test.pdf"  # Change this to your PDF file path

    if os.path.exists(test_file_path):
        with open(test_file_path, "rb") as f:
            pdf_content = f.read()
        test_pdf_processing(pdf_content, test_file_path)
    else:
        print("❌ Test PDF file not found. Please create a test.pdf file or modify the path.")