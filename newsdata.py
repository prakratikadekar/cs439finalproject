import pandas as pd
from sentence_transformers import SentenceTransformer
import re
import numpy as np
import kaggle
import time 

model = SentenceTransformer('all-MiniLM-L6-v2')



# sample user input



# ----------- STEP 1: Filter dataset for just political and computer science/technology topics ---------------------------------------


# df = pd.read_csv('guardian_articles.csv')

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

# filtered dataset that was obtained from original 
df = pd.read_csv('https://www.kaggle.com/datasets/prakratikadekar/guardian-filtered', sep='\t')

kaggle.api.dataset_download_files(
    'prakratikadekar/guardian-filtered',
    path='data/',
    unzip=True
)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

# ----------- STEP 2: Read dataset and convert the data columns of title and body content into strings ---------------------------------------


df = pd.read_csv('data/guardian_filtered.csv', encoding='utf-8')
# print('read dataset')

# print('columns: ', df.columns)
# print('dataset type: ', df['bodyContent'].dtype)
# print('first 5 entries: ', df.head())

# object -> string
# df['bodyContent'] = df['bodyContent'].astype(str)
# df['webTitle'] = df['webTitle'].astype(str)


# ----------- STEP 3: Clean dataset to get rid of extra HTML from kaggle + extra whitespace  ---------------------------------------

# def clean_datacol(col_data):
#     col_data = re.sub(r'<.*?>', '', col_data) # removes HTML
#     col_data = re.sub(r'\s+', ' ', col_data) # removes extra whitespace
#     return col_data.lower()
# print('cleaned data')


# #bodyContent in dataset is the article content (title and everything else kept the same)
# df['cleaned_bodyContent'] = df['bodyContent'].apply(clean_datacol)
# df['cleaned_title'] = df['webTitle'].apply(clean_datacol)
# print('applied cleaning')

# article_titles = df['cleaned_title'].tolist()
# articles_body_content = df['cleaned_bodyContent'].tolist()

# ----------- STEP 4: Use the Sentence Transformer model to encode both the titles and body content of articles with sentiment values (384 dimensional vector). This is a pretrained model  ---------------------------------------

# model documentation: https://sbert.net/examples/sentence_transformer/applications/computing-embeddings/README.html

# news_content = df['cleaned_title'] + " " + df['cleaned_bodyContent']
# news_embeddings = model.encode(news_content.tolist(), batch_size=100)
# print('model has been applied')


# ----------- STEP 5: After running above code once, saved it to an npy file so we do not need to rerun again - these are our news embeddings  ---------------------------------------

# np.save('news_embeddings.npy', news_embeddings)

# print('shape of news embeddings', news_embeddings.shape)

# ----------- STEP 6: Cosine similarity: use the embeddings of user input and news data to find which articles are similar to  ---------------------------------------
# ----------- STEP 7: Gather highest 3 cosine similarities of input and embedding data ---------------------------------------
# ----------- STEP 8: Write the articles in the txt file ---------------------------------------

def get_top_news_matches(user_input): 

    user_input_embedding = model.encode(user_input)

    news_embeddings = np.load('news_embeddings.npy')


    user_input_embedding = np.atleast_2d(user_input_embedding)
    user_input_normalized = user_input_embedding / np.linalg.norm(user_input_embedding, axis=1, keepdims=True)

    news_embeddings_normalized = news_embeddings / np.linalg.norm(news_embeddings, axis=1, keepdims=True) # column -> 1 dimension across all articles (rows)

    similarities = np.dot(user_input_normalized, news_embeddings_normalized.T)
    
    # get index for the 3 highest similarities in relation to news embeddings
    # order from greatest to least similarity
    best_matches = np.argsort(similarities[0])[-3:][::-1] # indices of top 3 largest similarities from cosine
    # print('best matches shape: ', best_matches.shape)

    recommended_guardian_articles = df.iloc[best_matches]

    with open('recommended_news.txt', 'a', encoding='utf-8') as file: 
        file.write('\n\nNEW RUN:\n')
        file.write(recommended_guardian_articles[['sectionName', 'webTitle', 'webUrl']].to_string())



# main:
get_top_news_matches('ai')












# ----------------------- ARCHIVE CODE -------------------------------------------------------







# similarities = cosine_similarity([user_input_embedding], article_embeddings)

# top 3
# print('similarity shape', similarities.shape)

# flatten
# row = similarities[0].flatten() # converts shape from (1, __) to (__, 1)

# shape (articles, embedding_dim = 384)

# title_embeddings = model.encode(article_titles, batch_size=100)
# body_content_embeddings = model.encode(articles_body_content, batch_size=100)


# now the article's body content is a vector where similar texts will have vectors close together

# title_normalized = np.linalg.norm(title_embeddings, axis=1, keepdims=True)
# body_content_normalized = np.linalg.norm(body_content_embeddings, axis=1, keepdims=True)


# df['embedded_title'] = df['cleaned_title'].apply(lambda x: model.encode(x))
# df['embedded_bodyContent'] = df['cleaned_bodyContent'].apply(lambda x: model.encode(x))


# df_first10000 = df.loc[:9999]

# df_first10['embedded_title'] = df_first10['cleaned_title'].apply(lambda x: model.encode(x))
# print('apply embeddings to titles')

# title_embeddings = np.vstack(df_first10['embedded_title'].values)
# similarities = cosine_similarity([user_input_embedding], title_embeddings)
# print('used cosine similarities with body content')



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