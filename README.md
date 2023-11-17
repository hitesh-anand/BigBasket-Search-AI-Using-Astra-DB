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


## Execution Details

Executing the code is quite straightforward since there is only one code file. However, there a few important things to do before trying to run the code:

* The dataset should be in the same folder as the code file.
* It is worth noticing that the first 6 lines of the code file have to be filled appropriately with the API Keys and corresponding Authentication tokens from OpenAI and Astra DB. These keys and tokens can be generated only after creating accounts on the respective websites.
* Also, OpenAI free account only allows a limited number of requests and hence, must be utilized judiciously. This limit can be extended by making payments in case it is required by the user.
* [Here](https://youtu.be/yfHHvmaMkcA?si=gr4Xylviuow2vCID), is a nice Youtube tutorial that I referred to while creating accounts on OpenAI, Astra DB and then subsequently generating the keys. Users can refer to the same in case they are stuck.


## Sample Query

Now, moving to the fun part. The following example shows a sample execution of the provided code:

Question: `What household items are available?`

Response: `Home products are available, including pet water bottles made of high-quality plastic which is 100% food grade and BPA free. They come in a variety of attractive colours and are microwave safe (without lid), refrigerator safe, dishwasher safe and can also be used for re-heating food. They also have airtight lids and can be stacked in the kitchen for a look-good factor.`

This is followed by two candidate answers along with their relevance score:

`0.8974"Each product is microwave safe (without lid), refrigerator safe, dishwasher safe and can also be use ..."`

`0.8942"These BB Home pet water bottles are made of high-quality plastic which is 100% food grade and BPA fr ..."`
