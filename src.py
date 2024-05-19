from bs4 import BeautifulSoup
import requests
from zipfile import ZipFile
from io import BytesIO
import pandas as pd


def get_soup_obj(url):
    with requests.get(url) as response:
        html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def get_zipfile_urls(soup, base_url):
    zipfile_urls = []

    # find all urls in the html soup that contain 'csv.zip'
    for link in soup.find_all('a', href=re.compile('csv.zip')):
        # concatenate the base url with the link and append to the list
        zipfile_urls.append(base_url + "/" + link['href'])
    return zipfile_urls


def zipfiles_to_df(list_of_zipfiles_urls):
    dfs = []
    for zipfile in list_of_zipfiles_urls:
        with ZipFile(BytesIO(requests.get(zipfile).content)) as unzipped_zipfile:
            for file in unzipped_zipfile.namelist():
                with unzipped_zipfile.open(file) as csv:
                    dfs.append(pd.read_csv(csv))

    final_df = pd.concat(dfs)
    return final_df


