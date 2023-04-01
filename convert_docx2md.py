import mammoth

with open("Eletropaulo teste.docx", "rb") as docx_file:
    result = mammoth.convert_to_markdown(docx_file)

with open("sample.md", "w") as md_file:
    md_file.write(result.value)
    