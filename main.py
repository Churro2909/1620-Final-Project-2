from bs4 import BeautifulSoup
import requests
import csv

"""
This code was designed to scrape Apartments.com for listings in a city that is inputted by the user.
It will look for the name, address, price rage, rooms, and link to the page from Apartments.com and write it to a csv file.
The user can then take the file and quickly scan and filter the results to help them in their search for a home.
"""

# We open the csv file at the beginning of the code with the "with" function to avoid issues related to closing the file.
with open('../apartments.csv', 'w', newline='') as csvfile:
    table_title = ["Title", "Address", "Price Range", "Rooms", "Link to Page"]
    content = csv.writer(csvfile)
    content.writerow(table_title)

    # Here the user is asked to input a city and state so that it can be used to get the url
    location = input("Insert a city and state (e.g. omaha ne): ")

    # There is a for loop here that replaces the end of the url for however many pages you would like the code to iterate through
    for page in range(1, 25):

        url = "https://www.apartments.com/{}/{}".format(location, page)
        headers = {
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US, en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.52',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'http://www.wikipedia.org/',
            'Connection': 'keep-alive'
        }
        # Here we set up the Beautiful Soup object to get the code from the website
        response = requests.request("GET", url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Here we get the blocks that contain all the information and throw it into a list
        try:
            cards = soup.find_all('li', class_='mortar-wrapper')
        except AttributeError:
            break

        # For every listing in the cards list we look for specific tags and extract the data from it
        for card in cards:
            try:
                title = card.find('span', class_='js-placardTitle title').text
            except AttributeError:
                title = "None"
            try:
                address = card.find('div', class_='property-address js-url').text
            except AttributeError:
                address = "None"
            try:
                price_range = card.find('p', class_='property-pricing').text
            except AttributeError:
                price_range = "None"
            try:
                rooms = card.find('p', class_='property-beds').text
            except AttributeError:
                rooms = "None"
            try:
                link = card.find('a', class_='property-link').get("href")
            except AttributeError:
                link = "None"
            apartments = [title, address, price_range, rooms, link]
            # We then write it into the "apartments.csv" file that the user can use.
            content.writerow(apartments)

    print("done")
