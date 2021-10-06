from bs4 import BeautifulSoup
import requests
import csv

# Create a list to hold all of the records and their information
all_items = []
all_items_sorted = []
fields = ['Artist', 'Title', 'Sale Price', 'Original Price', 'Description']

# Opening the html file for home page of Turntable Lab
for i in range(1, 20):
    url = requests.get('https://www.turntablelab.com/collections/vinyl-cds-date?_=pf&page={}'.format(i)).text
    soup = BeautifulSoup(url, 'lxml')

    # Get all of the product blocks for the records
    product_blocks = soup.findAll('div', class_='product-block')

    # Iterates through all of the product blocks. If there is a block denoting that the item is on sale,
    # It will save the description, artist, title, sale price, and regular price of the record.
    for product in product_blocks:
        if product.find('div', class_='price ftc on-sale'):
            artist = product.find('div', class_='collection-artist')
            title = product.find('div', class_='collection-title')
            price = product.find('div', class_='price ftc on-sale')
            description = product.find('div', class_='prod-desc')

            # Divides the prices category into the sale price and the original price of the record.
            # Removes the $ in each so that the two values can be compared
            sale_price = price.find('span', class_='money')
            regular_price = price.findNext('span', class_='category-compareprice')
            sale_price = sale_price.text.replace('$', '')
            regular_price = regular_price.text.replace('$', '')

            # Fixes formatting of the descriptions by removing all non-alphanumeric characters from the string
            desc = str(description.text).strip()

            # Add the new item to the dictionary
            all_items.append([artist.text, title.text, sale_price, regular_price, desc])

            # Write the list to a csv file
            with open('records.csv', 'w') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(fields)
                csvwriter.writerows(all_items)

