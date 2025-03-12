import json
import sys

from bs4 import BeautifulSoup

if len(sys.argv) < 2:
    print("ERROR: Pass the bookmarks file as argument.")
    sys.exit(1)
path = sys.argv[1]


def parse_bookmark(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    bookmarks = []

    if len(soup.find_all("dl")) != 1:
        print("WARNING! More than one Bookmark element found. File may be corrupt.")

    first = True
    last_desc = ""
    for el in soup.find_all("a"):
        bm_el = {}
        url = el["href"]
        title = el.string.strip() if el.string else url

        # date elements
        add_date = el.get("add_date", "")
        last_modified = el.get("last_modified", "")
        tag_string = el.get("tags", "")
        tags = tag_string.split(",") if tag_string else []

        # TODO: url contains '/shaare/' == note type

        # desc / note
        desc_el = el.parent.find_next_sibling("dd")
        # Have to fix the non-closed <dt> tabs :\
        # For now, in vim do: `:%s/<DT>.*/\0<\/DT>` to add a closing el to each line
        description = desc_el.contents[0].strip() if desc_el else ""
        if description and description == last_desc:
            description = ""
        if description:
            last_desc = description

        # print(f"URL: {url}, TITLE: {title}")
        # print(f"ADD: {add_date}, MOD: {last_modified}, TAGS: {tags}")
        # print(f"DESC: {description.strip()}")

        content = {}
        if "/shaare/" in url:
            content = {"type": "text", "text": description}
            # print(f"Detected note-style url ({url}) turning description to content.")
            description = ""
        else:
            content = {"type": "link", "url": url}

        bm_el = {
            "title": title,
            "note": description,
            "createdAt": int(last_modified if last_modified else add_date),
            "content": content,
        }
        if tags:
            bm_el["tags"] = tags
        if description:
            bm_el["note"] = description
        bookmarks.append(bm_el)

    return bookmarks


with open(path) as f:
    contents = f.readlines()
    for i, line in enumerate(contents):
        if "<DT>" in line:
            contents[i] = f"{line.rstrip()}</DT>"

    bookmarks = parse_bookmark("\n".join(contents))

    print(json.dumps({"bookmarks": bookmarks}, indent=2))
