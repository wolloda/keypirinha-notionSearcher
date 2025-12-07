import json
import os
import re
import urllib.request

class NotionSearcher():
    def __init__(self, notion_secret, skip_untitled_pages):
        self._NOTION_SECRET = notion_secret
        self._SKIP_UNTITLED_PAGES = skip_untitled_pages
        self._pages = []

    def search(self, match_parents: bool = True) -> list:
        response = self.make_request()

        results = response["results"] if response != [] else []

        while response["has_more"]:
            response = self.make_request(response["next_cursor"])
            results += response["results"]

        search_results = []
        for result in results:
            if result is None:
                continue

            name = self.parse_name(result)
            icon_URL = None
            icon_name = None
            url = ""

            parent_id = ""
            if "parent" in result:
                if "database_id" in result["parent"]:
                    parent_id = result["parent"]["database_id"]
                elif "page_id" in result["parent"]:
                    parent_id = result["parent"]["page_id"]

            # FIXME: try-except -> if else?
            try:
                icon_URL = result["icon"]["external"]["url"]
            except (KeyError, TypeError):
                try:
                    icon_URL = result["icon"]["file"]["url"]
                except (KeyError, TypeError):
                    pass

            if name and len(name[0]) > 1:
                # FIXME: hacky solution -- strings containing `.` or `,` are somewhy transformed into (<string>,) and then
                # parsed as tuples in underlying cpp
                name = name[0]

            id = result["id"]
            url = result["url"]

            if icon_URL is not None:
                icon_name = self.clean_filename(icon_URL)
                _, icon_extension = os.path.splitext(icon_name)

                if icon_extension.upper() not in ['.ICO', '.PNG', '.JPG', '.JPEG']:
                    icon_URL = None
                    icon_name = None

            search_results.append({
                "id": id,
                "name": name,
                "parent": "",
                "parent_id": parent_id,
                "iconURL": icon_URL,
                "iconName": icon_name,
                "url": url
            })

        if match_parents:
            search_results = self.match_parents(search_results)

        if self._SKIP_UNTITLED_PAGES:
            search_results = list(filter(lambda result: result["name"] != "Untitled", search_results))

        return search_results

    def parse_name(self, result):
        name = ""

        if result["object"] == 'database':
            title_field = result["title"]
            for i in range(len(title_field)):
                name += title_field[i]["text"]["content"]

        elif result["object"] == "page":
            title_field = self.get_title_field(result["properties"])
            for i in range(len(result["properties"][title_field]["title"])):
                name += result["properties"][title_field]["title"][i]["plain_text"]

        if name == "":
            name = "Untitled"

        return name

    def match_parents(self, pages):
        for i in range(len(pages)):
            for j in range(len(pages)):
                if pages[j]["id"] == pages[i]["parent_id"]:
                    pages[i]["parent"] = pages[j]["name"]


        return pages

    def make_request(self, cursor = None) -> list:
        URL = "https://api.notion.com/v1/search"

        headers = {
            "Authorization": f"Bearer {self._NOTION_SECRET}",
            "Content-Type": 'application/json',
            "Notion-Version": '2022-02-22'
        }

        data = {
            "sort": {
                "direction": "descending",
                "timestamp": "last_edited_time"
            }
        }

        if cursor:
            data["start_cursor"] = cursor

        req = urllib.request.Request(
            URL, json.dumps(data).encode(), headers
        )

        res = ""

        with urllib.request.urlopen(req) as f:
            res = f.read().decode("utf-8")

        response = json.loads(res)
        if not response:
            return []

        return response

    def get_title_field(self, obj: dict):
        keys = obj.keys()
        for key in keys:
            if obj[key]["type"] == "title":
                return key

    def clean_filename(self, filename):
        filename = re.sub('https?://', '', filename)
        filename = re.sub('/', '-', filename)
        return filename
