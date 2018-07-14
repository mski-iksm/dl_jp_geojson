# -*- coding: utf-8 -*-
from . import helpers
import os
import pandas as pd
import pkgutil
import csv


class DLGeoJSON:

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
        readdata = pkgutil.get_data('dl_jp_geojson',
                                    'dl_jp_geojson/data/prefecture_city.csv')
        csvdata = csv.reader(readdata.decode(
            'utf-8').splitlines(), delimiter=',')
        print(csvdata)
        # return pd.read_csv("dl_jp_geojson/data/prefecture_city.csv")
        return 0

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

        founddf["city_code"] = founddf["city_code"].astype(int)
        return founddf


if __name__ == "__main__":
    dlgeojson = DLGeoJSON()
    search = dlgeojson.search_word("宮古")
    print(search)
