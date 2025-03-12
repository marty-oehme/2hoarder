# wallabag2hoarder

Currently supports 2 conversions:

- ./convert_netscape.py:
    Converts into the 'netscape bookmark' format which hoarder should understand as 'html' import.
    It's a very lossy conversion, essentially only retaining url, title and creation time.
    Not tested well.

- ./convert_native_json.py:
    Uses the fact that wallabag outputs json and hoarder supports a native json export/import to
    transform the json into one that hoarder understands well. More tested, and works without a
    hitch, _however_ does not correctly transfer any annotations made in wallabag. Annotations
    are added as a simple json object to the 'note' field in hoarder.

- ./convert_api.py:
    _WIP_: Uses the public hoader API to move the wallabag articles over, _including_ annotations
    at a best-effort. Annotation support is a little behind the curve in hoarder -- we can only
    have highlights, not 'notes' attached to a highlight.
