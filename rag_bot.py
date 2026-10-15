from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma


documents = [
    Document(page_content="""
    The Payment API processes card payments.
    A successful payment returns HTTP 200.
    """, metadata={"module": "Payment"}),

    Document(page_content="""
    If payment processing fails because of a
    server error, the API can return HTTP 500.
    Test the server failure scenario.
    """, metadata={"module": "Payment"}),

    Document(page_content="""
    Invalid login credentials return HTTP 401.
    Verify that unauthenticated requests are rejected.
    """, metadata={"module": "Authentication"}),

    Document(page_content="""
    Refund requests must be tested after successful
    payments. Verify refund status and transaction amount.
    """, metadata={"module": "Payment"})
]


splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

chunks = splitter.split_documents(documents)

print("Number of chunks:", len(chunks))


embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name="qa_knowledge",
    persist_directory="./chroma_db"
)

print("Documents indexed successfully!")


retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)

llm = ChatOpenAI(model="gpt-4o-mini")


def ask_question(question):
    docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    prompt = f"""
    You are a QA testing assistant.

    Answer the question using only the
    context provided below.

    If the answer is not present in the
    context, say you do not have enough
    information.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    response = llm.invoke(prompt)
    return response.content


while True:
    question = input("\nAsk a QA question (or type exit): ")

    if question.lower() == "exit":
        break

    print("\nAnswer:", ask_question(question))
