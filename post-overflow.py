#!/usr/bin/env python3
from mitmproxy import http

def request(flow: http.HTTPFlow) -> None:
    if flow.request.url.startswith("http://log.z3.cn/"):
        # Extract the file name from the original URL
        file_name = flow.request.url.split("/")[-1]
        # Rewrite the URL
        new_url = f"https://myurl.com/{file_name}"
        flow.request.url = new_url
        print(f"Rewriting URL: {flow.request.url} -> {new_url}")
