# Simple similarity search service
### Performing the cosine similarity search for a given query in a knowledge base

## Strategy
The [whitepaper](https://services.google.com/fh/files/misc/ai_adoption_framework_whitepaper.pdf) which forms the initial knowledge base is split semantically using `langchain.SemanticChunker`.  
It is light-cleaned before the partition and then divided by sentences (not simply by sentences, but rather by a semantic group of 1-3 sentences )

## API
### `POST` `/kb`
**Description**: parse & process given file, create embeddings and upsert vectors to the knowledge base
**Body**:
```json
{
    "filepath": "<file_url_or_local_path>",
    "start_page": "<integer>"
}
```
___
### `GET` `/kb`
**Description**: parse & process given file, create embeddings and upsert vectors in the Pinecone
**Query params**:
```text
q=<query>
top_n=<integer> (default: 2)
page_number=<integer> (optional, for filtering)
```
**Response**:
```json
[
  {
    "id": "<str>",
    "sentence": "<str>",
    "page_number": "<int>",
    "score": "<float>"
  },
  ...
]
```
___
### `DELETE` `/kb`
**Description**: Truncate the knowledge base completely
___
### `GET` `/health`
**Description**: Check service status

## Setup & run
Create `.env` file from `.env.example` populating required fields
   - `OPENAPI_KEY` - you need to create an API Key in the [OpenAI Platform](https://platform.openai.com/settings/organization/api-keys)
   - `PINECONE_KEY` - you need to create an account in the [Pinecone](https://app.pinecone.io/) 
   - `PINECONE_IDX` - you can pre-create a Pinecone index or let the service do it automatically
     - Index configuration for manual creation:
       ```
       metric: cosine
       embedding_model: text-embedding-ada-002
       ```

### Local
Prerequisites:
- Python `3.12` + `venv` module
- `make`
- `docker`

Run in-place:
1. `make init-environment`
2. `make run-server-local`
3. use `http://localhost:8080` or `http://127.0.0.1:8080` to access the API

Run in Docker:
1. `run-server-docker`
2. use `http://localhost:8080` or `http://127.0.0.1:8080` to access the API

If you face any issues building the image you could use ready Docker Hub image:  
`docker run --rm --name simapi --env-file .env -p "8080:8080" garkling/similarity-service:1.0.0`


### K8S Cluster
Prerequisites:
- `make`
- `docker`
- `minikube`

Run:
1. `make create-cluster`
2. `make run-server-cluster`
3. `make run-cluster-proxy`
4. copy the provided IP from your terminal and use it to access the API
5. `make delete-cluster`

### Note: regardless of the running environment, the service will automatically parse and store the initial whitepaper on the startup, so no need to call `POST /kb` for this file

## Terraform plan for GCP (GKE)
- `make deployment-plan`
