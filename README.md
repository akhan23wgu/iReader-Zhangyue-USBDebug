# Enable iReader SmartOS USB Debugging
These scripts were tested on the Zhangyue iReader Ocean 2 with the latest firmware. With the latest Zhangyue iReader Android 9 updates, custom apps cannot be deployed via proxy. This repo includes a collection of scripts that crashes the iReader app to access the Android settings menu. There are probably better ways to do this, but it's what worked for me after a couple weeks of tinkering with the device.

Here are a series of scripts I used on a fully updated iReader Ocean 2 to enabled Android USB Debugging and allowing apps from the File Explorer app.
Full disclosure: I wasn't able to get Android Studio to detect the iReader as an Android tablet, nor install any apps. There are also numerous calls to home (even if you click the menu button, it's logged), so I'm leaving my results here to see if it can help someone else.

### Required applications:
- Python 3
- mitmproxy (python3 -m pip install mitmproxy)
- http (python3 -m pip install http)
- Ability to generate subdomains
  - I used an existing wildcard certificate and route with traefik. You might be able to get away with using `/etc/hosts`.

### Limitations of iReader SmartOS
These are the limitations placed by Zhangyue on iReader SmartOS, which intentionally breaks some of Android's features to prevent sideloading and custom modifications:
- Does NOT allow enabling of system or user CA certificates
- No native browser, only Android WebView
- File Browser only opens specific documents, even apks are opened in PDFs
  
I suggest using a python virtual environment to get started. As the name implies, mitmproxy is used to perform a MITM attack again URLS. Here are a list of non-SSL URLs used by the device:
`http://log.z3.cn/` (phone home)
`http://g.cn/` (check internet connectivity)

## Accessing Android Settings
### Enable ADB & Unkown Sources in File Explorer

The following steps will crash the iReader "Home" application. Once the crash occurs, a popup will appear with the “App Info” button.

1. Start mitmproxy
`mitmproxy --mode regular --listen-host 0.0.0.0 --listen-port 8000 --set connection_strategy=lazy --allow-hosts "google.com" --script post-overflow.py`

2. Launch a new terminal. Navigate to ~/iReader-Zhangyue-USBDebug
`cd ~/iReader-Zhangyue-USBDebug`

3. Run http_server.py. You can replace `payloadk-mitm.apk` with any apk - the content is not important. We're just crashing the home app.
`python3 http_server.py`

### Crash the iReader Home Application
1. Download a couple of documents or books that are ~200MB to 300MB in size. Keep opening/closing the applications repeatedly. After a few crashes, you get a pop-up with the “App Info” button. 
<img src="https://github.com/user-attachments/assets/06a37c55-dc4b-4d95-bf77-31f3a87eb3bb" width=50% height=50%>

3. Once you click the “App Info” button, there is an invisible search button on the top-right. This is always there - use it to navigate settings. (Hard to see because of contrast). Click it and a search bar will appear.
<img src="https://github.com/user-attachments/assets/9efe3782-f7de-47df-a9ac-0bb2eb57ed9d" width=50% height=50%>

### Enable Developer Mode 
- Search "About" > Go to About > Press the build version 7 times to enable Developer mode. You will get a message saying Developer Mode has been enabled.

### Enable USB Debugging  
- Search "Developer" and click "Developer Mode"
- Scroll down and enabled "USB Debugging"
<img src="https://github.com/user-attachments/assets/7321bcd4-7c40-470d-9f31-2642aebe11d5" width=50% height=50%>
<img src="https://github.com/user-attachments/assets/8ffc6974-3482-40fe-a4c0-57b1745f0fa4" width=50% height=50%>

### Enable "Install Unknown Apps" in File Explorer
- Search "Apps" > Go to "Apps & App Info"
- Go to File Explorer
- Enable “Install from unknown sources” for File Explorer
<img src="https://github.com/user-attachments/assets/cdc9c181-49f2-4e5c-9868-01fc54956c4d" width=50% height=50%>

## Access Android WebView

1. Start mitmproxy with:
```python
mitmproxy --mode regular --listen-host 0.0.0.0 --listen-port 8000 --set connection_strategy=lazy --allow-hosts "google.com" --script mitm-server.py
```
2. Open a new terminal and navigate to the `~/iReader-Zhangyue-USBDebug` directory and start a web server with `python3 -m http.server 8080`.
3. On your iReader, stop and start Wi-Fi.
4. An Android WebView window will appear with the website defined in mitm-server.py.
  - This NEEDS to have a valid trusted certificate, or else you will get SSL errors. See trusted-ca.txt for a list of trusted CAs. I was able to use a Let's Encrypt certificate to browse without any issues.
