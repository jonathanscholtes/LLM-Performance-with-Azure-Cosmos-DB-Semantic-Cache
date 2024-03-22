from os import environ
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.cache import AzureCosmosDBSemanticCache
from langchain_community.vectorstores.azure_cosmos_db import (
    CosmosDBSimilarityType,
    CosmosDBVectorSearchType,
)
from langchain.globals import set_llm_cache
from langchain_openai import ChatOpenAI
import time

load_dotenv(override=True)

#variable from '.env' file
MONGO_CONNECTION_STRING = environ.get("MONGO_CONNECTION_STRING")
DB_NAME = "research"
COLLECTION_NAME = "resources"

llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k", temperature=0)
set_llm_cache(AzureCosmosDBSemanticCache(
        cosmosdb_connection_string=MONGO_CONNECTION_STRING,
        cosmosdb_client=None,
        embedding=OpenAIEmbeddings(),
        database_name=DB_NAME,
        collection_name=DB_NAME+'_CACHE',
        num_lists=1, #for a small demo, you can start with numLists set to 1 to perform a brute-force search across all vectors.,
        similarity=CosmosDBSimilarityType.COS,
        kind=CosmosDBVectorSearchType.VECTOR_IVF,
        dimensions=1536,
        m=16,
        ef_construction=64,
        ef_search=40,
        score_threshold=.99))



query = "speed of light"



start_time = time.time()
#the first query it is not yet in cache, so it should take longer
print(llm.invoke(query))

print(f"--- {time.time() - start_time:.2f} seconds ---")

start_time = time.time()
#the second query will use the cache, and will return faster
print(llm.invoke(query))

print(f"--- {time.time() - start_time:.2f} seconds ---")