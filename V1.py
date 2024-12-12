import os
import re
import requests
from bs4 import BeautifulSoup
from PIL import Image

# Map- en bestandsinstellingen
base_folder_url = "https://www.folderz.nl/winkels"
output_base_path = "/Users/r_middelman/Documents/WebScraper_Project/"


# Functie om de nieuwste folder-ID op te halen
def get_latest_folder_id(store_name):
    store_url = f"{base_folder_url}/{store_name}/folders-aanbiedingen"
    response = requests.get(store_url)
    if response.status_code != 200:
        print(
            f"Fout bij het laden van de pagina voor {store_name}: {response.status_code}"
        )
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    og_image_meta = soup.find("meta", property="og:image")
    if og_image_meta:
        og_image_url = og_image_meta["content"]
        match = re.search(r"/flyers/(\d+)/", og_image_url)
        if match:
            return match.group(1)
    print(f"Geen folder-ID gevonden voor {store_name}.")
    return None


# Functie om de afbeeldingen van de folder te downloaden
def download_folder_images(store_name, folder_id):
    if not folder_id:
        print(f"Geen folder-ID opgegeven voor {store_name}. Stop met downloaden.")
        return

    folder_path = os.path.join(output_base_path, store_name.capitalize())
    os.makedirs(folder_path, exist_ok=True)

    base_url = f"https://img.offers-cdn.net/assets/uploads/flyers/{folder_id}/largeWebP/{store_name}-"
    page_number = 1
    while True:
        image_url = f"{base_url}{page_number}-1.webp"
        output_path = os.path.join(folder_path, f"page_{page_number}.webp")

        print(f"Probeer pagina {page_number} te downloaden: {image_url}")
        response = requests.get(image_url)

        if (
            response.status_code != 200
            or b"<Code>AccessDenied</Code>" in response.content
        ):
            print(
                f"Geen verdere pagina's gevonden of toegang geweigerd voor {store_name}. Laatste statuscode: {response.status_code}"
            )
            break

        with open(output_path, "wb") as file:
            file.write(response.content)
        print(f"Pagina {page_number} gedownload naar {output_path}")

        page_number += 1


# Functie om afbeeldingen te converteren naar JPEG en een PDF te maken
def convert_webp_to_jpg_and_create_pdf(store_name):
    folder_path = os.path.join(output_base_path, store_name.capitalize())
    output_pdf_path = os.path.join(folder_path, f"{store_name.capitalize()}_Folder.pdf")

    image_list = []
    jpg_files = []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".webp"):
            webp_path = os.path.join(folder_path, filename)
            jpg_path = os.path.splitext(webp_path)[0] + ".jpg"

            try:
                with Image.open(webp_path) as img:
                    rgb_img = img.convert("RGB")
                    rgb_img.save(jpg_path, "JPEG")
                    print(
                        f"Afbeelding omgezet: {filename} naar {os.path.basename(jpg_path)}"
                    )
                    image_list.append(rgb_img)
                    jpg_files.append(jpg_path)

                os.remove(webp_path)
                print(f"Origineel bestand verwijderd: {filename}")

            except Exception as e:
                print(f"Fout bij het omzetten van {filename}: {e}")

    if image_list:
        image_list[0].save(output_pdf_path, save_all=True, append_images=image_list[1:])
        print(f"PDF succesvol gemaakt voor {store_name}: {output_pdf_path}")

        # for jpg_file_path in jpg_files:
        #     if os.path.exists(jpg_file_path):
        #         os.remove(jpg_file_path)
        #         print(f"Converteerd .jpg bestand verwijderd: {jpg_file_path}")
    else:
        print(f"Geen afbeeldingen om toe te voegen aan de PDF voor {store_name}.")


# Hoofdscript
if __name__ == "__main__":
    stores = [
        "albert-heijn",
        "lidl",
        "jumbo",
        "kruidvat",
    ]  # Voeg hier meer winkels toe, zoals 'jumbo', 'aldi', etc.

    for store in stores:
        print(f"\nVerwerken van winkel: {store.capitalize()}")
        folder_id = get_latest_folder_id(store)
        if folder_id:
            print(f"Nieuwste folder-ID gevonden voor {store.capitalize()}: {folder_id}")
            download_folder_images(store, folder_id)
            convert_webp_to_jpg_and_create_pdf(store)
        else:
            print(f"Kan de nieuwste folder-ID niet vinden voor {store.capitalize()}.")
