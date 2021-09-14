import os
from typing import List

import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlsplit
from urllib.request import urlretrieve



def strip_scheme(url: str) -> str:
    parsed = urlsplit(url)
    scheme = f"{parsed.scheme}://"
    return parsed.geturl().replace(scheme, '', 1)


def download_assets(asset_urls: List[str], store_dir: str) -> None:
    for asset_url in asset_urls:
        asset_file_path = os.path.join(store_dir, strip_scheme(asset_url))
        dir_path = os.path.dirname(asset_file_path)
        os.makedirs(dir_path, exist_ok=True)
        urlretrieve(asset_url, asset_file_path)


def archive(url: str) -> None:
    # initialize a session
    session = requests.Session()
    # set the User-agent as a regular browser
    session.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"

    html = session.get(url).content
    parent_dir = "testing"

    # parse HTML using beautiful soup
    soup = bs(html, "html.parser")

    # get the JavaScript files
    script_files = []

    for script in soup.find_all("script"):
        if script.attrs.get("src"):
            # if the tag has the attribute 'src'
            script_url = urljoin(url, script.attrs.get("src"))
            script_files.append(script_url)

    # get the CSS files
    css_files = []

    for css in soup.find_all("link"):
        if css.attrs.get("href"):
            # if the link tag has the 'href' attribute
            css_url = urljoin(url, css.attrs.get("href"))
            css_files.append(css_url)

    # get the IMG files
    img_files = []

    for img in soup.find_all("img"):
        if img.attrs.get("src"):
            # if the link tag has the 'href' attribute
            img_url = urljoin(url, img.attrs.get("src"))
            img_files.append(img_url)

    print("Total script files in the page:", len(script_files))
    print("Total CSS files in the page:", len(css_files))
    print("Total IMG files in the page:", len(img_files))

    # download assets
    download_assets(css_files, store_dir=parent_dir)
    download_assets(img_files, store_dir=parent_dir)

    index_html_path = os.path.join(parent_dir, strip_scheme(url), "index.html")
    with open(index_html_path, "w") as f:
        f.write(str(soup))


if __name__ == "__main__":
    # URL of the web page you want to extract
    url = "http://books.toscrape.com"
    archive(url)