import requests
import json
import xml.etree.ElementTree as ET

# The URL to make the GET request to
url = "https://mobile.lidl.de/Mobile-Server/service/95/containerService/NL/campaign/nl/a10008785/0/50?warehouseKey=6"

# Send a GET request to the API
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    print("Request successful!")
    content_type = response.headers.get('Content-Type')

    if 'application/json' in content_type:
        try:
            data = response.json()  # Parse the JSON response

            # Save the JSON response to a text file
            with open("response_data.txt", "w") as file:
                json.dump(data, file, indent=4)
            print("JSON response saved to response_data.txt")

            # Read the JSON data from the text file
            with open("response_data.txt", "r") as file:
                data = json.load(file)

            # Create an empty list to store the items with new prices
            sale_items = []

            # Loop through the "ContainerItems" to get the product details
            for item in data.get("ContainerItems", []):
                if "Product" in item:
                    product = item["Product"]
                    new_price = product.get("price")
                    old_price = product.get("oldPrice")
                    title = product.get("productLanguageSet", {}).get("ProductLanguageSet", {}).get("title", "No Title")

                    # Check if the price is on sale (new price is lower than old price)
                    if new_price and old_price and new_price < old_price:
                        sale_item = {
                            "title": title,
                            "new_price": new_price,
                            "old_price": old_price,
                            "discount_percentage": product.get("basicprice", "No discount info")
                        }
                        sale_items.append(sale_item)

            # Output the list of sale items
            if sale_items:
                with open("sale_items.txt", "w") as file:
                    for item in sale_items:
                        file.write(f"Title: {item['title']}\n")
                        file.write(f"New Price: {item['new_price']}\n")
                        file.write(f"Old Price: {item['old_price']}\n")
                        file.write(f"Discount: {item['discount_percentage']}\n")
                        file.write("-" * 50 + "\n")
                print("Sale items saved to sale_items.txt")
            else:
                print("No sale items found.")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            print("Response content:", response.content)
    elif 'application/xml' in content_type or 'text/xml' in content_type:
        try:
            root = ET.fromstring(response.content)  # Parse the XML response

            # Save the XML response to a text file
            with open("response_data.xml", "wb") as file:
                file.write(response.content)
            print("XML response saved to response_data.xml")

            # Create an empty list to store the product details
            products = []

            # Loop through the XML to get the product details
            for product in root.findall(".//Product"):
                title = product.findtext(".//title", "No Title")
                new_price = product.findtext(".//price", "No Price")
                old_price = product.findtext(".//oldPrice", "No Old Price")
                discount_text = product.findtext(".//discountText", "No Discount")

                product_details = {
                    "title": title,
                    "new_price": new_price,
                    "old_price": old_price,
                    "discount_text": discount_text
                }
                products.append(product_details)

            # Output the list of product details
            if products:
                with open("products.txt", "w") as file:
                    for product in products:
                        file.write(f"Title: {product['title']}\n")
                        file.write(f"New Price: {product['new_price']}\n")
                        file.write(f"Old Price: {product['old_price']}\n")
                        file.write(f"Discount: {product['discount_text']}\n")
                        file.write("-" * 50 + "\n")
                print("Products saved to products.txt")
            else:
                print("No products found.")
        except ET.ParseError as e:
            print(f"Error parsing XML: {e}")
            print("Response content:", response.content)
    else:
        print(f"Unexpected content type: {content_type}")
        print("Response content:", response.content)
else:
    print(f"Request failed with status code {response.status_code}")