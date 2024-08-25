import requests
from waste_collection_schedule import Collection  # type: ignore[attr-defined]
from bs4 import BeautifulSoup
from datetime import datetime

TITLE = "Ikast-Brande Municipality"
DESCRIPTION = "Renomatic for Ikast-Brande Municipality"
URL = "https://skrald.ikast-brande.dk/Tomningsinfo"
INFO_COLUMN_INDEX = 0
DATE_COLUMN_INDEX = 3

TEST_CASES = {
    "TestCase1": {
        "address_id": 33441,
    },
    "TestCase2": {
        "address_id": 7326,
    },
    "TestCase3": {
        "address_id": 1970,
    },
}

ICON_MAP = {
    "RESIDUAL": "mdi:trash-can",
    "RECYCLABLE": "mdi:recycle",
}

class Source:
    def __init__(self, address_id: int):
        self._address_id = address_id

    def parse_date_with_year(self, date_string):
        current_year = datetime.now().year

        parsed_date = datetime.strptime(date_string, '%d-%m').replace(year=current_year)
        return parsed_date if parsed_date >= datetime.now() else parsed_date.replace(year=current_year + 1)

    def get_table_rows(self, soup):
        table = soup.find('div', id='table')
        table_body = table.find('tbody')
        return table_body.find_all('tr')

    def retrieve_dates_from_row(self, date_text):
        return [self.parse_date_with_year(date) for date in date_text.split(', ')]

    def fetch(self):
        query_params = {
            "adresseId": self._address_id
        }

        response = requests.get(URL, params=query_params)

        if response.status_code != 200:
            raise ValueError("Unable to read collection dates, verify address_id")
        
        soup = BeautifulSoup(response.text, 'html.parser')

        rows = self.get_table_rows(soup)
        
        if rows is None:
            return
        
        residual_waste_dates = None
        recyclable_dates = None
        
        for row in rows:
            info_text = row.find_all('td')[INFO_COLUMN_INDEX].text.strip()
            date_text = row.find_all('td')[DATE_COLUMN_INDEX].text.strip()

            if date_text == '':
                continue

            if "renovation" in info_text.lower() and not residual_waste_dates:
                residual_waste_dates = self.retrieve_dates_from_row(date_text)                
            elif "genbrugsbeholder" in info_text.lower() and not recyclable_dates:
                recyclable_dates = self.retrieve_dates_from_row(date_text)
            
            if residual_waste_dates and recyclable_dates:
                break
                
        entries = []
                
        for date in residual_waste_dates:                   
            entries.append(
                Collection(
                    date=date,
                    t="Residual",
                    icon=ICON_MAP.get("RESIDUAL"),
                )
            )
        
        for date in recyclable_dates:                   
            entries.append(
                Collection(
                    date=date,
                    t="Recyclable",
                    icon=ICON_MAP.get("RECYCLABLE"),
                )
            )
        
        return entries