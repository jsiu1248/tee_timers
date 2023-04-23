import requests

url = 'https://partner-api.groupon.com/deals.json?tsToken=US_AFF_0_201236_212556_0&offset=0&limit=50&filters=category:Golf'

response = requests.get(url)
data = response.json()

deals = data['deals']

if response.status_code == 200:
    results = response.json().get("deals")

    for deal in deals:
        title = deal['title']
        price = deal['price']['formattedAmount']
        value = deal['value']['formattedAmount']
        discount = deal['discount']['formattedAmount']
        
        print(f"{title}\nPrice: {price}\nValue: {value}\nDiscount: {discount}\n")

else:
    print("Request failed")