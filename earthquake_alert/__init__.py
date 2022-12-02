from typing import List
import requests
from bs4 import BeautifulSoup

class Earthquake_Alert:
    def __init__(self):
        self.description = 'To get the latest EarthQuake information in Indonesia'
        self.result = None
    def data_extraction(self):
        try:
            content = requests.get('https://warning.bmkg.go.id') #scrape from bmkg website
        except Exception:
            return None

        if content.status_code == 200: # Check if website status OK/200
            soup = BeautifulSoup(content.text, 'html.parser')
            result = soup.find('h5', {'class': 'center'}) #get information location
            result2 = soup.find('h5', {'class': 'center'}) #get information location
            result = result.text.split(', ') #devide information into date and time
            date_eq = result[0]
            time_eq = result[1]

            result = soup.find('ul', {'class': 'infolindu'}) #get information from infolindu
            result2 = soup.find('div', {'class': 'infoext'}) #get information from infoext
            result = result.findChildren('li') # search html li
            result2 = result2.findChildren('p') #search html p

            # describe variable
            i = 0
            x = 0
            magnitudo_eq = None
            magnitudo_eq2 = None
            ls = None
            bt = None
            location_place_eq = None
            location_eq = None
            depth_eq = None
            impacted_area = None

            # fill variable with with content of website
            for res in result:
                if i == 0:
                    magnitudo_eq = res.text.split('M')
                    magnitudo_eq2 = magnitudo_eq[0]
                elif i == 1:
                    depth_eq = res.text.split('K')
                elif i == 2:
                    location_eq = res.text
                i = i + 1

            # fill variable with with content of website
            for res in result2:
                if x == 0:
                    location_place_eq = res.text.split('Gempa')
                elif x == 1:
                    impacted_area = res.text.split('Arahan')
                x = x + 1

            # save result in variable
            scrape_result = dict()
            scrape_result['date_eq'] = date_eq  # Date of earth quake
            scrape_result['time_eq'] = time_eq  # Time of earth quake
            scrape_result['magnitudo_eq'] = magnitudo_eq2  # Magnitudo of earth quake
            scrape_result['location_eq'] = location_eq
            scrape_result['depth_eq'] = depth_eq[0]  # Depth of earth quake
            scrape_result['location_place_eq'] = location_place_eq[1]
            scrape_result['impacted_area'] = impacted_area[0]
            # scrape_result
            self.result = scrape_result
        else:
            return None

    # this section used to display information
    def show_data(self):
        if self.result is None:
            print("Can not find earth quake data, plese check target url")
            return

        print('Latest Earth Quake In Indonesia')
        print(f"Date : {self.result['date_eq']}")
        print(f"Time : {self.result['time_eq']}")
        print(f"Magnitudo : {self.result['magnitudo_eq']}")
        print(f"Coordinate : {self.result['location_eq']}")
        print(f"Depth : {self.result['depth_eq']}")
        print(f"Location : {self.result['location_place_eq']}")
        print(f"Impacted Area : {self.result['impacted_area']}")

    def run(self):
        self.data_extraction()
        self.show_data()

if __name__ == '__main__':
    earthquake_in_country = Earthquake_Alert()
    print('Deskripsi Package', earthquake_in_country.description)
    earthquake_in_country.run()
    #earthquake_in_country.data_extraction()
    #earthquake_in_country.show_data()
