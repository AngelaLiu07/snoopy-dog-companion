import chromadb
from ollama import embed

client = chromadb.PersistentClient(path = "./my_chroma_data")
coll = client.get_or_create_collection(name='snoopy_images')

def search_snoopy_images(user_query: str, top_n : int = 1):
    '''
    embed the user query and search ChromaDB for nearest matches
    '''
    # using nomic-embed-text model, get the embedding for the user query
    query_response = embed(model='nomic-embed-text', input = user_query)
    # query the image collection and perform similarity search
    search_results = coll.query(
        query_embeddings=query_response.embeddings, 
        n_results = top_n)

    best_match = {
        'filepath': search_results['ids'][0][0],
        'distance' : search_results['distances'][0][0],
        'title': search_results['metadatas'][0][0].get('title'),
        'keywords': search_results['metadatas'][0][0].get('keywords')
    }
    return best_match

