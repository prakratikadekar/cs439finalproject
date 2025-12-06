from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
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

    book_embedding_normalized = book_embedding / np.linalg.norm(book_embedding, axis=1, keepdims=True)

    similarities = np.dot(user_input_normalized, book_embedding_normalized.T)

    top_matches = np.argsort(similarities[0])[-3:][::-1]

    # top_matches_embeddings = book_embedding_normalized[top_matches]

    # kmeans = KMeans(3).fit(top_matches_embeddings)
    # clusters = kmeans.labels_

    # recommendation_list = []

    # for i in range(3):
    #     books_in_cluster_i = np.where(clusters == i)[0]
    #     top_match_cluster_embeddings = top_matches_embeddings[books_in_cluster_i]
    #     cosine_similarity = np.dot(user_input_normalized, top_match_cluster_embeddings.T)
    #     most_similar_in_cluster = books_in_cluster_i[np.argmax(cosine_similarity)]
    #     recommendation_list.append(top_matches[most_similar_in_cluster])
    
    recommended = df.iloc[top_matches]

    # with open('recommended_books.txt', 'a', encoding='utf-8') as file: 
    #     file.write('\n\nNEW RUN:\n')
    #     file.write(recommended[['Title', 'Authors', 'ISBN-10', 'ISBN-13', 'Description']].to_string())

    final_recommendations = []
 
    for _, row in recommended.iterrows():
        book_dict = {
            'title': str(row['Title']) if pd.notna(row['Title']) else 'Unknown Title',
            'author': str(row['Authors']) if pd.notna(row['Authors']) else 'Unknown Author',
            'isbn10': str(row['ISBN-10']) if pd.notna(row['ISBN-10']) else '',
            'isbn13': str(row['ISBN-13']) if pd.notna(row['ISBN-13']) else '',
            'description': str(row['Description']) if pd.notna(row['Description']) else 'No Description Provided'
        }
        final_recommendations.append(book_dict)
    return final_recommendations

def main():
    if not os.path.exists("book_embedding.npy"):
        create_embeddings()

df = pd.read_csv('data/book_data.csv', sep = '\t', encoding = 'utf-8')
model = SentenceTransformer("all-MiniLM-L6-v2")

if __name__ == '__main__':
    main()