import json
import urllib.request
import re

class NotionSearcher():
    def __init__(self, notion_secret):
        self._NOTION_SECRET = notion_secret

    def search(self) -> list:
        response = self.make_request()

        results = response["results"] if response != [] else []

        while response["has_more"]:
            response = self.make_request(response["next_cursor"])
            results += response["results"]

        search_results = []
        for result in results:


            if result is None:
                continue

            parent = ""
            name = ""
            icon = ""
            url = ""

            if result["object"] == 'database':
                title_field = result["title"]
                for i in range(len(title_field)):
                    name += title_field[i]["text"]["content"]

            elif result["object"] == "page":
                title_field = self.get_title_field(result["properties"])
                for i in range(len(result["properties"][title_field]["title"])):
                    name += result["properties"][title_field]["title"][i]["plain_text"]

            # TODO: add parent {page, database} name

            # if "parent" in result:
            #     if "database_id" in result["parent"]:
            #         parent = result["parent"]["database_id"]
            #     elif "page_id" in result["parent"]:
            #         parent = result["parent"]["page_id"]


            name = name if name != "" else "<unnamed page>"

            try:
                icon = result["icon"]["external"]["url"]
            except (KeyError, TypeError):
                try:
                    icon = result["icon"]["file"]["url"]
                except (KeyError, TypeError):
                    pass

            if name and len(name[0]) > 1:
                # FIXME: hacky solution -- strings containing `.` or `,` are somewhy transformed into (<string>,) and then
                # parsed as tuples in underlying cpp
                name = name[0]

            url = result["url"]

            search_results.append({
                "name": name,
                "parent": parent,
                "iconURL": icon,
                "iconName": self.clean_filename(icon),
                "url": url
            })

        return search_results

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
        filename = re.sub('https://', '', filename)
        filename = re.sub('/', '-', filename)
        return filename
