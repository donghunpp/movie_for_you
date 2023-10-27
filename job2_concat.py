import pandas as pd
import glob

data_paths = glob.glob('./crawing_data/*')
print(data_paths[:-5])

df = pd.DataFrame()
for path in data_paths:
    df_temp = pd.read_csv(path)
    df_temp.dropna(inplace=True)
    df_temp.drop_duplicates(inplace = True)
    df = pd.concat([df, df_temp], ignore_index = True)
df.drop_duplicates(inplace = True)
df.info()
my_year = 2023
df.to_csv('./crawling_data/reivews.csv', index = False)


