from bs4 import BeautifulSoup
import requests
import pandas as pd

def scrape_data():

    pageNumbers = range(1,66)

    data_rows = []

    for pageNumber in pageNumbers:
        data_row = get_page_data(pageNumber)
        data_rows.extend(data_row)

    # Storing the data in a pandas DataFrame and saving it to a CSV file
    df = pd.DataFrame(data_rows)
    df.to_csv('names-locations.csv', index=False)


def get_page_data(pageNumber):
    data_rows = []
    # URL for the page to scrape
    pageURL = "https://onebite.app/reviews/dave?page=" + str(pageNumber) + "&minScore=0&maxScore=10"
    page = requests.get(pageURL)
    soup = BeautifulSoup(page.content, 'html.parser')

    locations = soup.find_all('p', class_='reviewCard__location')
    titles = soup.find_all('h2', class_='reviewCard__title') 

    # Storing the location and title in a dictionary list

    for i in range(len(locations)):
        location = locations[i].text.strip()
        title = titles[i].text.strip()
        data_rows.append({'Location': location, 'Title': title})
        #print(f"Location: {location}, Title: {title}")
        
    print(f"Page {pageNumber} processed.")

    return data_rows

def main():
    scrape_data()
    return 0


if __name__ == "__main__":
    main()
    print("Data extraction complete. CSV file created: names-locations.csv")