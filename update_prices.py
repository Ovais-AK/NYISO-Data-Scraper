from src import update_data
import pandas as pd

link_to_data = 'data/rtlbmp_zone_1999-2024.csv'
url_to_data_source = 'http://mis.nyiso.com/public/P-24Alist.htm'

print("Updating data...")
update_data(link_to_data, url_to_data_source)
print("Update complete...")

