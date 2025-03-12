import json
import re

from base import Wallabag_Converter
from bs4 import BeautifulSoup

# test_api_key: ak1_d202e69375c111461882_b0271d0e739ce0234f96
from requests import Response, request

# NOTE: Wallabag annotation format is as follows:
# [{'text': '', 'quote': "A while back they raised their prices, which lost them a lot of subscribers, because they were losing money per search at the old prices. They were actually still losing money per search on the new prices. They eventually lowered the prices back down a bit (and maybe raised them again? I've completely lost the plot on their pricing at this point) and have claimed that at 25,000 users they would be breaking even.", 'ranges': [{'start': '/p[6]', 'startOffset': '429', 'end': '/p[6]', 'endOffset': '844'}]}]
# with /p signifying the paragraph? Hoarder only has a concept of offset, so probably have to transform the paragraphs into lengths and then add them up to convert from one format to the other.


class API_Converter(Wallabag_Converter):
    def __init__(self, data: list[dict], hoarder_url: str, hoarder_key: str):
        self.data = data
        self.url = hoarder_url
        self.key = hoarder_key

        self.api_url = f"{self.url}/api/v1"
        self.bm_url = f"{self.api_url}/bookmarks"
        self.hl_url = f"{self.api_url}/highlights"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.key}",
        }

    def convert(self) -> str:
        print(f"[DEBUG] Found {len(self.data)} wallabag entries.")

        for entry in self.data:
            # bm = {
            #     "content": {"type": "link", "url": entry["url"]},
            # }
            response = self._create_bookmark(entry).json()
            id = response["id"]

            if "alreadyExists" in response and response["alreadyExists"]:
                print(f"[INFO] Skip adding url: {entry['url']} already exists.")

            if entry["tags"]:
                self._create_tags(id, entry)

            if entry["annotations"]:
                self._create_annotations(id, entry)

        return json.dumps("Done.")

    def _create_bookmark(self, entry) -> Response:
        payload = json.dumps(
            {
                "title": entry["title"] if entry["title"] else None,
                "archived": True if entry["is_archived"] == 1 else False,
                "favourited": True if entry["is_starred"] == 1 else False,
                "type": "link",
                "url": entry["url"],
                "tags": entry["tags"] + ["_wallabag"],
                # "note": "string",
                # "summary": "string",
                # "createdAt": datetime.strptime(
                #     entry["created_at"], "%Y-%m-%dT%H:%M:%S%z"
                # ).timestamp(),
                "createdAt": entry["created_at"],
            }
        )
        response = request("POST", self.bm_url, headers=self.headers, data=payload)
        return response

    def _create_tags(self, id, entry) -> Response:
        payload = json.dumps({"tags": [{"tagName": tag} for tag in entry["tags"]]})
        print(f"[DEBUG] Found {len(entry['tags'])} tags for {entry['url']}.")
        tag_attach_url = f"{self.bm_url}/{id}/tags"
        response = request(
            "POST",
            tag_attach_url,
            headers=self.headers,
            data=payload,
        )
        print(f"[DEBUG] TAGS: {response.json()}")
        return response

    def _create_annotations(self, entry_id, entry) -> Response:
        payload_dict = {
            "bookmarkId": entry_id,
            "startOffset": 5000,
            "endOffset": 6000,
            "color": "yellow",
            "text": "MYTEXT",
            "note": "mynote",
        }

        annot_url = f"{self.api_url}/highlights"
        for annot in entry["annotations"]:
            pl = payload_dict
            pl["text"] = annot["quote"]
            pl["note"] = annot["text"] if "text" in annot else None
            pl["startOffset"], pl["endOffset"] = self._calc_annot_offsets(
                entry["content"], annot
            )
            if pl["startOffset"] == -1:
                print(f"[WARNING] Annotation not found in bookmark: {annot['quote']}")
                continue

            response = request(
                "POST",
                annot_url,
                headers=self.headers,
                data=json.dumps(pl),
            )
            print(f"[DEBUG] New annotation: {response.json()}")
        response = Response()
        return response

    def _calc_annot_offsets(self, content, annot) -> tuple[int, int]:
        print(f"START: {annot['ranges'][0]['start']}")
        p_start_match = re.match(r"/p\[(\d+)\]", annot["ranges"][0]["start"])
        if p_start_match and len(p_start_match.groups()) == 1:
            p_start = int(p_start_match[1])

        bs4 = BeautifulSoup(content, "lxml")
        relevant_p = bs4.find_all("p")[p_start]
        start_offset = str(bs4.text).find(str(relevant_p.text))
        end_offset = start_offset + len(annot["quote"])
        return (start_offset, end_offset)
