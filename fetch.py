import time
import urllib3
from deepmerge import always_merger

http = urllib3.PoolManager()

gaplimit = 500
cllimit = 500

HEADERS = {
    "User-Agent": f"BWIKI2Dict/0.1.0; github.com/YCR160/bwiki2dict",
    "Accept-Encoding": "gzip, deflate",
}


def fetch_all_titles(api_url="https://wiki.biligame.com/sr/api.php"):
    data = {}
    all_data = {}

    gapcontinue = None
    clcontinue = None

    fetch_url = f"{api_url}?action=query&generator=allpages&prop=categories&format=json&gaplimit={gaplimit}&cllimit={cllimit}"

    cont = True
    while cont:
        clcontinue = data.get("continue", {}).get("clcontinue")

        if "gapcontinue" in data.get("continue", {}).get("continue", {}):
            gapcontinue = data.get("continue", {}).get("gapcontinue")
            # print(f"已获取{all_data['query']['pages'].__len__()}条数据，目前：{gapcontinue}")

        # print(f"gapcontinue: {gapcontinue}, clcontinue: {clcontinue}")

        now_fetch_url = fetch_url
        if gapcontinue:
            now_fetch_url += f"&gapcontinue={gapcontinue}"
        if clcontinue:
            now_fetch_url += f"&clcontinue={clcontinue}"

        # print(now_fetch_url)

        resp = http.request("GET", now_fetch_url, headers=HEADERS, retries=3)

        if resp.status == 200 and "application/json" in resp.headers.get("Content-Type"):
            data = resp.json()
            all_data = always_merger.merge(all_data, data)
            cont = data.get("continue", False)
        else:
            print("Error: ", resp.status, resp.headers.get("Content-Type"))
            time.sleep(5)

    return all_data


if __name__ == "__main__":
    import json

    all_data = fetch_all_titles()
    with open("allpages.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(all_data, ensure_ascii=False, indent=2))
