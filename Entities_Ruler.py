import json
with open('anotaçoes/arquivo_junto.txt', "r", encoding='utf-8') as f:
    text = f.read().split('\n\n')
    #print (text)
    
    
    
    
for segment in text:
    segment = segment.strip()
    segment = segment.replace('\n', ' ')
    segment = segment.replace('\t', ' ')
    punc = '''!()-[]{};:'“"\”,<>./?@#$%^&*_~'''
    for ele in segment:
        if ele in punc:
            segment = segment.replace(ele, "")
    
    print (segment)