import sys, chromadb, openai
from utilities import getconfig
import chromadb.utils.embedding_functions as embedding_functions

openai.api_key = "EMPTY"
openai.base_url = "http://"+getconfig()["fastchat_host"]+":"+getconfig()["fastchat_port"]+"/v1/"
fastchat_model = getconfig()["fastchat_model"]

embedmodel = getconfig()["embedmodel"]
mainmodel = getconfig()["mainmodel"]
chroma = chromadb.HttpClient(host=getconfig()["chroma_host"], port=getconfig()["chroma_port"])
collection = chroma.get_or_create_collection("buildragwithpython")

ollama_ef = embedding_functions.OllamaEmbeddingFunction(
    url="http://"+getconfig()["ollama_host"]+":"+getconfig()["ollama_port"]+"/api/embeddings",
    model_name=embedmodel,
)

query = " ".join(sys.argv[1:])
queryembed = ollama_ef(query)

relevantdocs = collection.query(query_embeddings=[queryembed[0]], n_results=10)["documents"][0]
docs = "\n\n".join(relevantdocs)
modelquery = f"{query} - Answer that question using the following text as a resource: {docs}"

completion = openai.chat.completions.create(
  model=fastchat_model,
  messages=[
      {"role": "user", "content": modelquery}
      ]
)

print(completion.choices[0].message.content)