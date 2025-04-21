from bs4 import BeautifulSoup
import requests
import pandas as pd

def process_scraped_data(data: pd.DataFrame):
    '''
    Process the scraped data to extract latitude and longitude
    '''
    data = pd.read_csv('names-locations.csv')
    # Splitting City,State column into two separate columns using comma as the delimiter
    # Loading us cities data
    us_cities = pd.read_csv('uscities.csv')
    us_cities = us_cities[['city', 'state_id', 'lat', 'lng']]
    us_cities['cityName'] = us_cities['city'] + ', ' + us_cities['state_id']

    # Merging the scraped data with the US cities data to get latitude and longitude
    data = pd.merge(data, us_cities, left_on='Location', right_on='cityName', how='left')

    # Print the number of missing values in the latitude and longitude columns
    print("Missing values in latitude and longitude columns:")
    print(data['lat'].isnull().sum())
    print(data['lng'].isnull().sum())
    # Print 10 random rows with missing lat long values
    print("Random rows with missing latitude and longitude values:")
    print(data[data['lat'].isnull() | data['lng'].isnull()].sample(10)) 
    # Groupy by City and State, print the top 10 visited cities
    grouped = data.groupby(['cityName']).size().reset_index(name='Occurrences')
    grouped = grouped.sort_values(by='Occurrences', ascending=False)
    print(grouped.head(20))
    return data

def getAPIurl(Lat: float,Lon: float) -> str:
    '''
    Returns API url using lat/long search
    '''
    return("https://one-bite-api.barstoolsports.com/venue?dave=1&lat=" + str(Lat) + "&lon=" + str(Lon))

def scrape_data():

    pageNumbers = range(1,66)

    data_rows = []

    for pageNumber in pageNumbers:
        data_row = get_page_data(pageNumber)
        data_rows.extend(data_row)

    # Storing the data in a pandas DataFrame and saving it to a CSV file
    df = pd.DataFrame(data_rows)
    df.to_csv('names-locations.csv', index=False)

    return df


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
    #scrape_data()
    process_scraped_data(pd.DataFrame())
    return 0


if __name__ == "__main__":
    main()
    print("Data extraction complete. CSV file created: names-locations.csv")