from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np
import os

def create_embeddings():
    df['Title'] = df['Title'].fillna('')
    df['Subjects'] = df['Subjects'].fillna('')
    df['Description'] = df['Description'].fillna('')

    df['Combined_For_Embedding'] = df['Title'] + ' | ' + df['Subjects'] + ' | ' + df['Description']

    print("Creating Embeddings")
    embedding = model.encode(df['Combined_For_Embedding'].to_list(), batch_size = 100, show_progress_bar = True)
    print("Finish Creating Embeddings")

    np.save('book_embedding.npy', embedding)

    return embedding

def get_top_3_book_groups(user_input):
    user_input_embedding = model.encode(user_input)

    book_embedding = np.load('book_embedding.npy')


    user_input_embedding = np.atleast_2d(user_input_embedding)
    user_input_normalized = user_input_embedding / np.linalg.norm(user_input_embedding, axis=1, keepdims=True)

    book_embedding_normalized = book_embedding / np.linalg.norm(book_embedding, axis=1, keepdims=True) # column -> 1 dimension across all articles (rows)

    similarities = np.dot(user_input_normalized, book_embedding_normalized.T)

    best_matches = np.argsort(similarities[0])[-5:][::-1] # indices of top 3 largest similarities from cosine
    # print('best matches shape: ', best_matches.shape)

    recommended = df.iloc[best_matches]

    with open('recommended_books.txt', 'a', encoding='utf-8') as file: 
        file.write('\n\nNEW RUN:\n')
        file.write(recommended[['Title', 'Authors', 'ISBN-10', 'ISBN-13', 'Description']].to_string())



def main():
    if not os.path.exists("book_embedding.npy"):
        create_embeddings()
    user_input = "Clustering Algorithms"
    get_top_3_book_groups(user_input)

df = pd.read_csv('book_data.csv', sep = '\t', encoding = 'utf-8')
model = SentenceTransformer("all-MiniLM-L6-v2")
main()