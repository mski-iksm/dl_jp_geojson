# -*- coding: utf-8 -*-
from . import helpers
import os
import pandas as pd
import csv
import urllib.request
import json


class DLGeoJSON:
    """ Library for downloading prefecture/city boarder geojson files of Japan.

    This module search and download prefecture/city boarder line geojson files\
    from github(https://github.com/niiyz/JapanCityGeoJson).
    Boarder json files will be donloaded to selected directory (default is ./geojson).
    Also, you can import json files to your program as pandas or geopandas using option.

    Example (Manual Download):
        1. Import package to your program.
            `import dl_jp_geojson as dl`
        2. Initiate the instance.
            `dlgeojson = dl.core.DLGeoJSON()`
        3. Search json file by prefecture or city name.
            `founddf = dlgeojson.search_word("宮古")`
        4. Download json files.
            `dlgeojson.download_files(founddf)`
        5. Import json files to pandas
            `dlgeojson.import2pandas(founddf)`
    """

    def __init__(self, dir='./geojson'):
        self.directory = self.set_directory(dir)
        self.df = self.readcsv()

    def set_directory(self, dir):
        if self.find_directory(dir):
            pass
        else:
            self.make_directory(dir)
        return dir

    def find_directory(self, dir):
        return os.path.exists(dir)

    def make_directory(self, dir):
        os.mkdir(dir)

    def readcsv(self):
        pkjpath = os.path.abspath(os.path.dirname(__file__))
        csvdf = pd.read_csv("{}/data/prefecture_city.csv".format(pkjpath))
        csvdf = csvdf.fillna(0)
        csvdf["prefecture_code"] = csvdf["prefecture_code"].astype(int)
        csvdf["city_code"] = csvdf["city_code"].astype(int)
        return csvdf

    def search_word(self, wordin, algorithm="or"):
        if isinstance(wordin, str):
            founddf = self.df.loc[self.df.loc[:, "prefecture_name"].str.contains(wordin) |
                                  self.df.loc[:, "city_name"].str.contains(wordin)].copy()
        elif isinstance(wordin, list):
            founddf = False
            targetdf = self.df.copy()
            for word in wordin:
                middf = targetdf.loc[targetdf.loc[:, "prefecture_name"].str.contains(word) |
                                     targetdf.loc[:, "city_name"].str.contains(word)].copy()
                if algorithm == "or":
                    if founddf is False:
                        founddf = middf
                    else:
                        founddf = pd.concat(founddf, middf)
                elif algorithm == "and":
                    targetdf = middf
                    founddf = middf

        return founddf

    def download_files(self, founddf):
        for row in founddf.iterrows():
            p_code = row[1]["prefecture_code"]
            c_code = row[1]["city_code"]
            self.download_json(p_code, c_code)
        return None

    def download_json(self, p_code, c_code):
        p_str = '{0:02d}'.format(p_code)
        c_str = '{0:05d}'.format(c_code)
        url = "https://raw.githubusercontent.com/niiyz/JapanCityGeoJson/master/geojson/{}/{}.json".format(
            p_str, c_str)
        fname = "{}.json".format(c_str)
        urllib.request.urlretrieve(url, "{}/{}".format(self.directory, fname))
        return None

    def import2pandas(self, founddf):
        imported_df = False
        for row in founddf.iterrows():
            p_code = row[1]["prefecture_code"]
            c_code = row[1]["city_code"]

            if imported_df is False:
                imported_df = self.readjson(p_code, c_code)
            else:
                imported_df = pd.concat(
                    imported_df, self.readjson(p_code, c_code))
        return imported_df

    def readjson(self, p_code, c_code):
        c_str = '{0:05d}'.format(c_code)
        fname = "{}.json".format(c_str)
        pathfname = "{}/{}".format(self.directory, fname)
        readjson_dic = json.loads(pathfname)
        print(readjson_dic)
        return 0

    def search_dl_all():
        return 0


if __name__ == "__main__":
    dlgeojson = DLGeoJSON()
    founddf = dlgeojson.search_word("昭島")
    dlgeojson.download_files(founddf)
    dlgeojson.import2pandas(founddf)
