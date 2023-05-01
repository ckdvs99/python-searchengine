import os.path
import requests
import pandas as pd
import redis

from download import download_wikipedia_abstracts
from load import load_documents
from search.timing import timing
from search.index import Index


@timing
def index_documents(documents, index):
    index.index_documents(documents)
    return index


if __name__ == '__main__':
    index_key = 'index'

    r = redis.Redis(host='localhost', port=6379, db=0)

    if not r.exists(index_key):
        if not os.path.exists('data/enwiki-latest-abstract.xml.gz'):
            download_wikipedia_abstracts()

        index = Index()
        index_documents(load_documents(), index)
        r.set(index_key, index.serialize())
        print(f'Index saved to Redis with key {index_key}')
    else:
        index = Index.deserialize(r.get(index_key))
        print(f'Index loaded from Redis with key {index_key}')

    print(f'Index contains {len(index.documents)} documents')

    # Prepare an empty DataFrame to store the results
    results_df = pd.DataFrame(columns=['Query', 'Search Type', 'Rank', 'Title', 'Relevance Score'])

    # Collect multiple search queries
    while True:
        search_query = input("Please enter your search query (or type 'exit' to finish): ")
        if search_query.strip().lower() == 'exit':
            break

        search_type = input("Enter search type (AND or OR): ").strip().upper()

        if search_type not in ('AND', 'OR'):
            print("Invalid search type. Please enter 'AND' or 'OR'.")
            continue

        results = index.search(search_query, search_type=search_type, rank=True)

        # Store the top 10 results in the DataFrame
        for idx, (document, score) in enumerate(results[:10]):
            results_df = results_df.append({
                'Query': search_query,
                'Search Type': search_type,
                'Rank': idx + 1,
                'Title': document.title,
                'Relevance Score': score
            }, ignore_index=True)

    # Save the results DataFrame to an Excel file
    excel_file = 'search_results.xlsx'
    results_df.to_excel(excel_file, index=False, engine='openpyxl')
    print(f"Results saved to {excel_file}")
