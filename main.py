import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_astradb import AstraDBVectorStore
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools.retriever import create_retriever_tool
from langchain import hub
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from github import fetch_git_issues
from note import note_tool

MODEL_LLAMA = "llama3.1"
load_dotenv()

def connect_to_vstore():
    ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
    desired_namespace = os.getenv("ASTRA_DB_KEYSPACE")
    ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")

    # embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", api_key=OPENAI_API_KEY)
    embeddings = OllamaEmbeddings(model=MODEL_LLAMA)

    if desired_namespace:
        ASTRA_DB_KEYSPACE = desired_namespace
    else:
        ASTRA_DB_KEYSPACE = None
    
    vstore = AstraDBVectorStore(
        embedding=embeddings,
        collection_name="github_issues",
        api_endpoint=ASTRA_DB_API_ENDPOINT,
        token=ASTRA_DB_APPLICATION_TOKEN,
        namespace=ASTRA_DB_KEYSPACE,
    )

    return vstore

vstore = connect_to_vstore()
add_to_vectorestore = input("Do you want to update the issues? (y/N): ").lower() in ["y", "yes"]

if add_to_vectorestore:
    owner = "facebook"
    repo = "react"
    issues = fetch_git_issues(owner, repo)

    try:
        vstore.delete_collection()
    except:
        pass

    vstore = connect_to_vstore()
    vstore.add_documents(issues)


# Create the retriever tool
retriever = vstore.as_retriever(kwargs={"k": 5})
retriever_tool = create_retriever_tool(
    retriever=retriever,
    name="github_search",
    description="Search for information about github issues. For any questions about github issues, you must use this tool!",
)

# Load the prompt from the hub
prompt = hub.pull("hwchase17/openai-functions-agent", api_key=os.getenv("OPENAI_API_KEY"))

# Create the LLM
llm = Ollama(model=MODEL_LLAMA)

# Define the tools
tools = [retriever_tool, note_tool]

# Create the agent
agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
)

# Create the agent executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
)

while (question := input("Ask a question about github issues (q to quit): ")) != "q":
    result = agent_executor.invoke({"input": question})
    print(result["output"])