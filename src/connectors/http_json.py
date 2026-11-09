"""Minimal JSON API connector with explicit timeout and no hidden retries."""

from __future__ import annotations

import json
from urllib.request import Request, urlopen


class JsonApiConnector:
    def __init__(self, url: str, timeout: float = 10.0):
        self.url = url
        self.timeout = timeout

    def fetch(self) -> object:
        request = Request(self.url, headers={"User-Agent": "smart-parking-proposal/0.1"})
        with urlopen(request, timeout=self.timeout) as response:
            if response.status != 200:
                raise RuntimeError(f"HTTP {response.status}")
            return json.load(response)

