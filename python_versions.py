import itertools
import re
from dataclasses import dataclass
from html.parser import HTMLParser
from typing import List, Tuple

import requests
from packaging.version import Version

EMPTY_TAG = ""
ANCHOR_TAG = "a"
ANCHOR_HREF_ATTR = "href"

VERSION_REGEX = r"^(\d+\.)?(\d+\.)?(\*|\d+)"

HTTP_URL = "https://www.python.org/ftp/python/"


class PythonFTPHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self._current_tag = EMPTY_TAG
        self._links = []
        self._data = []

    def handle_starttag(self, tag, attrs):
        self._current_tag = tag
        if tag == ANCHOR_TAG:
            attrs = {k: v for k, v in attrs}
            if ANCHOR_HREF_ATTR in attrs:
                self._links.append(attrs[ANCHOR_HREF_ATTR])

    def handle_endtag(self, tag):
        self._current_tag = EMPTY_TAG

    def handle_data(self, data):
        if self._current_tag == ANCHOR_TAG:
            self._data.append(data.strip())

    def clear(self):
        self._links = []
        self._data = []

    def get_collected(self) -> List[Tuple[str, str]]:
        return list(zip(self._links, self._data))

    def then_feed(self, data: str) -> "PythonFTPHTMLParser":
        self.feed(data)
        return self


@dataclass
class VersionEntry:
    version: Version
    sub_url: str


def request_url(url: str) -> str:
    res = requests.get(url)
    if res.status_code >= 300:
        raise ValueError(f"Bad status code {res.status_code} from '{url}'")
    return res.text


def process_hrefs(links: List[Tuple[str, str]]) -> List[VersionEntry]:
    vers_regex = re.compile(VERSION_REGEX)
    hrefs = []
    for link, ver in links:
        matched = vers_regex.match(ver)
        if matched:
            s, e = matched.span()
            v = Version(ver[s:e])
            hrefs.append(VersionEntry(v, HTTP_URL + link))
    hrefs.sort(key=lambda e: e.version)
    return hrefs


def main():
    data = request_url(HTTP_URL)
    parser = PythonFTPHTMLParser().then_feed(data)
    processed = process_hrefs(parser.get_collected())
    grouped_vers = itertools.groupby(processed, key=lambda p: p.version.major)
    for major, its_vers in grouped_vers:
        if major == 3:
            print(f"{major}.x.x:")
            for ver in its_vers:
                print(f"--  {ver.version}")


if __name__ == "__main__":
    main()
