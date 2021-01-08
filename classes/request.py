import requests
import os, sys
import json
from dotenv import load_dotenv


class Request(object):
    def __init__(self, url, file_path, scope, as_of):
        self.scope = scope
        self.get_environment_variables()
        self.file_path = file_path
        self.file_path = self.file_path.replace("[scope]", self.scope)
        self.tariff_url = self.tariff_url.replace("[scope]", self.scope)
        self.url = os.path.join(self.tariff_url, url)
        if as_of != "":
            self.url += "?as_of=" + as_of

        self.response = requests.get(self.url)
        self.status_code = self.response.status_code
        if str(self.status_code) != "200":
            self.log()
        self.json = self.response.json()
        parsed = json.loads(self.response.text)
        self.text = json.dumps(parsed, indent=2)
        self.make_folders()

    def log(self):
        f = open("log/log.txt", "a")
        f.write(self.url + "," + str(self.status_code) + "\n")
        f.close()

    def get_environment_variables(self):
        load_dotenv('.env')
        self.TARIFF_URL_PRODUCTION_V2 = os.getenv('TARIFF_URL_PRODUCTION_V2')
        self.TARIFF_URL_PRODUCTION_V1 = os.getenv('TARIFF_URL_PRODUCTION_V1')
        self.TARIFF_URL_STAGING_V2 = os.getenv('TARIFF_URL_STAGING_V2')
        self.TARIFF_URL_STAGING_V1 = os.getenv('TARIFF_URL_STAGING_V1')
        self.TARIFF_URL_DEV_V2 = os.getenv('TARIFF_URL_DEV_V2')
        self.TARIFF_URL_DEV_V1 = os.getenv('TARIFF_URL_DEV_V1')
        self.tariff_url = os.getenv('TARIFF_URL')

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
                    print(self.url, write_path)
                    f = open(write_path, "w+")
                    f.write(self.text)
