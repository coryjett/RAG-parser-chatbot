# RAG-parser-chatbot

This is a sample Retrieval Augmented Generation [RAG](https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/) generative AI importer and search application.

**import.py** takes a list of URLs and a directory of documents, generates [embeddings](https://aws.amazon.com/what-is/embeddings-in-machine-learning/) using Ollama, and stores them in ChromaDB.

**search.py** takes a query, generates an embedding of the query using Ollama, and pulles a list of similar information back from ChromaDB where the embeddings are stored (using [cosign](https://docs.trychroma.com/usage-guide#changing-the-distance-function)).  It then takes that information and your original query, and asks the LLM a question (through Fastchat).

![trafficflow.](/Images/trafficflow.png)

## Install and run ChromaDB

ChromaDB is used as a database to store embeddings.

https://www.trychroma.com/

If on Windows: Install VSbuildtools [link to instructions](https://github.com/bycloudai/InstallVSBuildToolsWindows)

`pip install chromadb`

`chroma.exe run --host IP_ADDR --port 8001 --path ./my_chroma_data`


## Install and run Fastchat

Fastchat provides a scalable controller/worker model and API for serving LLM based chatbots.

https://github.com/lm-sys/FastChat

`pip install "fschat[model_worker,webui]"`

`python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121`

`python -m fastchat.serve.controller`

`python -m fastchat.serve.model_worker --model-path lmsys/vicuna-7b-v1.5`

`python -m fastchat.serve.openai_api_server --host IP_ADDR --port 8000`


## Install and run Ollama

Ollama provies an API that is used to generate embeddings.

https://ollama.com/

`ollama pull nomic-embed-text`

`$env:OLLAMA_HOST="0.0.0.0"`

`ollama serve`


## Other pre-run things

### Install libmagic 

Windows: https://github.com/pidydx/libmagicwin64

Mac: `brew install libmagic`

### Nvidia stuff

Check CUDA version: `nvidia-smi`


## Edit ./config.ini

Modify models, hosts, ports, and the embedding collection to the appropriate values.


## Add files and URLs

Some sample docs and URLs have been pre-added

Add/remove files to/from `/scripts`, or reference another location in `config.ini` for `files_path`

Add/remove URLs to/from `sourcedocs.txt`


## Run the importer

This will run continually and pick up new changes.

`python import.py`


## Run the search engine

`python search.py "query"`

eg. `python search.py "How are models stored on the filesystem?  Explain in detail."`
