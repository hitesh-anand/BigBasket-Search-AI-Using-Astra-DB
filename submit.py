ASTRA_DB_SECURE_BUNDLE_PATH="C:/Users/anand/Documents/Certificates_ImpDocuments/Placements/chaabi/secure-connect-vector-database.zip"
ASTRA_DB_APPLICATION_TOKEN="AstraCS:OSEtrkhtBFUcGYSzvwoiolJa:1838ff20c56ed3b6e99aa88f9efabeb469002f560b9f8f465b0c320a04e14b79"
ASTRA_DB_CLIENT_ID="OSEtrkhtBFUcGYSzvwoiolJa"
ASTRA_DB_CLIENT_SECRET="ces-.stLCqCAUuGHQ__ZPe4DLDA4nZ-Ox,UbP_0sjZ,5B0.tNfbdd9KYEXqIA,TDoKofzaxykfT+uFSBQ22fY7-GsEKJS90Kma5YZqidr,aPHYu8ZeW0mbtI2LT84Xb_"
ASTRA_DB_KEYSPACE="search"
OPENAI_API_KEY="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"

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
    for doc, score in myCassandraVStore.similarity_search_with_score(query_text, k=2):
        print("%0.4f\"%s ...\"" %(score, doc.page_content[:100]))
 