import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain_text_splitters import CharacterTextSplitter
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain import hub

load_dotenv()


class RAGLocal:
    def __init__(self, pdf_name: str, pdf_path: str):
        self.pdf_name = pdf_name
        self.pdf_path = pdf_path
        self.embeddings = OpenAIEmbeddings()
        self.retrieval_chain = None

    def create_index(self):
        """Creating the index for the RAG model and retriever chain."""
        if os.path.exists(f"indexes/faiss_{self.pdf_name}"):
            should_create = (
                input("Index already exists, you still want to create index?(y/n): ")
                == "y"
            )
            if not should_create:
                return
        loader = PyPDFLoader(file_path=self.pdf_path)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(
            chunk_size=1000, chunk_overlap=30, separator="\n"
        )
        docs = text_splitter.split_documents(documents=documents)

        vectorstore = FAISS.from_documents(docs, self.embeddings)
        vectorstore.save_local(f"indexes/faiss_{self.pdf_name}")

    def load_index(self):
        """Loading existing index for the RAG model."""
        vectorstore = FAISS.load_local(
            f"indexes/faiss_{self.pdf_name}",
            self.embeddings,
            allow_dangerous_deserialization=True,
        )
        retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
        combine_docs_chain = create_stuff_documents_chain(
            OpenAI(), retrieval_qa_chat_prompt
        )
        self.retrieval_chain = create_retrieval_chain(
            vectorstore.as_retriever(), combine_docs_chain
        )

    def ask_question(self, question: str):
        """Ask a question to the RAG model by invoking the retrieval chain."""
        return self.retrieval_chain.invoke({"input": question})


if __name__ == "__main__":
    print("Starting the application...")
    pdf_name_input = input("Name of the pdf file: ")
    pwd = os.getcwd()
    rag = RAGLocal(pdf_name_input, f"{pwd}/documents/{pdf_name_input}.pdf")
    print("Creating index...")
    rag.create_index()
    print(f"Index {pdf_name_input} created successfully.")
    print("Loading index...")
    rag.load_index()
    print(f"Index {pdf_name_input} loaded successfully.")
    print("Type 'exit' to exit the application.")
    if not rag.retrieval_chain:
        print("Index creation failed")
        exit(1)
    while True:
        question_input = input("Question: ")
        if question_input == "exit":
            exit(0)
        res = rag.ask_question(question_input)
        print(res["answer"])
