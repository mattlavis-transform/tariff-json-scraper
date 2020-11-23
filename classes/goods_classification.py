import sys
import os
import json

from classes.request import Request
from classes.chapter import Chapter


class GoodsClassification(object):
    def __init__(self):
        if len(sys.argv) > 1:
            if sys.argv[1] == "structure":
                self.download_structure()

            elif sys.argv[1] == "commodities":
                self.download_commodities()
        else:
            return

    def download_commodities(self):
        # Look for the downloaded goods_nomenclatures files in the sections folder
        root = os.path.dirname(os.path.realpath(__file__))
        root = os.path.join(root, "..")
        root = os.path.realpath(root)
        subfolder = os.path.join(root, "json")
        subfolder = os.path.join(subfolder, "goods_nomenclatures")
        if not(os.path.isdir(subfolder)):
            print("Subfolder cannot be found")
            sys.exit()
        else:
            file_list = os.listdir(subfolder)  # dir is your directory path
            file_list.sort()
            if len(file_list) != 21:
                print(
                    "There need to be 21 files in the json/goods_nomenclatures subfolder: one for each section")
                sys.exit()
            else:
                for file in file_list:
                    full_path = os.path.join(subfolder, file)
                    with open(full_path, "r") as f:
                        data = json.load(f)
                        for item in data["data"]:
                            href = item["attributes"]["href"]
                            goods_nomenclature_item_id = item["attributes"]["goods_nomenclature_item_id"]
                            chapter_id = goods_nomenclature_item_id[0:2]
                            if "commodities" in href:
                                url = 'commodities/{}'.format(goods_nomenclature_item_id)
                                path = 'json/commodities/{}/{}.json'.format(chapter_id, goods_nomenclature_item_id)
                                commodity = Request(url, path).json




    def download_structure(self):
        # self.get_sections()
        # self.get_chapters()
        # self.get_search_references()
        self.get_geographical_areas()
        self.get_footnote_types()
        self.get_certificate_types()
        self.get_additional_code_types()
        self.get_additional_codes()

    def get_sections(self):
        # Get all sections and section notes and commodities
        sections = Request("sections", "json/sections/sections.json").json
        for item in sections["data"]:
            # Get sections
            url = 'sections/{}'.format(item["id"])
            path = 'json/sections/section_{:0>2}.json'.format(item["id"])
            section = Request(url, path).json

            # Get section notes
            url = 'sections/{}/section_note'.format(item["id"])
            path = 'json/section_notes/section_note_{:0>2}.json'.format(
                item["id"])
            section_note = Request(url, path).json

            # Get commodities
            url = 'goods_nomenclatures/section/{}'.format(item["id"])
            path = 'json/goods_nomenclatures/goods_nomenclature_{:0>2}.json'.format(
                item["id"])
            section_note = Request(url, path).json

    def get_chapters(self):
        # Get all chapters
        chapters = Request("chapters", "json/chapters/chapters.json").json
        for item in chapters["data"]:
            # Get chapters
            chapter_id = item["attributes"]["goods_nomenclature_item_id"][0:2]
            url = 'chapters/{}'.format(chapter_id)
            path = 'json/chapters/chapter_{:0>2}.json'.format(chapter_id)
            chapter = Chapter(Request(url, path).json)

            # Get chapter notes
            url = 'chapters/{}/chapter_note'.format(chapter_id)
            path = 'json/chapter_notes/chapter_note_{:0>2}.json'.format(
                chapter_id)
            chapter_note = Request(url, path).json

    def get_search_references(self):
        # Get all search references (green pages)
        search_references = Request(
            "search_references", "json/search_references/search_references.json").json

    def get_geographical_areas(self):
        # Get all geographical areas
        geographical_areas = Request(
            "geographical_areas", "json/geographical_areas/geographical_areas.json").json
        countries = Request("geographical_areas/countries",
                            "json/geographical_areas/countries.json").json

    def get_footnote_types(self):
        # Get all footnote types
        footnote_types = Request(
            "footnote_types", "json/footnote_types/footnote_types.json").json

    def get_certificate_types(self):
        # Get all certificate types
        certificate_types = Request(
            "certificate_types", "json/certificate_types/certificate_types.json").json

    def get_additional_code_types(self):
        # Get all additional code types
        additional_code_types = Request(
            "additional_code_types", "json/additional_code_types/additional_code_types.json").json

    def get_additional_codes(self):
        types = "2346789ABCDPVX"
        types = [char for char in types]
        for type in types:
            url = 'additional_codes/search?type={}'.format(type)
            path = 'json/additional_codes/additional_codes_{}.json'.format(
                type)
            additional_codes = Request(url, path).json
