# QA RAG Chatbot

A small command-line chatbot that answers QA testing questions from a fictional knowledge base. It retrieves relevant notes with Chroma, then asks `gpt-4o-mini` to answer using only that context

The knowledge base covers card payments, authentication failures, and refunds. Questions outside those notes should get a reply that there is not enough information

## Requirements

- Python 3.10 or newer
- An OpenAI API key with billing enabled

Packages are listed in `requirements.txt`:

- `langchain-core`
- `langchain-openai`
- `langchain-chroma`
- `langchain-text-splitters`

## Setup (Windows PowerShell)

1. Open this folder in VS Code.
2. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install the packages:

   ```powershell
   pip install -r requirements.txt
   ```

4. Set your API key for the current PowerShell session. Keep the key out of Git:

   ```powershell
   $env:OPENAI_API_KEY="your-api-key"
   ```

5. Start the chatbot:

   ```powershell
   python rag_bot.py
   ```

6. Type a question at the prompt. Type `exit` to stop.

The first run creates a local `chroma_db` directory and indexes the documents into the `qa_knowledge` collection.

## Try these questions

- What payment failure scenarios should I test?
- What HTTP status code is returned for invalid login?
- What should I verify when testing refunds?
- What is the timeout value for the Payment API?

The timeout question is outside the knowledge base. The prompt tells the model to say when the context does not contain the answer. That instruction reduces unsupported answers; it does not make them impossible.

## Knowledge base

`rag_bot.py` embeds four short notes:

| Module | What it covers |
| --- | --- |
| Payment | Card payments succeed with HTTP 200. A server error can return HTTP 500, and that failure path should be tested. |
| Authentication | Invalid login credentials return HTTP 401. Unauthenticated requests should be rejected. |
| Payment | Refunds are tested after a successful payment. Check refund status and transaction amount. |

## How it works

1. Load the four source documents.
2. Split them with `RecursiveCharacterTextSplitter` (`chunk_size=300`, `chunk_overlap=50`).
3. Embed the chunks with OpenAI `text-embedding-3-small`.
4. Store the vectors and text in Chroma (`./chroma_db`, collection `qa_knowledge`).
5. For each question, retrieve the top 3 chunks.
6. Send those chunks and the question to `gpt-4o-mini` with a QA-assistant prompt that limits answers to the retrieved context.
7. Print the model reply.

## Project layout

```text
rag_bot.py          Chatbot script
requirements.txt    Python packages
chroma_db/          Local vector store, created on first run
```

## Notes

- Embedding and chat calls go to OpenAI and can incur charges.
- The vector store is local. Delete `chroma_db` if you change the source documents and want a fresh index.
- This is a learning prototype, with a hardcoded knowledge base and no conversation memory.
