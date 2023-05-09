import cv2
import pytesseract
from pytesseract import Output
import json
import os
import time
import re

directory_imgs = "image_deteccao/"
paths = [os.path.join(directory_imgs, f) for f in os.listdir(directory_imgs)]
print(paths)

pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"

def process_image(img, keywords, regex_pattern=None, padding=10, height_scale_factor=1, width_scale_factor=1):
    result = pytesseract.image_to_data(img, lang="por", output_type=Output.DICT)

    lines = {}
    for i in range(0, len(result["text"])):
        text = result["text"][i]
        if any(keyword in text for keyword in keywords) or (regex_pattern and re.search(regex_pattern, text)):
            y = result["top"][i]
            x = result["left"][i]
            w = result["width"][i]
            h = result["height"][i]

            if y not in lines:
                lines[y] = {"x_min": x, "y_min": y, "x_max": x + w, "y_max": y + h}
            else:
                lines[y]["x_min"] = min(lines[y]["x_min"], x)
                lines[y]["x_max"] = max(lines[y]["x_max"], x + w)
                lines[y]["y_max"] = max(lines[y]["y_max"], y + h)

    for line in lines.values():
        cv2.rectangle(
            img,
            (line["x_min"] - padding * 2, line["y_min"] - padding * 2),
            (line["x_max"] + int(padding * 350 * width_scale_factor), line["y_max"] + int(padding * 20 * height_scale_factor)),
            (0, 0, 255),
            10,
        )

    return img

for filename in os.listdir(directory_imgs):
    if filename.endswith(".tiff"):
        image_path = os.path.join(directory_imgs, filename)
        img = cv2.imread(image_path)

if img is None:
    print("Erro ao ler a imagem:", image_path)
else:
  
    keywords1 = ["CONTRATO"] #KEYWORDS
    img_processed1 = process_image(img, keywords1, height_scale_factor=0.05, width_scale_factor=0.20)

    output_image_path = "image_deteccao/numero_contrato_encontrado.tiff"
    cv2.imwrite(output_image_path, img_processed1)





# Diretorio para detecção de imagens Tiffs
output_directory = (
    "image_deteccao/"
)
os.makedirs(output_directory, exist_ok=True)
# Termo padrão e intermediario de busca de texto e pixels
term_search = "CONTRATO Nº"  # Parametro para detecção de texto

for image in paths:
    if not image.endswith(".tif") and not image.endswith(".tiff"):
        continue

    # Processa a imagem em busca da assinatura da imagem
    try:
        img = cv2.imread(image)
        file_img = os.path.split(image)[-1]
        print("==================\n" + str(file_img))
        time.sleep(0.10)

        # Processa a imagem usando a função process_image() e keywords = [term_search]
        img_processed = process_image(img, [term_search])

        # Extrai texto da imagem usando a função pytesseract.image_to_string()
        text = pytesseract.image_to_string(img_processed, lang="por")

        # Verifica se o termo de busca aparece no texto extraído
        if term_search in text:
            file_ext = os.path.splitext(file_img)[1]
            new_file_name = "numero_contrato_copia" + file_ext
            new_image_path = os.path.join(output_directory, new_file_name)

            # Salva a imagem com o termo de busca em uma nova pasta
            cv2.imwrite(new_image_path, img)
            print(f"Imagem copiada e salva em: {new_image_path}")

            # Salva a imagem com as bounding boxes em uma nova pasta
            boxes_data = pytesseract.image_to_data(
                img_processed, lang="por", output_type=Output.DICT
            )
            # Apos Boundbox com  keywords faz o Regex para extração exata do paragrafo
            numero_contrato = re.search(r"CONTRATO Nº (\d{11})", text)
            # Adiciona o resultado encontrado no resultado JSON
            resultado = {}
            resultado["numero_contrato"] = {
                
                "Numero_Contrato": numero_contrato.group(1),
                "Recebido": "Sim",
                "Legivel": "Sim",               
                "url_image_detectada_pela_IA": os.path.join(
                    directory_imgs, "numero_contrato_encontrado.tiff"
                ),
            }
            resultado["mensagem"] = "Número do contrato foi adicionado ao relatório"
            print(json.dumps(resultado, indent=4))
            break
        else:
            # Adiciona o resultado não encontrado no resultado JSON
            resultado = {}
            numero_nao_legivel = re.search(r"\d+", text).group()
            resultado["numero_contrato"] = {
            "Numero_Contrato": "Dados não detectados",
            "Recebido": "Não",
            "Legivel": "Não",
  }
            resultado["mensagem"] = "Número do contrato não foi detectado pela plataforma"
            print(json.dumps(resultado, indent=4))
        print("\n")
    except Exception as e:
        print(f"Erro ao processar a imagem {image}: {str(e)}")