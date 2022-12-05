import http.cookiejar
import json
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import BinaryIO, Iterator, TextIO

CACHE_DIR = Path("./input/")
ENV_FILE = Path("./.env")
URL = "https://adventofcode.com/2022/day/{}/input"
UTF8 = "utf-8"


def iter_text(f: TextIO) -> Iterator[str]:
    while (line := f.readline()) != "":
        yield line[: len(line) - 1]


def iter_bytes(f: BinaryIO, encoding: str = UTF8) -> Iterator[str]:
    decoded = f.read().decode(encoding)
    yield from decoded.splitlines()


def add_cookie_to_request(
    name: str, value: str, host: str | None, request: urllib.request.Request
) -> None:
    jar = http.cookiejar.CookieJar()

    cookie = http.cookiejar.Cookie(
        version=0,
        name=name,
        value=value,
        port=None,
        port_specified=False,
        domain=host if host is not None else "",
        domain_specified=host is not None,
        domain_initial_dot=False,
        path="/",
        path_specified=True,
        secure=True,
        expires=None,
        discard=False,
        comment=None,
        comment_url=None,
        rest={},
        rfc2109=False,
    )
    jar.set_cookie(cookie)
    jar.add_cookie_header(request)


def fetch_input(puzzle_id: int) -> Iterator[str]:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    cache_file = CACHE_DIR.joinpath(f"input_{puzzle_id:02}.txt")

    try:
        with cache_file.open(mode="r", encoding=UTF8) as f:
            yield from iter_text(f)
            return
    except IOError:
        pass

    with ENV_FILE.open(mode="r", encoding=UTF8) as f:
        env = json.load(f)

    request = urllib.request.Request(
        url=URL.format(puzzle_id),
        headers={"User-Agent": "dev@wallparty.horse"},
        method="GET",
    )

    host = urllib.parse.urlsplit(URL).hostname
    add_cookie_to_request("session", env["cookie"], host, request)

    data = ""

    try:
        with urllib.request.urlopen(request) as f:
            data = f.read().decode(UTF8)
    except urllib.error.HTTPError as e:
        print(f"Response failed with code {e.code}, {e.reason}")
        return

    with cache_file.open(mode="w", encoding=UTF8) as f:
        f.write(data)

    yield from data.splitlines()
