import requests
import os
import json
from dotenv import load_dotenv


class Request(object):
    def __init__(self, url, file_path):
        load_dotenv('.env')
        self.tariff_url = os.getenv('TARIFF_URL')
        self.file_path = file_path
        self.url = os.path.join(self.tariff_url, url)
        self.response = requests.get(self.url)
        self.json = self.response.json()
        parsed = json.loads(self.response.text)
        self.text = json.dumps(parsed, indent=2)
        self.make_folders()

    def make_folders(self):
        if self.file_path.strip == "":
            return

        root = os.path.dirname(os.path.realpath(__file__))
        root = os.path.join(root, "..")
        root = os.path.realpath(root)
        paths = self.file_path.split("/")
        write_path = root
        for path in paths:
            write_path = os.path.join(write_path, path)
            if ".json" not in path:
                if not(os.path.isdir(write_path)):
                    os.mkdir(write_path)
            else:
                if not('"detail": "not found"' in self.text):
                    print(write_path)
                    f = open(write_path, "w+")
                    f.write(self.text)
