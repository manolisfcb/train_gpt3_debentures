#extract_doc_info.py

from PyPDF2 import PdfReader

def extract_information(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf = PdfReader(f)
        information = pdf.metadata
        number_of_pages = len(pdf.pages)
   

        txt = f"""
        Information about {pdf_path}: 

        Author: {information.author}
        Creator: {information.creator}
        Producer: {information.producer}
        Subject: {information.subject}
        Title: {information.title}
        Number of pages: {number_of_pages}

        """
        
        for num in range(number_of_pages):

            page = pdf.pages[num]
            print(f'Page {num}')
            print(page.extract_text())
            
            if num == 20:
                break
    
    
    print(txt)
    return information

if __name__ == '__main__':
    path = 'Termo de Securitização - v. assinatura TRUE CRI 37E.pdf'
    extract_information(path)