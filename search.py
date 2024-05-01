import ollama, sys, chromadb
from utilities import getconfig
import chromadb.utils.embedding_functions as embedding_functions

embedmodel = getconfig()["embedmodel"]
mainmodel = getconfig()["mainmodel"]
chroma = chromadb.HttpClient(host="localhost", port=8000)
collection = chroma.get_or_create_collection("buildragwithpython")

ollama_ef = embedding_functions.OllamaEmbeddingFunction(
    url="http://localhost:11434/api/embeddings",
    model_name=embedmodel,
)

query = " ".join(sys.argv[1:])
#queryembed = ollama.embeddings(model=embedmodel, prompt=query)['embedding']
queryembed = ollama_ef(query)

relevantdocs = collection.query(query_embeddings=[queryembed[0]], n_results=10)["documents"][0]
docs = "\n\n".join(relevantdocs)
modelquery = f"{query} - Answer that question using the following text as a resource: {docs}"

stream = ollama.generate(model=mainmodel, prompt=modelquery, stream=True)

for chunk in stream:
  if chunk["response"]:
    print(chunk['response'], end='', flush=True)
