from pdf2image import convert_from_path
import easyocr
import numpy as np  

# Path naar je PDF-bestand
pdf_path = "/Users/r_middelman/Documents/WebScraper_Project/Albert-heijn/Albert-heijn_Folder.pdf"

# Converteer PDF-pagina's naar afbeeldingen
images = convert_from_path(pdf_path)

# Initialize EasyOCR reader
reader = easyocr.Reader(['nl'])  # 'nl' for Dutch

# OCR uitvoeren op elke pagina
for i, image in enumerate(images):
    # Convert PIL image to numpy array
    image_np = np.array(image)
    result = reader.readtext(image_np, detail=0)
    text = "\n".join(result)
    print(f"--- Pagina {i + 1} ---")
    print(text)
    print("\n")