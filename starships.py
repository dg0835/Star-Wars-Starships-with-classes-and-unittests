import requests
from pprint import pprint
import pymongo

client = pymongo.MongoClient()
db = client['starwars']

class Scraper:

    def __init__(self):
        self.url = "https://swapi.dev/api/starships"

    def get_api_json(self, next_page: str):
        # Get information from the API in the URL in json format

        response = requests.get(next_page)
        return response.json()

    def go_to_next_page(self, next_page: str):

        # Checks if a next page exists. If so, return the data in json format. If not, throw an exception

        try:
            data = self.get_api_json(next_page)
            return data

        except requests.exceptions.MissingSchema:
            print("There is no valid next page. the program will now stop scraping.")
            return False






class DataAlteration:

    def __init__(self):
        print("Now altering data")

    def store_starships(self, data: list):

        # Stores dictionaries (containing info about starships) into one list.

        current_data = data
        starships = []

        while True:

            next_page = current_data["next"]
            starship_dicts = current_data["results"]

            for starship in starship_dicts:
                starships.append(starship)

            current_data = scraper.go_to_next_page(next_page)

            if not current_data:
                break

        return starships


    def find_pilot_id(self, name: str):

        # Using the pilot's name, finds the pilot's ID from the local MongoDB star wars characters database.

        print(f"Finding {name} ID")
        pilot = db.characters.find({"name": name})

        for p in pilot:
            print(p["_id"])
            return p["_id"]


    def check_for_pilots(self, pilots: list):

        # Checks if the starship has any pilots

        if len(pilots) == 0:
            return False
        return True


    def replace_pilots(self, starships: list):

        # For each starship, replaces urls in the list of pilots with the pilot IDs.

        for ship in starships:
            pilots = ship["pilots"]
            are_there_pilots = self.check_for_pilots(pilots)

            if are_there_pilots:
                new_pilot_list = []

                for p in pilots:

                    p_info = scraper.get_api_json(p)
                    p_name = p_info["name"]
                    p_id = self.find_pilot_id(p_name)

                    new_pilot_list.append(p_id)

                ship["pilots"] = new_pilot_list

        return starships

class DataUpload:

    def __init__(self):
        print("Program will now upload data")

    def upload_data_to_mongodb(self, data):

        # Upload all the starship data to the local MangoDB Database

        collection = db["starships"]

        for d in data:

            inserted = collection.insert_one(d)


    def drop_collection(self):

        # Drops the starships collection

        collection = db["starships"]

        collection.drop()

scraper = Scraper()
da = DataAlteration()
du = DataUpload()

starship_api_info = scraper.get_api_json(scraper.url)  # Pass in the url of the page that we wish to scrape from

all_starships = da.store_starships(starship_api_info)  # Create a list containing all starships and their metadata

data_to_insert = da.replace_pilots(all_starships)  # Replace pilots with their IDs

du.drop_collection()
du.upload_data_to_mongodb(data_to_insert)

print("Done!")






