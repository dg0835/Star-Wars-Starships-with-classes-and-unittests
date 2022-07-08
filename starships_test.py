import unittest
import pymongo

import pytest
from starships import Scraper, DataAlteration, DataUpload

client = pymongo.MongoClient()
db = client['starwars']

class UnitTests(unittest.TestCase):

    def setUp(self) -> None:

        self.s = Scraper()
        self.da = DataAlteration()
        self.du = DataUpload()

    def test_is_starship_json_returned(self):

        info = self.s.get_api_json("https://swapi.dev/api/starships")

        actual = info["count"]
        expected = 36
        self.assertEqual(
            actual, expected,
            "Is the correct json returned?")

    def test_all_info_stored(self):

        info = self.s.get_api_json("https://swapi.dev/api/starships")
        starships = self.da.store_starships(info)

        actual = starships[35]["name"]
        expected = "V-wing"
        self.assertEqual(
            actual, expected,
            "Is the correct page returned?")

    def test_correct_pilot_id(self):

        info = self.s.get_api_json("https://swapi.dev/api/starships")
        starships = self.da.store_starships(info)
        updated_starships = self.da.replace_pilots(starships)

        actual = updated_starships[20]["pilots"]
        print(actual)

        correct_pilot = False

        if "ObjectId" in str(actual):
            correct_pilot = True

        self.assertTrue(correct_pilot)

    def test_new_data_stored_locally(self):
        info = self.s.get_api_json("https://swapi.dev/api/starships")
        starships = self.da.store_starships(info)
        updated_starships = self.da.replace_pilots(starships)
        self.du.drop_collection()
        self.du.upload_data_to_mongodb(updated_starships)


        for ship in db.starships.find({"name": "Millennium Falcon"}):
            pilots = ship["pilots"]

            print(pilots)

        valid_pilots = True

        for p in pilots:
            if "ObjectId" not in str(p):
                valid_pilots = False

        self.assertTrue(valid_pilots)




