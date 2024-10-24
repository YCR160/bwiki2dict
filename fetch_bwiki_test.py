import urllib3

gaplimit = 500
cllimit = 500

gapcontinue = None
clcontinue = None

http = urllib3.PoolManager()

HEADERS = {
    "User-Agent": f"BWIKI2Dict/0.1.0; github.com/YCR160/bwiki2dict",
    "Accept-Encoding": "gzip, deflate",
}

api_url = "https://wiki.biligame.com/sr/api.php"
fetch_url = f"{api_url}?action=query&generator=allpages&prop=categories&format=json&gaplimit={gaplimit}&cllimit={cllimit}"
resp = http.request("GET", fetch_url, headers=HEADERS, retries=3)
data = resp.json()

print(data)
