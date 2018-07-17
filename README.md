# dl_jp_geojson

### [日本語]

## 概要

日本の都道府県、市区町村郡の境界線を示すgeojsonファイルをダウンロードし、pandas.DataFrame形式で読み込むライブラリです。

都道府県、市区町村郡の境界線は、[JapanCityGeoJson 2016](https://github.com/niiyz/JapanCityGeoJson)からダウンロードしています。
※JapanCityGeoJson 2016のデータソースは国土数値情報 (JPGIS2.1(GML)準拠及びSHAPE形式データ)　国土交通省



## 使用方法

- 使用例１（geojsonファイルの検索、ダウンロードから読み込みまで自動）

1. パッケージを読み込む
   `import dl_jp_geojson as dl`
2. ライブラリをインスタンス化する
   `dlgeojson = dl.core.DLGeoJSON()`
3. Geojsonファイルを検索し、見つかったものをすべてダウンロード、pandas.DataFrameで取得する。
   `jsondf = dlgeojson.read_geo_json("宮古")`



- 使用例２（手動検索、ダウンロード、読み込み）

1. パッケージを読み込む
   `import dl_jp_geojson as dl`
2. ライブラリをインスタンス化する
   `dlgeojson = dl.core.DLGeoJSON()`
3. 都道府県名もしくは市町村名でgeojsonを検索する。
   `founddf = dlgeojson.search_word("宮古")`
4. geojsonファイルをダウンロードする。
   `dlgeojson.download_files(founddf)`
5. ダウンロードしたgeojsonファイルをpandas.DataFrame形式で読み込む。 
   `jsondf = dlgeojson.import2pandas(founddf)`



- 出力形式

     上記のコードを実行すると、以下の形式のpandas.DataFrameでgeojsonが読み込まれる。

  ```
                          lons                                               lats
      0     [142.020434228, 142.020442892, 142.020451141, ...  [39.499224532, 39.499222279, 39.499222306, 39....
      1     [142.019816978, 142.019806744, 142.019796498, ...  [39.499232838, 39.499232559, 39.499232586, 39....
      2     [142.0174893, 142.017482477, 142.017477497, 14...  [39.499561559, 39.499561532, 39.499564, 39.499... 
  ```





### [English]

## General



Library for downloading prefecture/city boarder geojson files of Japan.

This module search and download prefecture/city boarder line geojson filesfrom github
(https://github.com/niiyz/JapanCityGeoJson).
Boarder json files will be donloaded to selected directory (default is ./geojson).
Also, you can import json files to your program as pandas DataFrame.




## Examples

* Example (Automatic Download and import):

​        1. Import package to your program.
            `import dl_jp_geojson as dl`
        2. Initiate the instance.
            `dlgeojson = dl.core.DLGeoJSON()`
        3. Search geojson and return pandas DataFrame
            `jsondf = dlgeojson.read_geo_json("宮古")`



* Example (Manual Download and import):

​        1. Import package to your program.
            `import dl_jp_geojson as dl`
        2. Initiate the instance.
            `dlgeojson = dl.core.DLGeoJSON()`
        3. Search json file by prefecture or city name.
            `founddf = dlgeojson.search_word("宮古")`
        4. Download json files.
            `dlgeojson.download_files(founddf)`
        5. Import json files to pandas
            `jsondf = dlgeojson.import2pandas(founddf)`

* Output pandas format:
          Using codes  demostrated above will return pandas DataFrame `jsondf` as following format.

                              lons                                               lats
          0     [142.020434228, 142.020442892, 142.020451141, ...  [39.499224532, 39.499222279, 39.499222306, 39....
          1     [142.019816978, 142.019806744, 142.019796498, ...  [39.499232838, 39.499232559, 39.499232586, 39....
          2     [142.0174893, 142.017482477, 142.017477497, 14...  [39.499561559, 39.499561532, 39.499564, 39.499... 

## Methods

```python
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
                    "or": search phrases with `or`. 
                    	(i.e. maches with geojson which has at least 1 phrase in its name)
                    "and": search phrases with `and`. 
                    	(i.e. maches with geojson which has all phrases in its name)
                    Only valid when List[str] is given as wordin.
                    Default is "or".

        download_files(founddf)
            Download geojson files.
            Geojson data specified in each row of `founddf`
            	(pandas.DataFrame returned from search_word()) will be downloaded.

            Parameters:
                - founddf [pandas.DataFrame]
                    Desired geojson information.
                    Return data of search_word() should be specified here.

        import2pandas(founddf)
            Import geojson data as pandas.DataFrame.
            Geojson data specified in each row of `founddf`
            	(pandas.DataFrame returned from search_word()) will be downloaded.
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
            Method for automatically process search_word(),download_files(),
            	and import2pandas().

            Parameters:
                - wordin [str or List[str]]
                    Search word phrase. Required.
                    Both str and List[str] is accepted.

                - algorithm="or" ["or" or "and"]
                    Search algorithm for multiple phrases given at wordin.
                    "or": search phrases with `or`. 
                    	(i.e. maches with geojson which has at least 1 phrase in its name)
                    "and": search phrases with `and`. 
                    	(i.e. maches with geojson which has all phrases in its name)
                    Only valid when List[str] is given as wordin.
                    Default is "or".
```

