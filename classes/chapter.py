import sys
from classes.request import Request


class Chapter(object):
    def __init__(self,  chapter):
        self.chapter = chapter
        self.download()

    def download(self):
        # Get all headings
        try:
            for item in self.chapter["included"]:
                if item["type"] == "heading":
                    heading_id = item["attributes"]["goods_nomenclature_item_id"][0:4]
                    url = 'headings/{}'.format(heading_id)
                    path = 'json/headings/heading_{}.json'.format(heading_id)
                    # heading = Request(url, path).json
        except:
            pass
