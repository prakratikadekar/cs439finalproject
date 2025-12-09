import pandas as pd
from sentence_transformers import SentenceTransformer
import re
import numpy as np
import kaggle
import time 
import os


def download_data():
        # could not push this in github so this is how we can get the filtered dataset
        kaggle.api.dataset_download_files (
            'prakratikadekar/guardian-filtered',
            path='data/',
            unzip=True
        )

        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_colwidth', None)

        return 'data/guardian_filtered.csv'



model = SentenceTransformer('all-MiniLM-L6-v2')
df = pd.read_csv(download_data())



# ----------- STEP 1: Filter dataset for just political and computer science/technology topics ---------------------------------------

# original df: https://www.kaggle.com/datasets/adityakharosekar2/guardian-news-articles aka data/guardian_articles.csv
# filtered df: data/guardian_filtered.csv 


def remove_whitespace(col_data):
    col_data = re.sub(r'<.*?>', '', col_data) # removes HTML
    col_data = re.sub(r'\s+', ' ', col_data) # removes extra whitespace
    return col_data.lower()
    # print('cleaned data')



def filter_df():

    df = 'data/guardian_articles.csv'

    sections_to_keep = [
        "US news",
        "World news",
        "News",
        "Australia news",
        "UK news",
        "Politics",
        "Technology"
    ]

    cleaned_section = clean_data()[2]

    filtered_news = df[cleaned_section].isin(sections_to_keep)
    filtered_news = filtered_news.reset_index(drop=True)

    filtered_news.to_csv('guardian_filtered.csv', index=False)

    # filtered dataset that was obtained from original 




    # ----------- STEP 2: Read dataset and convert the data columns of title and body content into strings ---------------------------------------

def clean_data():
         
    df['bodyContent'] = df['bodyContent'].astype(str)
    df['webTitle'] = df['webTitle'].astype(str)
    df['sectionName'] = df['sectionName'].astype(str)

    # ----------- STEP 3: Clean dataset to get rid of extra HTML from kaggle + extra whitespace  ---------------------------------------


    df['cleaned_bodyContent'] = df['bodyContent'].apply(remove_whitespace)
    df['cleaned_title'] = df['webTitle'].apply(remove_whitespace)
    df['cleaned_section'] = df['sectionName'].apply(remove_whitespace)

    return df['cleaned_title'], df['cleaned_bodyContent'], df['sectionName']



    
#    ----------- STEP 4: Use the Sentence Transformer model to encode both the titles and body content of articles with sentiment values (384 dimensional vector). This is a pretrained model  ---------------------------------------

# model documentation: https://sbert.net/examples/sentence_transformer/applications/computing-embeddings/README.html

def sentence_transformer():
    clean_titles, clean_body_content = clean_data()
    news_content = clean_titles + " " + clean_body_content
    news_embeddings = model.encode(news_content.tolist(), batch_size=100)
    print('model has been applied')


    # ----------- STEP 5: After running above code once, saved it to an npy file so we do not need to rerun again - these are our news embeddings  ---------------------------------------

    np.save('news_embeddings.npy', news_embeddings)
    print('shape of news embeddings', news_embeddings.shape)




# ----------- STEP 6: Cosine similarity: use the embeddings of user input and news data to find which articles are similar to  ---------------------------------------
# ----------- STEP 7: Gather highest 3 cosine similarities of input and embedding data ---------------------------------------
# ----------- STEP 8: Write the articles in the txt file ---------------------------------------

def get_top_news_matches(user_input): 
    user_input_embedding = model.encode(user_input)

    news_embeddings = np.load('news_embeddings.npy')


    user_input_embedding = np.atleast_2d(user_input_embedding)
    user_input_normalized = user_input_embedding / np.linalg.norm(user_input_embedding, axis=1, keepdims=True)

    news_embeddings_normalized = news_embeddings / np.linalg.norm(news_embeddings, axis=1, keepdims=True) # 1 dimension across all articles (rows)

    similarities = np.dot(user_input_normalized, news_embeddings_normalized.T)
    
    # get index for the 3 highest similarities in relation to news embeddings
    # order from greatest to least similarity
    best_matches = np.argsort(similarities[0])[-3:][::-1] # indices of top 3 largest similarities from cosine
    # print('best matches shape: ', best_matches.shape)

    top_similarities = similarities[0][best_matches]
    # print(top_similarities)
    valid_matches = []

    for match, similarity in zip(best_matches, top_similarities):
        if similarity >= 0.4:
            valid_matches.append(match)


    recommended_guardian_articles = df.iloc[valid_matches]

    with open('recommended_news.txt', 'a', encoding='utf-8') as file: 
        file.write('\n\nNEW RUN:\n')
        file.write(recommended_guardian_articles[['sectionName', 'webTitle', 'webUrl']].to_string())

    final_recommendation = []


    # this is how it best displays on the website

    for _, row in recommended_guardian_articles.iterrows():
        article_dict = {
            'title': str(row['webTitle']) if pd.notna(row['webTitle']) else 'Unknown Title',
            'description': str(row['sectionName']) if pd.notna(row['sectionName']) else 'News',
            'url': str(row['webUrl']) if pd.notna(row['webUrl']) else '',
        }
        final_recommendation.append(article_dict)

    return final_recommendation



# main:
get_top_news_matches('trump')
 











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