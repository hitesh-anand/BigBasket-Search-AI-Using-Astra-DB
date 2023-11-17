ASTRA_DB_SECURE_BUNDLE_PATH="<ASTRA DP SECURE BUNDLE PATH>"
ASTRA_DB_APPLICATION_TOKEN="<ASTRA DB APPLICATION TOKEN>"
ASTRA_DB_CLIENT_ID="<ASTRA DB CLIENT ID>"
ASTRA_DB_CLIENT_SECRET="<ASTRA DB CLIENT SECRET>"
ASTRA_DB_KEYSPACE="<ASTRA DB KEYSPACE>"
OPENAI_API_KEY="<OPENAI API KEY>"

from langchain.vectorstores.cassandra import Cassandra
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings

import numpy as np
import pandas as pd

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

# Authentication and Establishing Connection
cloud_config = {
    'secure_connect_bundle': ASTRA_DB_SECURE_BUNDLE_PATH
}
auth_provider = PlainTextAuthProvider(ASTRA_DB_CLIENT_ID, ASTRA_DB_CLIENT_SECRET)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
astraSession = cluster.connect()

# Step 1: Create Vector Embeddings
llm = OpenAI(openai_api_key=OPENAI_API_KEY)
myEmbedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

myCassandraVStore = Cassandra(
    embedding=myEmbedding,
    session=astraSession,
    keyspace=ASTRA_DB_KEYSPACE,
    table_name='qa_mini_demo',
)

# Step 2: Store the Embeddings
df = pd.read_csv('bigBasketProducts.csv')
df['description'] = df['description'].astype(str)

# Number of entries (rows) to be inserted
num_entries = 100
values = df['description'].values[:num_entries]
# print(values[:5])

myCassandraVStore.add_texts(values)

print(f'Inserted {len(values)} lines')

vectorIndex = VectorStoreIndexWrapper(vectorstore=myCassandraVStore)

# Perform Queries
first_qn = True
while True:
    if first_qn:
        query_text = input("\nEnter your question (or type 'quit' to exit): ")
        first_qn = False
    else:
        query_text = input("\nWhat's your next question (or type 'quit' to exit): ")

    if query_text.lower()=='quit':
        break

    print("Question: \%s\""%query_text)
    answer = vectorIndex.query(query_text, llm=llm).strip()
    print("Answer: \%s\"\n"%answer)

    print("Entries by Relevance:")
    for doc, score in myCassandraVStore.similarity_search_with_score(query_text, k=4):
        print("%0.4f\"%s ...\"" %(score, doc.page_content[:100]))
        
