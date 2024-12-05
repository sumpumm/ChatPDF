import pdfplumber
from tkinter.filedialog import askopenfilename


pdf_path = askopenfilename(filetypes=[("PDF files", "*.pdf")])

with pdfplumber.open('manual.pdf') as pdf:
    number_pages=len(pdf.pages)
    print(number_pages)
    
    pages=pdf.pages
    
    text=pages[7].extract_text()
    
    
    lines = text.split('\n')
    for i in range(10):
        print(lines[i])
        