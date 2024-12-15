import requests
import re
import os

# URL of the GraphQL endpoint
url = 'https://www.jumbo.com/aanbiedingen/nu'

# Define headers (similar to those in your example)
headers = {
    'Content-Type': 'application/json',
    'Accept': '*/*',
    'Apollographql-Client-Version': 'master-v1.120.0-web',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Mobile/15E148 Safari/604.1',
    'Referer': 'https://www.jumbo.com/aanbiedingen/nu',
    'Origin': 'https://www.jumbo.com',
}

# Define the GraphQL query
payload = {
    "operationName": "GetDisplayAdsPlacement",
    "variables": {
        "input": {
            "page": 1,
            "platform": "WEB_MOBILE",
            "positions": 46,
            "fallbackPositions": 45
        }
    },
    "query": """query GetDisplayAdsPlacement($input: DisplayAdsPlacementInput!) {
        getDisplayAdsPlacement(input: $input) {
            displayAds {
                adgroupId
                auctionId
                position
                ranking
                advertiserId
                campaignId
                creative {
                    cta {
                        id
                        title
                        action
                    }
                    styling {
                        alignment {
                            textElements
                        }
                        packshotURL
                        colors {
                            adBackground
                            ctaBackground
                            cta
                            textElements
                        }
                        backgroundImage
                    }
                    headline
                    subline
                    destinationURL
                    productId
                    advertiserName
                }
            }
        }
    }"""
}

# Send the POST request to the GraphQL endpoint
response = requests.post(url, json=payload, headers=headers)
print(response.text)

response_output_path = '/Users/r_middelman/Documents/WebScraper_Project/Jumbo/response_output.txt'
with open(response_output_path, 'w') as file:
    if response.status_code == 200:
        file.write("Request successful.\n")
        file.write("Response Headers:\n")
        file.write(str(response.headers) + "\n")
        file.write("Response Body:\n")
        file.write(response.text + "\n")

