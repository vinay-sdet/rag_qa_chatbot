# QA RAG Chatbot

This is a beginner-friendly RAG chatbot based on the code in the copied tutorial. It answers questions using a small, fictional QA knowledge base about payment, authentication, and refunds.

## Requirements

- Python 3.10 or newer recommended
- An OpenAI API key with API access and billing configured

## Setup in VS Code (Windows PowerShell)

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

4. Set your API key for the current PowerShell session. Replace the placeholder with your key; do not commit the key to Git:

   ```powershell
   $env:OPENAI_API_KEY="your-api-key"
   ```

5. Run the chatbot:

   ```powershell
   python rag_bot.py
   ```

6. Ask a question. Type `exit` to stop.

## Try these questions

- What payment failure scenarios should I test?
- What HTTP status code is returned for invalid login?
- What should I verify when testing refunds?
- What is the timeout value for the Payment API?

The last question is not covered by the supplied documents. The prompt asks the model to say when there is not enough information, but this instruction cannot guarantee that the model will never produce an unsupported answer.

## How it works

1. Define the source documents.
2. Split documents into chunks.
3. Generate embeddings.
4. Store the vectors and document text in ChromaDB.
5. Retrieve up to three relevant chunks for a question.
6. Pass the question and retrieved context to the chat model.
7. Print the generated answer.

## Notes

- This example calls hosted OpenAI embedding and chat models, so API usage may incur charges.
- The code creates/uses a local `chroma_db` directory.
- This is a learning prototype, not a production-ready chatbot.
