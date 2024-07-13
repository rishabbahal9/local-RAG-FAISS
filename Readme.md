# Local RAG with FAISS
## Chat with PDF

This is a simple example of how to use the RAG model with a local FAISS index to chat with a PDF file. 

## How to run the app
1. Python 3.11 is used.
2. Create a virtual environment and install the requirements.
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
3. Install the requirements.
    ```bash
    pip install -r requirements.txt
    ```
4. Create a 'documents' directory if it does not exist and place the PDF file in it. 
5. create a .env file based on .env.example
6. Run the app.
    ```bash
    python main.py
    ```

## Example 
```bash
$ python main.py
Starting the application...
Name of the pdf file: Sample
Creating index...
Index Sample created successfully.
Loading index...
Index Sample loaded successfully.
Type 'exit' to exit the application.
Question: What is React?

React is a language model that integrates decision making and reasoning capabilities. 
It allows for the use of external knowledge sources and generates human-like task-solving
 trajectories that are more interpretable than baselines without reasoning traces. 
 It has been shown to outperform state-of-the-art baselines on various language and 
 decision making tasks, such as question answering and fact verification. It is designed 
 to be intuitive, flexible, and robust, making it suitable for a diverse set of tasks.

Question: exit

$
```

### Tips
1. In name of the pdf file, don't include the extension '.pdf'.
2. To exit the application, type 'exit'.