from joblib import load
model = load('classificador_estrutura.model')
import docx
import pandas as pd
import os
import unicodedata
def para_text_extract(files):

    '''
        Extrai docs, parágrafos docx e textos separados em parágrafos docx e '\n'
    '''

    docs = [docx.Document(doc) for doc in files]
    texts = [accept_track_changes_all(doc) for doc in docs]



    return docs, texts

def get_text_dir(folder):
    '''
        Recebe o caminho de um diretório e retorna uma lista com os caminhos dos arquivos de extensão .docx ordenados
    '''

    only_docx_path = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith('.docx')]
    only_docx_path.sort()
    return only_docx_path

def accept_track_changes(p):
    
    try:
        from xml.etree.cElementTree import XML
    except ImportError:
        from xml.etree.ElementTree import XML


    WORD_NAMESPACE = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    TEXT = WORD_NAMESPACE + "t"


    
    """Return text of a paragraph after accepting all changes"""
    xml = p._p.xml
    if "w:del" in xml or "w:ins" in xml:
        tree = XML(xml)
        runs = (node.text for node in tree.getiterator(TEXT) if node.text)
        return "".join(runs)
    else:
        return p.text
def accept_track_changes_all(docx):
    text_list = []
    for p in docx.paragraphs:
        text_list.extend(accept_track_changes(p).replace('”',"'").replace("“","'").replace("”","'").replace("“","'").replace("\"","'").split('\n'))
    return text_list


files_dir = get_text_dir('data')
_,documentos = para_text_extract(files_dir)



for texto in documentos:
    estrutura = model.predict(texto)
    df = pd.DataFrame({'texto':texto, 'estrutura':estrutura})
    #Criar um loop para salvar cada clausula em um arquivo txt7
    flag = False
    for i in range(len(df)):
        if df['estrutura'][i] == 'clausula':
            flag = True
            nome_clausula = unicodedata.normalize('NFKD',df['texto'][i].strip().lower()).encode('ASCII', 'ignore').decode('ASCII')
            f = open(f"data_split_by_clausese/{nome_clausula}.txt", "a+")
            f.write(df['texto'][i] + "\n")
        
        if df['estrutura'][i] != 'clausula' and flag == True:
            f.write(df['texto'][i] + "\n")
        else:
            pass



# #criar um txt com o texto do docx
# for i in texto:
#     f = open("data_split_by_clausese/Eletropaulo teste1.txt", "a+")
#     f.write(i + "\n")

#f.close()

