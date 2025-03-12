#!/usr/bin/env python

from datetime import datetime
import json
import sys
from pathlib import Path

from jinja2 import Template

# USAGE: ./convert.py file exportfile

if len(sys.argv) < 2 or not Path(sys.argv[1]).is_file():
    print("Please provide a file to import as the first argument.")
    sys.exit(1)

INPUT_FILE = Path(sys.argv[1])
OUTPUT_FILE = (
    Path(sys.argv[2]) if len(sys.argv) > 2 else Path("exported_bookmarks.json")
)
print(f"[DEBUG] inputfile: {INPUT_FILE}")
print(f"[DEBUG] outputfile: {OUTPUT_FILE}")

# Read JSON file
with open(INPUT_FILE, "r") as f:
    data_in = json.load(f)

# NOTE: Wallabag annotation format is as follows:
# [{'text': '', 'quote': "A while back they raised their prices, which lost them a lot of subscribers, because they were losing money per search at the old prices. They were actually still losing money per search on the new prices. They eventually lowered the prices back down a bit (and maybe raised them again? I've completely lost the plot on their pricing at this point) and have claimed that at 25,000 users they would be breaking even.", 'ranges': [{'start': '/p[6]', 'startOffset': '429', 'end': '/p[6]', 'endOffset': '844'}]}]
# with /p signifying the paragraph? Hoarder only has a concept of offset, so probably have to transform the paragraphs into lengths and then add them up to convert from one format to the other.

print(f"[DEBUG] Found {len(data_in)} wallabag entries.")

data_out = {"bookmarks":[]}
n = 0
for entry in data_in:
    bm = {
        "createdAt": datetime.strptime(entry["created_at"], "%Y-%m-%dT%H:%M:%S%z").timestamp(),
        "content": {"type": "link", "url": entry["url"]},
        "title": entry["title"] if entry["title"] else None,
        "tags": entry["tags"] + ["wallabag"],
        # FIXME: Need to wait for better hoarder annotation handling to import them in a good format
        # for now we just turn them _all_ into a single note.
        # DOABLE WITH API? https://docs.hoarder.app/api/create-a-new-highlight
        "note": json.dumps(entry["annotations"]) if entry["annotations"] else None,
    }
    data_out["bookmarks"].append(bm)
    n += 1
    if n > 50:
        break

with open(OUTPUT_FILE, "w") as f:
    json.dump(data_out, f)
