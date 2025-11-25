import kagglehub

path = kagglehub.dataset_download("prakratikadekar/guardian-filtered")
print("Path to dataset files:", path)

import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

df = pd.read_csv('guardian_articles.csv')

# print(df.head()) # print first 5 rows


sections_to_keep = [
    "US news",
    "World news",
    "News",
    "Australia news",
    "UK news",
    "Politics",
    "Technology"
]

filtered_news = df[df['sectionName'].isin(sections_to_keep)]
filtered_news = filtered_news.reset_index(drop=True)

filtered_news.to_csv('guardian_filtered.csv', index=False)

print('Filtered dataset: ', len(filtered_news))
