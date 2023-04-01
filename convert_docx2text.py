import os
import pypandoc
import mammoth
def convert_docx2text(src_path, dst_path):
    files = os.listdir(src_path)
    files = [f for f in files if f.endswith('.docx')]
    for file in files:
        try:
            pypandoc.convert_file(os.path.join(src_path, file), 'plain', outputfile=os.path.join(dst_path, file[:-5] + '.txt'))
        except Exception as e:
            print(e)
            
if __name__ == '__main__':
    # convert_docx2text('data/', 'data_converted/')
    

            
        
    # ele = read_txt_file('data_converted/Eletropaulo teste.txt')
    # print (ele)