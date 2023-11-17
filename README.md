# BigBasket-Search-AI-Using-Astra-DB
This repository contains the implementation of a simple AI model which first creates the embeddings of a large dataset, stores it into a vector database, and then makes search queries on the stored data


## Implementation Details

### Step 1 : Create Embeddings

The embeddings are created using the [OpenAI API](https://platform.openai.com/docs/api-reference). The free version of OpenAI API
allows to create embeddings for a limited number of inputs. 
Hence, in the current code, only a limited number of entries are used from the dataset (specified by the variable named `num_entries`). However, this can be increased further as per the user's demands.

### Step 2 : Store the Embeddings

We need a reliable Vector Database to store the resulting vector embeddings generated in the Step 1. I have used [Datastax Astra DB](https://www.datastax.com/) for this purpose since it is highly useful in real-time data integrations and deploying generative AI applications in production. 

### Step 3 : Query the Database

Once we have stored the embeddings, we can make simple queries on the stored data. In my code, I have showed how to do similarity searches. The result consists of two parts: The corresponding answer to the query and the best answer candidates sorted by a relevance score. The number of such candidates can also be tweaked in the code.
