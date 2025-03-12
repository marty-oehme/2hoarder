#!/usr/bin/env python

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
    Path(sys.argv[2]) if len(sys.argv) > 2 else Path("exported_bookmarks.html")
)
print(f"[DEBUG]\ninput: {INPUT_FILE}\noutput: {OUTPUT_FILE}")


# TODO: Timestamp does not get recognized and instead becomes 1970-01-01 - maybe needs unix ts?
def generate_html(data):
    return Template("""<!DOCTYPE NETSCAPE-Bookmark-file-1>
    <META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
    <TITLE>Bookmarks</TITLE>
    <H1>Bookmarks</H1>
    <DL><p>
    {% for item in data %}
        <DT>
            <A HREF="{{ item.url }}" ADD_DATE="{{ item.created_at }}" TAGS="{{ item.tags }}">{{ item.title }}</A>
        </DT>
    {% endfor %}
    </DL><p>
    """).render(data=data)


# Read JSON file
with open(INPUT_FILE, "r") as f:
    data = json.load(f)

html_content = generate_html(data)

# Save or print HTML content
with open(OUTPUT_FILE, "w") as f:
    f.write(html_content)
