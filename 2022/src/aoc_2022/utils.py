import http.cookiejar
import json
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Iterator, TextIO

CACHE_DIR = Path("./input/")
ENV_FILE = Path("./.env")
URL = "https://adventofcode.com/2022/day/{}/input"
UTF8 = "utf-8"

__all__ = ["fetch_input"]


def fetch_input(puzzle_id: int) -> Iterator[str]:
    """Fetch the puzzle input remotely or from local disk cache.

    Args
    ----
        puzzle_id (int): the puzzle ID (day number).

    Yields
    ------
        Iterator[str]: an iterator of the input lines.
    """
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    cache_file = CACHE_DIR.joinpath(f"input_{puzzle_id:02}.txt")

    try:
        with cache_file.open(mode="r", encoding=UTF8) as f:
            yield from _iter_text(f)
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
    _add_cookie_to_request("session", env["cookie"], host, request)

    try:
        with urllib.request.urlopen(request) as f:
            # No nice way of streaming result as iterator, must decode from bytes first
            data = f.read().decode(UTF8)

            with cache_file.open(mode="w", encoding=UTF8) as f:
                f.write(data)

            yield from data.splitlines()
    except urllib.error.HTTPError as e:
        print(f"Response failed with code {e.code}, {e.reason}")
        return


def _iter_text(f: TextIO) -> Iterator[str]:
    while (line := f.readline()) != "":
        yield line[: len(line) - 1]


def _add_cookie_to_request(
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
