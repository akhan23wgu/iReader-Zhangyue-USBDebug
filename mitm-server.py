#!/usr/bin/python3
from mitmproxy import http

def request(flow):
    if flow.request.port == 80:
        if flow.request.url.startswith("http://log.z3.cn/"):
            flow.response = http.Response.make(302, b'',
                            http.Headers(Location='file:///SD card/F-Droid.apk',
                            content_type="application/vnd.android.package-archive",
                            content_disposition="attachment; filename=F-Droid.apk"))
        if flow.request.url.startswith("http://g.cn/"):
            flow.response = http.Response.make(302, b'',
                            http.Headers(Location='https://myurl.com'))
