import pdfplumber

pdf_path = "/home/geoff/dev/portfolio/unstructured_pdf_to_excel_converter/PDF_TO_EXTRACT.pdf"

with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        print(f"\n--- Page {i+1} ---")
        text = page.extract_text()
        print(text[:2000])  # print just the first 2000 characters to avoid overflow


