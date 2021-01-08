import sys
import os
import json

from classes.request import Request
from classes.chapter import Chapter


class GoodsClassification(object):
    def __init__(self):
        self.scope = ""
        self.as_of = ""

        minimum_code = ""
        if len(sys.argv) > 1:
            if sys.argv[1] == "structure":
                if len(sys.argv) > 2:
                    self.scope = sys.argv[2]
                else:
                    self.scope = "uk"
                if self.scope != "xi" and self.scope != "uk":
                    self.scope = "uk"

                if len(sys.argv) > 3:
                    self.as_of = sys.argv[3]
                else:
                    self.as_of = ""

                self.download_structure()

            elif sys.argv[1] == "commodities":
                if len(sys.argv) > 2:
                    self.scope = sys.argv[2]
                else:
                    self.scope = "uk"
                if self.scope != "xi" and self.scope != "uk":
                    self.scope = "uk"

                if len(sys.argv) > 3:
                    minimum_code = sys.argv[3]
                self.download_commodities(minimum_code)
        else:
            return

    def download_commodities(self, minimum_code):
        # Look for the downloaded goods_nomenclatures files in the sections folder
        root = os.path.dirname(os.path.realpath(__file__))
        root = os.path.join(root, "..")
        root = os.path.realpath(root)
        subfolder = os.path.join(root, "json")
        subfolder = os.path.join(subfolder, self.scope)
        subfolder = os.path.join(subfolder, "goods_nomenclatures")
        try:
            os.mkdir(subfolder)
        except:
            pass
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
                    if "04" in file:
                        full_path = os.path.join(subfolder, file)
                        looper = 0
                        with open(full_path, "r") as f:
                            data = json.load(f)
                            for item in data["data"]:
                                href = item["attributes"]["href"]
                                goods_nomenclature_item_id = item["attributes"]["goods_nomenclature_item_id"]
                                if goods_nomenclature_item_id[0:2] == "22":
                                # if goods_nomenclature_item_id >= minimum_code:
                                    producline_suffix = item["attributes"]["producline_suffix"]
                                    chapter_id = goods_nomenclature_item_id[0:2]
                                    if producline_suffix == "80":
                                        if "commodities" in href:
                                            looper += 1
                                            looper = looper % 4
                                            if looper != 999:
                                                url = 'commodities/{}'.format(
                                                    goods_nomenclature_item_id)
                                                path = 'json/[scope]/commodities/{}/{}.json'.format(
                                                    chapter_id, goods_nomenclature_item_id)
                                                # commodity = Request(url, path, self.scope, "2021-01-07").json
                                                commodity = Request(
                                                    url, path, self.scope, "").json

    def download_structure(self):
        self.get_sections()
        self.get_chapters()
        # self.get_search_references()
        # self.get_geographical_areas()
        # self.get_footnote_types()
        # self.get_certificate_types()
        # self.get_additional_code_types()
        # self.get_additional_codes()

    def get_sections(self):
        # Get all sections and section notes and commodities
        url = "json/[scope]/sections/sections.json"
        sections = Request("sections", "json/[scope]/sections/sections.json", self.scope, self.as_of).json
        for item in sections["data"]:
            # Get sections
            url = 'sections/{}'.format(item["id"])
            path = 'json/[scope]/sections/section_{:0>2}.json'.format(
                item["id"])
            section = Request(url, path, self.scope, self.as_of).json

            # Get section notes
            # url = 'sections/{}/section_note'.format(item["id"])
            # path = 'json/[scope]/section_notes/section_note_{:0>2}.json'.format(
            #     item["id"])
            # section_note = Request(url, path).json

            # Get commodities
            url = 'goods_nomenclatures/section/{}'.format(item["id"])
            path = 'json/[scope]/goods_nomenclatures/goods_nomenclature_{:0>2}.json'.format(
                item["id"])
            self.goods_nomenclatures = Request(url, path, self.scope, self.as_of).json

    def get_chapters(self):
        # Get all chapters
        chapters = Request(
            "chapters", "json/[scope]/chapters/chapters.json", self.scope, self.as_of).json
        for item in chapters["data"]:
            # Get chapters
            chapter_id = item["attributes"]["goods_nomenclature_item_id"][0:2]
            url = 'chapters/{}'.format(chapter_id)
            path = 'json/[scope]/chapters/chapter_{:0>2}.json'.format(
                chapter_id)
            chapter = Chapter(Request(url, path, self.scope, self.as_of).json, self.scope, self.as_of)

            # Get chapter notes
            # url = 'chapters/{}/chapter_note'.format(chapter_id)
            # path = 'json/[scope]/chapter_notes/chapter_note_{:0>2}.json'.format(
            #     chapter_id)
            # chapter_note = Request(url, path, self.scope, self.as_of).json

    def get_search_references(self):
        # Get all search refereçnces (green pages)
        search_references = Request(
            "search_references", "json/[scope]/search_references/search_references.json", self.scope, self.as_of).json

    def get_geographical_areas(self):
        # Get all geographical areas
        geographical_areas = Request(
            "geographical_areas", "json/[scope]/geographical_areas/geographical_areas.json", self.scope, self.as_of).json
        countries = Request("geographical_areas/countries", "json/[scope]/geographical_areas/countries.json", self.scope, self.as_of).json
        regions = Request("geographical_areas/regions", "json/[scope]/geographical_areas/regions.json", self.scope, self.as_of).json

    def get_footnote_types(self):
        # Get all footnote types
        footnote_types = Request(
            "footnote_types", "json/[scope]/footnote_types/footnote_types.json", self.scope, self.as_of).json

    def get_certificate_types(self):
        # Get all certificate types
        certificate_types = Request(
            "certificate_types", "json/[scope]/certificate_types/certificate_types.json", self.scope, self.as_of).json

    def get_additional_code_types(self):
        # Get all additional code types
        additional_code_types = Request(
            "additional_code_types", "json/[scope]/additional_code_types/additional_code_types.json", self.scope, self.as_of).json

    def get_additional_codes(self):
        types = "2346789ABCDPVX"
        types = [char for char in types]
        for type in types:
            url = 'additional_codes/search?type={}'.format(type)
            path = 'json/[scope]/additional_codes/additional_codes_{}.json'.format(
                type)
            additional_codes = Request(url, path, self.scope, self.as_of).json
