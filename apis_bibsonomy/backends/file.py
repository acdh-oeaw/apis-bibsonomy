import httpx
from pathlib import Path
import json


class FileBackend:
    def __init__(self, config):
        self.backend = config.get("backend", "zotero")
        self.path = config.get("file_path", f"/tmp/bibsonomy_cache_{self.backend}.json")
        group = config.get("group", None)
        user = config.get("user", None)
        path = f"user/{user}"
        if group:
            path = f"groups/{group}"
        self.endpoint = (
            f"https://api.zotero.org/{path}/items?include=data,bib,bibtex,csljson"
        )
        self.headers = {"Zotero-API-Key": config.get("KEY")}

    def iterate_zotero(self, endpoint: str) -> (int, list):
        items = []
        last_modified_version = None
        with httpx.Client() as client:
            while endpoint:
                response = client.get(endpoint, headers=self.headers)
                response.raise_for_status()

                items.extend(response.json())

                link = response.headers.get("link")
                last_modified_version = response.headers.get("last-modified-version")
                endpoint = None
                for item in link.split(","):
                    if item.split(";")[1] == ' rel="next"':
                        endpoint = item.split(";")[0].strip()[1:-1]
        return last_modified_version, items

    def merge_items(self, items, changed_items=[]):
        for item in changed_items:
            key = item["key"]
            items[key] = item
        return items

    def query_file(self, q, page_size=20, offset=0):
        file_path = Path(self.path)
        endpoint = self.endpoint

        paths = sorted(Path(file_path.parent).glob(f"{file_path.stem}.*"))
        items = {}
        if paths:
            endpoint += "&since=" + paths[0].suffix[1:]
            items = json.loads(paths[0].read_text())

        last_version, changed_items = self.iterate_zotero(endpoint)
        items = self.merge_items(items, changed_items)
        if changed_items:
            file_path = f"{file_path}.{last_version}"
            Path(file_path).write_text(json.dumps(items))

        return [
            item
            for (key, item) in items.items()
            if q.lower() in item["data"].get("title", "").lower()
        ]

    def get_bibtex_from_url(self, url):
        file_path = Path(self.path)
        paths = sorted(Path(file_path.parent).glob(f"{file_path.stem}.*"))
        if paths:
            for key, item in json.loads(paths[0].read_text()).items():
                if item["links"]["self"]["href"] == url:
                    return item["csljson"]
        return ""
