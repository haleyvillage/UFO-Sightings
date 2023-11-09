NUFORC_DATA_URL = "https://nuforc.org/sighting/?id="

import requests
from bs4 import BeautifulSoup
import pprint
import sqlite3
import time

con = sqlite3.connect("ufo_database")


# create table ufo_sightings ( Characteristics text, Duration text, Location text, Location_Details text, No_Of_Observers text, Occurred text, Posted text , Reported text, Shape text, comments_and_content text);

def insert_event(Characteristics, Duration, Location, Location_Details, No_of_Observers, Occurred, Posted, Reported,
                 Shape, comments_and_content):
    cur = con.cursor()
    cur.execute("insert into ufo_sightings values( ? , ? , ? , ? , ? , ? , ? , ? , ? , ?)",
                (Characteristics, Duration, Location, Location_Details, No_of_Observers, Occurred, Posted, Reported,
                 Shape, comments_and_content))
    con.commit()


def get_soup_for_page(url):
    print(url)
    page = requests.get(url)
    return BeautifulSoup(page.text, 'html.parser')


def scrape_sighting_report(nuforc_id):
    soup = get_soup_for_page(NUFORC_DATA_URL + nuforc_id)

    primary = soup.find("div", {"id": "primary"})
    data = {}
    strip_from = ""
    for b in primary.find_all('b'):
        data[b.text.strip().replace(':', '')] = b.next_sibling.text.strip()
        strip_from = b.next_sibling.text.strip()

    comments_and_content = str(primary)
    comments_and_content = comments_and_content[comments_and_content.find(strip_from):]

    data['comments_and_content'] = comments_and_content

    # simple test to see if it is a valid sighiting id
    if data['Reported'] == 'Pacific':
        return

    pprint.pprint(data)
    insert_event(data['Characteristics'] if 'Characteristics' in data else "",
                 data['Duration'] if 'Duration' in data else "",
                 data['Location'] if 'Location' in data else "",
                 data['Location details'] if 'Location details' in data else "",
                 data['No of observers'] if 'No of observers' in data else "",
                 data['Occurred'] if 'Occurred' in data else "",
                 data['Posted'] if 'Posted' in data else "",
                 data['Reported'] if 'Reported' in data else "",
                 data['Shape'] if 'Shape' in data else "",
                 data['comments_and_content'] if 'comments_and_content' in data else ""
                 );


if __name__ == '__main__':
    # Get the page
    # scrape_sighting_report('178031')
    # scrape_sighting_report('1')
    for i in range(111, 300000):
        scrape_sighting_report(str(i))
        time.sleep(1)