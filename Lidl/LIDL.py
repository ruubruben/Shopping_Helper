import requests
import xml.etree.ElementTree as ET

# Lidl API URL
lidl_url = "https://mobile.lidl.de/Mobile-Server/service/95/containerService/NL/campaign/nl/a10008785/0/50?warehouseKey=6"

# Function to fetch data from a URL with optional headers and parameters
def fetch_data(url, headers=None, params=None):
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        print(f"Response status code: {response.status_code}")  # Debug: Print status code
        print(f"Response content: {response.text}")  # Debug: Print response content
        return response.text  # Return raw text if the request was successful
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

# Function to parse XML data
def parse_xml(data):
    try:
        root = ET.fromstring(data)
        return root
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return None

# Fetch data from Lidl API
lidl_data = fetch_data(lidl_url)

# Parse the XML data and extract product details
if lidl_data:
    root = parse_xml(lidl_data)
    if root is not None:
        # Extract product details
        products = []
        for product in root.findall(".//Product"):
            title = product.find(".//title").text if product.find(".//title") is not None else "No title"
            new_price = product.find(".//price").text if product.find(".//price") is not None else "No new price"
            old_price = product.find(".//oldPrice").text if product.find(".//oldPrice") is not None else "No old price"
            discount_text = product.find(".//discountText").text if product.find(".//discountText") is not None else "No discount text"
            
            product_details = {
                "title": title,
                "new_price": new_price,
                "old_price": old_price,
                "discount_text": discount_text
            }
            products.append(product_details)

        # Output the list of product details
        if products:
            with open("LIDL_Products.txt", "w") as file:
                for product in products:
                    file.write(f"Title: {product['title']}\n")
                    file.write(f"New Price: {product['new_price']}\n")
                    file.write(f"Old Price: {product['old_price']}\n")
                    file.write(f"Discount: {product['discount_text']}\n")
                    file.write("-" * 50 + "\n")
            print("Products saved to LIDL_Products.txt")
        else:
            print("No products found.")
    else:
        print("Failed to parse XML data.")
else:
    print("Failed to fetch Lidl data")