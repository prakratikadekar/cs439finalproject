import pandas as pd
from sentence_transformers import SentenceTransformer
import re
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import kaggle
import time 

model = SentenceTransformer('all-MiniLM-L6-v2')


# sample user input
user_input = 'facebook'
user_input_embedding = model.encode(user_input)


# filtered dataset that was obtained from original (put link here for ref)
# df = pd.read_csv('https://www.kaggle.com/datasets/prakratikadekar/guardian-filtered', sep='\t')

# kaggle.api.dataset_download_files(
#     'prakratikadekar/guardian-filtered',
#     path='data/',
#     unzip=True
# )

df = pd.read_csv('data/guardian_filtered.csv')
print('read dataset')

print('columns: ', df.columns)
print('dataset type: ', df['bodyContent'].dtype)
print('first 5 entries: ', df.head())

# object -> string
df['bodyContent'] = df['bodyContent'].astype(str)
df['webTitle'] = df['webTitle'].astype(str)


start_time = time.time() 

def clean_datacol(col_data):
    col_data = re.sub(r'<.*?>', '', col_data) # removes HTML
    col_data = re.sub(r'\s+', ' ', col_data) # removes extra whitespace
    return col_data.lower()
print('cleaned data')


#bodyContent in dataset is the article content (title and everything else kept the same)
df['cleaned_bodyContent'] = df['bodyContent'].apply(clean_datacol)
df['cleaned_title'] = df['webTitle'].apply(clean_datacol)
print('applied cleaning')

df['embedded_title'] = df['cleaned_title'].apply(lambda x: model.encode(x))
print('apply embeddings to titles')

title_embeddings = np.vstack(df['embedded_title'].values)
similarities = cosine_similarity([user_input_embedding], title_embeddings)
print('used cosine similarities with body content')


# # now the article's body content is a vector where similar texts will have vectors close together
# df['embedded_bodyContent'] = df['cleaned_bodyContent'].apply(lambda x: model.encode(x))
# print('model has been applied to body content')

# article_embeddings = np.vstack(df['embedded_bodyContent'].values)
# print('gathered article embeddings')

# similarities = cosine_similarity([user_input_embedding], article_embeddings)
# print('used cosine similarities with body content')

# top 3
top_matches = similarities.sort()[-3:][:]
recommended_guardian_articles = df.iloc[top_matches]


print(recommended_guardian_articles[['title', 'sectionName', 'webTitle', 'webUrl']])

end_time = time.time()

print('total time taken: ', end_time - start_time)






# import kagglehub


# import pandas as pd
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)

# df = pd.read_csv('guardian_articles.csv')

# # print(df.head()) # print first 5 rows


# sections_to_keep = [
#     "US news",
#     "World news",
#     "News",
#     "Australia news",
#     "UK news",
#     "Politics",
#     "Technology"
# ]

# filtered_news = df[df['sectionName'].isin(sections_to_keep)]
# filtered_news = filtered_news.reset_index(drop=True)

# filtered_news.to_csv('guardian_filtered.csv', index=False)

# print('Filtered dataset: ', len(filtered_news))

# path = kagglehub.dataset_download("prakratikadekar/guardian-filtered")



# print("USERNAME =", os.getenv("KAGGLE_USERNAME"))
# print("KEY =", os.getenv("KAGGLE_KEY"))

# try:
#     kaggle.api.set_config_value("username", os.getenv("KAGGLE_USERNAME"))
#     kaggle.api.set_config_value("key", os.getenv("KAGGLE_KEY"))
#     kaggle.api.authenticate()
#     print("Auth OK")
# except Exception as e:
#     print("Auth FAIL:", e)

# print(kaggle.api.dataset_list(user='prakratikadekar'))