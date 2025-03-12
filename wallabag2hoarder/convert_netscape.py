from base import Wallabag_Converter
from jinja2 import Template


class Netscape_Converter(Wallabag_Converter):
    def __init__(self, data: list[object]):
        self.data = data

    # TODO: Timestamp does not get recognized and instead becomes 1970-01-01 - maybe needs unix ts?
    def _generate_html(self, data):
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

    def convert(self) -> str:
        return self._generate_html(self.data)
