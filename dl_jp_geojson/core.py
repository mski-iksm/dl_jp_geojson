# -*- coding: utf-8 -*-
from . import helpers
import os
import pandas as pd
import csv
import urllib.request
import json
import numpy as np


class DLGeoJSON:
    """ DLGeoJSON

    Library for downloading prefecture/city boarder geojson files of Japan.

    This module search and download prefecture/city boarder line geojson files
    from github(https://github.com/niiyz/JapanCityGeoJson).
    Boarder json files will be donloaded to selected directory (default is ./geojson).
    Also, you can import json files to your program as pandas DataFrame.

    Example (Automatic Download and import):
        1. Import package to your program.
            `import dl_jp_geojson as dl`
        2. Initiate the instance.
            `dlgeojson = dl.core.DLGeoJSON()`
        3. Search geojson and return pandas DataFrame
            `jsondf = dlgeojson.read_geo_json("宮古")`

    Example (Manual Download and import):
        1. Import package to your program.
            `import dl_jp_geojson as dl`
        2. Initiate the instance.
            `dlgeojson = dl.core.DLGeoJSON()`
        3. Search json file by prefecture or city name.
            `founddf = dlgeojson.search_word("宮古")`
        4. Download json files.
            `dlgeojson.download_files(founddf)`
        5. Import json files to pandas
            `jsondf = dlgeojson.import2pandas(founddf)`

    Output pandas format:
        Using codes  demostrated above will return pandas DataFrame `jsondf` as following format.

                            lons                                               lats
        0     [142.020434228, 142.020442892, 142.020451141, ...  [39.499224532, 39.499222279, 39.499222306, 39....
        1     [142.019816978, 142.019806744, 142.019796498, ...  [39.499232838, 39.499232559, 39.499232586, 39....
        2     [142.0174893, 142.017482477, 142.017477497, 14...  [39.499561559, 39.499561532, 39.499564, 39.499... 


    ------------------------------------------------------------------

    Methods:
        __init__(dir='./geojson')
            Initiate instance.
            Parameters:
                - dir [str]
                    Specifies the directory to download geojson files.
                    Default is `./geojson`.

        search_word(wordin, algorithm="or")
            Search geojson files including `wordin` phrase.
            Both prefecture name and city name is searched.
            Returns found geojson file information in pandas.DataFrame format
                with columns: ["prefecture_name", "prefecture_code", "city_name", "city_code"].

            Parameters:
                - wordin [str or List[str]]
                    Search word phrase. Required.
                    Both str and List[str] is accepted.

                - algorithm="or" ["or" or "and"]
                    Search algorithm for multiple phrases given at wordin.
                    "or": search phrases with `or`. (i.e. maches with geojson which has at least 1 phrase in its name)
                    "and": search phrases with `and`. (i.e. maches with geojson which has all phrases in its name)
                    Only valid when List[str] is given as wordin.
                    Default is "or".

        download_files(founddf)
            Download geojson files.
            Geojson data specified in each row of `founddf`(pandas.DataFrame returned from search_word()) will be downloaded.

            Parameters:
                - founddf [pandas.DataFrame]
                    Desired geojson information.
                    Return data of search_word() should be specified here.

        import2pandas(founddf)
            Import geojson data as pandas.DataFrame.
            Geojson data specified in each row of `founddf`(pandas.DataFrame returned from search_word()) will be downloaded.
            This should be called after download is completed.

            Parameters:
                - founddf [pandas.DataFrame]
                    Desired geojson information.
                    Return data of search_word() should be specified here.   

            Output pandas format:
                                    lons                                               lats
                0     [142.020434228, 142.020442892, 142.020451141, ...  [39.499224532, 39.499222279, 39.499222306, 39....
                1     [142.019816978, 142.019806744, 142.019796498, ...  [39.499232838, 39.499232559, 39.499232586, 39....
                2     [142.0174893, 142.017482477, 142.017477497, 14...  [39.499561559, 39.499561532, 39.499564, 39.499... 

        read_geo_json(wordin, algorithm="or")
            Method for automatically process search_word(),download_files(), and import2pandas().

            Parameters:
                - wordin [str or List[str]]
                    Search word phrase. Required.
                    Both str and List[str] is accepted.

                - algorithm="or" ["or" or "and"]
                    Search algorithm for multiple phrases given at wordin.
                    "or": search phrases with `or`. (i.e. maches with geojson which has at least 1 phrase in its name)
                    "and": search phrases with `and`. (i.e. maches with geojson which has all phrases in its name)
                    Only valid when List[str] is given as wordin.
                    Default is "or".


    """

    def __init__(self, dir='./geojson'):
        """__init__(dir='./geojson')
            Initiate instance.
            Parameters:
                - dir [str]
                    Specifies the directory to download geojson files.
                    Default is `./geojson`.
        """
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
        """search_word(wordin, algorithm="or")
            Search geojson files including `wordin` phrase.
            Returns found geojson file information in pandas.DataFrame format
            with columns: ["prefecture_name", "prefecture_code", "city_name", "city_code"].

            Parameters:
                - wordin [str or List[str]]
                    Search word phrase. Required.
                    Both str and List[str] is accepted.

                - algorithm="or" ["or" or "and"]
                    Search algorithm for multiple phrases given at wordin.
                    "or": search phrases with `or`. (i.e. maches with geojson which has at least 1 phrase in its name)
                    "and": search phrases with `and`. (i.e. maches with geojson which has all phrases in its name)
                    Only valid when List[str] is given as wordin.
                    Default is "or".
        """

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

        return founddf[["prefecture_name", "prefecture_code", "city_name", "city_code"]]

    def download_files(self, founddf):
        """download_files(founddf)
            Download geojson files.
            Geojson data specified in each row of `founddf`(pandas.DataFrame returned from search_word()) will be downloaded.

            Parameters:
                - founddf [pandas.DataFrame]
                    Desired geojson information.
                    Return data of search_word() should be specified here.
        """

        for row in founddf.iterrows():
            p_code = row[1]["prefecture_code"]
            c_code = row[1]["city_code"]

            # check existing files:
            c_str = '{0:05d}'.format(c_code)
            fname = "{}.json".format(c_str)
            pathfname = "{}/{}".format(self.directory, fname)
            if self.find_directory(pathfname) is False:
                # download files
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
        """import2pandas(founddf)
            Import geojson data as pandas.DataFrame.
            Geojson data specified in each row of `founddf`(pandas.DataFrame returned from search_word()) will be downloaded.
            This should be called after download is completed.

            Parameters:
                - founddf [pandas.DataFrame]
                    Desired geojson information.
                    Return data of search_word() should be specified here.   

            Output pandas format:
                                    lons                                               lats
                0     [142.020434228, 142.020442892, 142.020451141, ...  [39.499224532, 39.499222279, 39.499222306, 39....
                1     [142.019816978, 142.019806744, 142.019796498, ...  [39.499232838, 39.499232559, 39.499232586, 39....
                2     [142.0174893, 142.017482477, 142.017477497, 14...  [39.499561559, 39.499561532, 39.499564, 39.499... 

        """

        geo_list = []
        for row in founddf.iterrows():
            p_code = row[1]["prefecture_code"]
            c_code = row[1]["city_code"]

            jsondata = self.readjson(p_code, c_code)
            geo_list = geo_list + jsondata
        imported_df = pd.DataFrame(geo_list, columns=["lons", "lats"])

        return imported_df

    def readjson(self, p_code, c_code):
        """
        Read each json file and returns list of geojson coordinate.

        Output format:
        [
            [ # feature 1
                [120,120,...], # lons
                [30,31,...]  # lats
            ],
            [ # feature 2
                [], # lons
                []  # lats
            ],
        ] 
        """
        c_str = '{0:05d}'.format(c_code)
        fname = "{}.json".format(c_str)
        pathfname = "{}/{}".format(self.directory, fname)
        f = open(pathfname, 'r')
        readjson_dic = json.load(f)
        f.close()

        coordlist = []
        # iter for each feature (isolated land block; e.g. island)
        for feature in readjson_dic["features"]:
            coordrow = []
            lons = np.array(feature["geometry"]["coordinates"])[0].T[0]
            lats = np.array(feature["geometry"]["coordinates"])[0].T[1]
            coordrow.append(lons.tolist())
            coordrow.append(lats.tolist())
            coordlist.append(coordrow)

        return coordlist

    def read_geo_json(self, wordin, algorithm="or"):
        """read_geo_json(wordin, algorithm="or")
            Method for automatically process search_word(),download_files(), and import2pandas().

            Parameters:
                - wordin [str or List[str]]
                    Search word phrase. Required.
                    Both str and List[str] is accepted.

                - algorithm="or" ["or" or "and"]
                    Search algorithm for multiple phrases given at wordin.
                    "or": search phrases with `or`. (i.e. maches with geojson which has at least 1 phrase in its name)
                    "and": search phrases with `and`. (i.e. maches with geojson which has all phrases in its name)
                    Only valid when List[str] is given as wordin.
                    Default is "or".
        """

        founddf = self.search_word(wordin, algorithm)
        self.download_files(founddf)
        jsondf = self.import2pandas(founddf)
        return jsondf


if __name__ == "__main__":
    dlgeojson = DLGeoJSON()
    founddf = dlgeojson.search_word("宮古")
    dlgeojson.download_files(founddf)
    jsondf = dlgeojson.import2pandas(founddf)
