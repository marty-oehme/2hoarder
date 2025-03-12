import json
from datetime import datetime

from base import Wallabag_Converter

class JSON_Converter(Wallabag_Converter):
    def __init__(self, data: list[dict]):
        self.data = data

    def convert(self) -> str:
        print(f"[DEBUG] Found {len(self.data)} wallabag entries.")

        data_out = {"bookmarks": []}
        n = 0
        for entry in self.data:
            bm = {
                "createdAt": datetime.strptime(
                    entry["created_at"], "%Y-%m-%dT%H:%M:%S%z"
                ).timestamp(),
                "content": {"type": "link", "url": entry["url"]},
                "title": entry["title"] if entry["title"] else None,
                "tags": entry["tags"] + ["_wallabag"],
                # FIXME: Need to wait for better hoarder annotation handling to import them in a good format
                # for now we just turn them _all_ into a single note.
                # DOABLE WITH API? https://docs.hoarder.app/api/create-a-new-highlight
                "note": json.dumps(entry["annotations"])
                if entry["annotations"]
                else None,
            }
            data_out["bookmarks"].append(bm)

        return json.dumps(data_out)
