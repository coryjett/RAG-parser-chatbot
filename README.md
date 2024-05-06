# RAG-parser-chatbot


## Install and run ChromaDB

ChromaDB is used as a database to store embeddings.

https://www.trychroma.com/

`pip install chromadb`

`chroma.exe run --host IP_ADDR --port 8001 --path ./my_chroma_data`


## Install and run Fastchat

Fastchat provides a scalable controller/worker model and API for serving LLM based chatbots.

https://github.com/lm-sys/FastChat

`pip3 install "fschat[model_worker,webui]"`

`python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121`

`python3 -m fastchat.serve.controller`

`python3 -m fastchat.serve.model_worker --model-path lmsys/vicuna-7b-v1.5`

`python -m fastchat.serve.openai_api_server --host IP_ADDR --port 8000`


## Install and run Ollama

Ollama provies an API that is used to generate embeddings.

https://ollama.com/

If on Windows: Install VSbuildtools [link to instructions](https://github.com/bycloudai/InstallVSBuildToolsWindows)

`$env:OLLAMA_HOST="0.0.0.0"`

`ollama serve`


## Edit config.ini

Modify models, hosts, ports, and the embedding collection to the appropriate values.


## Add files and URLs

Some sample docs and URLs have been pre-added

Add/remove files to/from `/scripts`, or reference another location in `config.ini` for `files_path`

Add/remove URLs to/from `sourcedocs.txt`


## Run the importer

This will run continually and pick up new changes.

`python3 import.py`


## Run the search engine

`python3 search.py "query"`

eg. `python3 search.py "How are models stored on the filesystem?  Explain in detail."`