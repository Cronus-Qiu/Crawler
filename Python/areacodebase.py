import requests
import lxml.html
import csv
import random

UA = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
    "Opera/8.0 (Windows NT 5.1; U; en)",
    "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
]


def clear(data):
    if isinstance(data, list):
        data = data[0]

    return data.replace("\n", "").strip(" ")


def html_parse(content: str):
    html = lxml.html.fromstring(content)
    rows = html.xpath('//*[@class="views-table cols-7"]/tbody/tr')
    print(rows)
    return [
        (
            clear(row.xpath("td[4]/a/text()")),
            clear(row.xpath("td[5]/text()")),
            clear(row.xpath("td[6]/text()")),
            clear(row.xpath("td[7]/a/text()")),
        )
        for row in rows
    ]


def download(area_code, page: int = 0):
    if page == 0:
        url = f"https://{area_code}.areacodebase.com/zh-hans/number_type/M"
    else:
        url = f"https://{area_code}.areacodebase.com/zh-hans/number_type/M?page={page}"
    print(f"URL: {url}")
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "DNT": "1",
        "Host": f"{area_code}.areacodebase.com",
        "Pragma": "no-cache",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": random.choice(UA)
    }
    session = requests.Session()
    session.heades = headers
    # session.proxies = {
    #     "http": "http://127.0.0.1:1082",
    #     "https": "http://127.0.0.1:1082",
    # }
    try:
        response = session.get(url)
        response.raise_for_status()
        return response.text
    except Exception as err:
        print(err)
        return None


if __name__ == "__main__":
    area_code = "mmr"
    output = f"{area_code}.csv"
    lines = []
    for i in range(100):
        html = download(area_code, page=i)
        if not html:
            break
        line = html_parse(html)
        if not line:
            break
        print(f"Extract: {len(line)}")
        lines.extend(line)

    if lines:
        header = ("ndc", "from", "to", "operator")
        with open(output, "w", newline="") as fd:
            writer = csv.writer(fd)
            writer.writerow(header)
            for line in lines:
                writer.writerow(line)
