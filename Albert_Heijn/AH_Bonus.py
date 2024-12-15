import requests
import re
import os


# URL for the initial GET request
url = "https://ah.nl/producten"

url_template = "https://www.ah.nl/producten/{category}?kenmerk=bonus"

# Headers for the request
headers = {
    "X-Clientname": "ipad",
    #"Authorization": "Bearer 109525384_ac7-44e1-a132-f28db7fc1fe8",
    "X-Application": "AHWEBSHOP",
    "X-Correlation-Id": "UNKNOWN-05C715BA-7AB3-4D50-BB82-A173177E9DBF",
    "X-Fraud-Detection-Installation-Id": "3B35783A-4BFE-477F-98F9-A78DEEB24B70",
    "X-Accept-Language": "nl-NL",
    "X-Clientversion": "9.2.1",
    "Accept": "*/*",
    "Accept-Language": "en-US;q=1.0, nl-NL;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "X-Shopping-Intent": "Store",
    "User-Agent": "Appie/9.2.1 (iPhone15,2; iPhone; CPU iPhone OS 18_2 like Mac OS X)",
}

# Cookies for the request
cookies = {
    "FPID": "FPID2.2.FjzCpimaZAdb0evkBlTmDxrfZKpVV9WOrOESb%2BYFieY%3D.1699835211",
    "_ga_MHW09B918N": "GS1.1.1734197818.32.1.1734197832.0.0.1524016366",
    "_ga": "GA1.1.433621946.1699835211",
    # Add other cookies if necessary
}
response = requests.get(url, headers=headers)

# Save the response to a text file
response_output_path = '/Users/r_middelman/Documents/WebScraper_Project/Albert_Heijn/response_output.txt'
with open(response_output_path, 'w') as file:
    if response.status_code == 200:
        file.write("Request successful.\n")
        file.write("Response Headers:\n")
        file.write(str(response.headers) + "\n")
        file.write("Response Body:\n")
        file.write(response.text + "\n")

        # If Bearer token is in the response body, extract it (example)
        if "Bearer" in response.text:
            # Replace this with actual parsing logic based on response structure
            bearer_token = response.text.split("Bearer ")[1].split('"')[0]
            file.write("Extracted Bearer Token: " + bearer_token + "\n")
        else:
            file.write("Bearer token not found in response.\n")
    else:
        file.write(f"Failed to send request. Status code: {response.status_code}\n")

# Filter the response output for titles and save to another text file
categories_output_path = '/Users/r_middelman/Documents/WebScraper_Project/Albert_Heijn/categories.txt'
pattern = re.compile(r'class="taxonomy-card_imageLink__4b6bk" title="([^"]+)"')

with open(response_output_path, 'r') as infile, open(categories_output_path, 'w') as outfile:
    for line in infile:
        matches = pattern.findall(line)
        for match in matches:
            print(f"Found category: {match}")
            outfile.write(match + '\n')

categories_file_path = '/Users/r_middelman/Documents/WebScraper_Project/Albert_Heijn/categories.txt'
with open(categories_file_path, 'r') as file:
    categories = [line.strip().replace(' ', '-').replace(',', '').lower() for line in file.readlines()]
    print("Categories:", categories)

# Open a single file to save all responses
response_output_path = '/Users/r_middelman/Documents/WebScraper_Project/Albert_Heijn/all_responses.txt'
with open(response_output_path, 'w') as file:
    # Loop through each category and make a request to the new URL
    for category in categories:
        url = url_template.format(category=category)
        response = requests.get(url, headers=headers, cookies=cookies)

        # Write the response to the file
        file.write(f"Category: {category}\n")
        if response.status_code == 200:
            file.write("Request successful.\n")
            file.write("Response Headers:\n")
            file.write(str(response.headers) + "\n")
            file.write("Response Body:\n")
            file.write(response.text + "\n")

        else:            
            file.write(f"Failed to send request. Status code: {response.status_code}\n")
        file.write("\n" + "="*80 + "\n\n")  # Separator between responses


# Input and output file paths
input_file_path = '/Users/r_middelman/Documents/WebScraper_Project/Albert_Heijn/all_responses.txt'
output_file_path = '/Users/r_middelman/Documents/WebScraper_Project/Albert_Heijn/products.txt'

input_file_path = response_output_path
output_file_path = os.path.join('/Users/r_middelman/Documents/WebScraper_Project/Albert_Heijn', 'products.txt')
product_pattern = re.compile(r'"product-title-line-clamp">([^<]+)')
path_pattern = re.compile(r'/producten/product/[^"]+')

# Open the input file and read lines
with open(input_file_path, 'r') as infile:
    lines = infile.readlines()

# Open the output file to write the extracted product names and prices
with open(output_file_path, 'w') as outfile:
    path_index = 0
    path_matches = []
    for line in lines:
        path_matches.extend(path_pattern.findall(line))
    
    for line in lines:
        product_matches = product_pattern.findall(line)
        for product in product_matches:
            if path_index < len(path_matches):
                path = path_matches[path_index]
                outfile.write(f"{product.strip()} - https://www.ah.nl{path.strip()}\n")
                path_index += 2  # Skip every second path
            else:
                outfile.write(f"{product.strip()} - No path found\n")
# for filename in os.listdir('/Users/r_middelman/Documents/WebScraper_Project/Albert_Heijn'):
#     if filename.endswith('.txt') and filename != 'products.txt':
#         os.remove(os.path.join('/Users/r_middelman/Documents/WebScraper_Project/Albert_Heijn', filename))