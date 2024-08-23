# GenAI Application with LLM and Custom AI Agent

This is a GenAI application that leverages a Large Language Model (LLM) with a custom AI Agent to provide advanced AI functionalities.
This program asks user to type any github issues. Based on the user input, it searches in facebook react repository for the open issue. It uses an agent to perform the operation.
If user asks to add any notes, then it uses another agent. That agent adds the note in notes.txt file.
If the input doesn't match any of the criterias, then no agent is invoked.

## Environment Variables

The application requires the following environment variables to be set in a `.env` file:

```properties
GITHUB_TOKEN=your_github_token
ASTRA_DB_API_ENDPOINT=your_astra_db_api_endpoint
ASTRA_DB_APPLICATION_TOKEN=your_astra_db_application_token
ASTRA_DB_KEYSPACE=your_astra_db_keyspace
OPENAI_API_KEY=your_openai_api_key
```

## Setup AstraDB

To use AstraDB, you need to sign up for an account. You can sign up here: <a href="https://www.datastax.com/">AstraDB Signup</a>.

Once signed up, create a serverless vector database and name it.

Once the database is generated, copy the endpoint and api key into .env.

## Setup OpenAI

Go to https://platform.openai.com/api-keys and generate API key and pase it in .env.

## Setup Ollama

Download and install Ollama locally.