from bs4 import BeautifulSoup
import requests
from zipfile import ZipFile
from io import BytesIO
import pandas as pd
import re


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


def get_csv_urls(soup, base_url, latest_date_in_database):
    recent_csvs = soup.find_all('a', href=re.compile(".csv$"))

    csv_index_to_download_till = None
    for i, link in enumerate(recent_csvs):
        if latest_date_in_database in link.text:
            csv_index_to_download_till = i
    
    if csv_index_to_download_till == None:
        raise Exception("Error: Last date not found in the list of available csvs")
    if csv_index_to_download_till == 0:
        raise Exception("No new data to download")
    
    csv_urls_to_download = []
    for link in recent_csvs[:csv_index_to_download_till]:
        csv_urls_to_download.append(base_url + "/" + link['href'])

    return csv_urls_to_download


def update_data(link_to_data_csv, url_to_data_source):
    print("Retrieving existing data...")
    df = pd.read_csv(link_to_data_csv)
    print("Existing data retrieved...")

    latest_date_in_database_split = df['Time Stamp'].iloc[-1].split(' ')[0].split('-')
    latest_date_in_database = latest_date_in_database_split[1] + '-' + latest_date_in_database_split[2] + '-' + latest_date_in_database_split[0]    

    print("Downloading new data...")
    soup = get_soup_obj(url_to_data_source)
    csv_urls_to_download = get_csv_urls(soup, 'http://mis.nyiso.com/public', latest_date_in_database)

    new_data = []
    for url in csv_urls_to_download:
        new_data.append(pd.read_csv(url))
    df_new_data = pd.concat(new_data)
    df_new_data["Time Stamp"] = pd.to_datetime(df_new_data["Time Stamp"], format="%m/%d/%Y %H:%M")
    df_new_data = df_new_data.sort_values(by=["Time Stamp", "Name"], ascending=[True, True])
    print("New data downloaded...")

    print("Saving updated data...")
    return pd.concat([df, df_new_data]).to_csv(link_to_data_csv)




