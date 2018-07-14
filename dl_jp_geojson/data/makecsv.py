import pandas as pd


savename = "prefecture_city.csv"
savedf = False
for num in range(1, 48):
    strnum = '{0:02d}'.format(num)
    filename = "prefecture{}.txt".format(strnum)
    df = pd.read_csv(filename, sep='|', skiprows=[1])
    df.columns = ["nan0", 'prefecture_name', 'prefecture_code',
                  'city_name', 'city_code', 'gj', 'tj', 'nan7']
    df = df.astype(str)
    for col in df.columns[1:-1]:
        df[col] = df[col].str.strip()

    df = df.iloc[:, 1:5]
    if savedf is False:
        savedf = df
    else:
        savedf = pd.concat([savedf, df])

savedf = savedf.reset_index(drop=True)
savedf.to_csv(savename)
