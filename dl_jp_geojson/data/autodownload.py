import urllib.request
import urllib.error


for num in range(1, 48):
    strnum = '{0:02d}'.format(num)
    filename = "https://raw.githubusercontent.com/niiyz/JapanCityGeoJson/master/geojson/{}/README.md".format(
        strnum)
    savename = "prefecture{}.txt".format(strnum)

    try:
        print("file found at {}".format(filename))
        urllib.request.urlretrieve(filename, savename)
    except urllib.error.HTTPError as e:
        print("no file found at {}".format(filename))
