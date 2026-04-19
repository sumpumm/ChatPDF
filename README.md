# PDF Chat Application

This project is a PDF-based chat application built with FastAPI for the backend and Streamlit for the user interface. It allows users to upload PDF files, interact with their content through a chat interface, and manage user authentication with token-based login/logout functionality.

## Features

- **User Authentication**:
  - Token-based login and logout system.
- **PDF Upload**:
  - Upload PDF files for processing and interaction.
- **Chat with PDF**:
  - Query and interact with the content of uploaded PDFs.
- **Chat History**:
  - Retrieve and display chat history for a session.
- **Streamlit UI**:
  - User-friendly interface for interacting with the application.

## Technologies Used

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Authentication**: JWT (JSON Web Tokens)
- **Server**: Uvicorn
- **LangChain**: For managing and chaining LLM-based workflows.
- **Ollama**: For running and interacting with local language models.
