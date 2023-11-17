# BigBasket-Search-AI-Using-Astra-DB
This repository contains the implementation of a simple AI model which first creates the embeddings of a large dataset, stores it into a vector database, and then makes search queries on the stored data


## Implementation Details

### Step 1 : Create Embeddings

The embeddings are created using the [OpenAI API](https://platform.openai.com/docs/api-reference). The free version of OpenAI API
allows to create embeddings for a limited number of inputs. 
Hence, in the current code, only a limited number of entries are used from the dataset (specified by the variable named `num_entries`). However, this can be increased further as per the user's demands.
