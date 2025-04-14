import bs4
import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents.base import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM
from langchain_text_splitters import RecursiveCharacterTextSplitter
from markdownify import markdownify as md

template = """
You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer the question.
If you don't know the answer, just say that you don't know.
Use five sentences maximum and keep the answer concise.

Question: {question}
Context: {context}
Answer:
"""

model = OllamaLLM(model="llama3.2", base_url="http://localhost:11434")
embedding = OllamaEmbeddings(model="llama3.2", base_url="http://localhost:11434")
vector_store = InMemoryVectorStore(embedding=embedding)


def load_page(url: str) -> list[Document]:
    """
    Load a web page from the given URL, convert HTML content to markdown.

    Args:
        url (str): The URL of the web page to load.

    Returns:
        list: A list of documents with markdown content.
    """
    # Load the page using WebBaseLoader
    loader = WebBaseLoader(web_path=url)
    documents = loader.load()

    # Convert HTML to markdown for each document
    for doc in documents:
        html_content = doc.page_content
        soup = bs4.BeautifulSoup(html_content, "html.parser")
        markdown_text = md(str(soup))
        doc.page_content = markdown_text

    return documents


def split_text(documents: list[Document]) -> list[Document]:
    """
    Split the text into smaller chunks.

    Args:
        documents (list): A list of documents to split.

    Returns:
        list[Document]: A list of smaller text chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True,
    )
    return text_splitter.split_documents(documents)


def index_docs(documents: list[Document], vectorstore: InMemoryVectorStore) -> None:
    """
    Index the documents into the vector store.

    Args:
        documents (list[Document]): A list of documents to index.
        vectorstore (InMemoryVectorStore): The vector store to index the documents into.
    """
    vectorstore.add_documents(documents)


def retrieve_docs(query: str, vectorstore: InMemoryVectorStore, k: int = 4) -> list[Document]:
    """
    Retrieve documents from the vector store based on the query.

    Args:
        query (str): The query to search for.
        vectorstore (InMemoryVectorStore): The vector store to search in.
        k (int): The number of documents to retrieve.

    Returns:
        list[Document]: A list of retrieved documents.
    """
    return vectorstore.similarity_search(query, k=k)


def answer_question(query: str, context: str) -> str:
    """
    Answer a question using the context and language model.

    Args:
        query (str): The question to answer.
        context (str): The retrieved context to use for answering.

    Returns:
        str: The answer to the question.
    """
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    return chain.invoke(
        {
            "question": query,
            "context": context,
        }
    )


def streamlit_app() -> None:
    """
    Streamlit application to load a web page, split text, and answer questions.
    """
    st.title("AI Crawler")

    # Initialize session state for chat history if it doesn't exist
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Initialize session state to track if documents are indexed
    if "docs_indexed" not in st.session_state:
        st.session_state.docs_indexed = False

    url = st.text_input("Enter URL to crawl:")

    if url and not st.session_state.docs_indexed:
        with st.spinner("Loading and processing webpage content..."):
            # Load the web page content
            documents = load_page(url)

            # Split the content into smaller chunks
            chunked_documents = split_text(documents)

            # Index the documents into the vector store
            index_docs(chunked_documents, vector_store)
            st.session_state.docs_indexed = True
            st.success("Documents indexed successfully.")

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Get new user input
    if query := st.chat_input("Ask a question about the webpage:"):
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": query})

        # Display user message
        with st.chat_message("user"):
            st.write(query)

        if st.session_state.docs_indexed:
            # Display assistant response with a spinner
            with st.chat_message("assistant"), st.spinner("Thinking..."):
                # Retrieve relevant documents based on the query
                retrieved_docs = retrieve_docs(query=query, vectorstore=vector_store)

                # Build the context from the retrieved documents
                context = "\n\n".join([doc.page_content for doc in retrieved_docs])

                # Answer the question using the question and context
                answer = answer_question(query=query, context=context)

                # Display the answer
                st.write(answer)

                # Add assistant response to chat history
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
        else:
            with st.chat_message("assistant"):
                response = "Please index a webpage first by entering a URL above."
                st.write(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})

    # Add a button to clear the chat history and reset the indexed status
    if st.button("Clear Chat History and Reset Index"):
        st.session_state.chat_history = []
        st.session_state.docs_indexed = False
        st.rerun()  # Updated from st.experimental_rerun()


if __name__ == "__main__":
    # Run the Streamlit app
    streamlit_app()
