import json
from datetime import datetime

from base import Wallabag_Converter

# NOTE: Wallabag annotation format is as follows:
# [{'text': '', 'quote': "A while back they raised their prices, which lost them a lot of subscribers, because they were losing money per search at the old prices. They were actually still losing money per search on the new prices. They eventually lowered the prices back down a bit (and maybe raised them again? I've completely lost the plot on their pricing at this point) and have claimed that at 25,000 users they would be breaking even.", 'ranges': [{'start': '/p[6]', 'startOffset': '429', 'end': '/p[6]', 'endOffset': '844'}]}]
# with /p signifying the paragraph? Hoarder only has a concept of offset, so probably have to transform the paragraphs into lengths and then add them up to convert from one format to the other.


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
