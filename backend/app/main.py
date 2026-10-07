from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .llm_service import generate_answer
from .search_service import search_documents
from .pdf_service import extract_pages_from_pdf
from .chunk_service import chunk_pdf_pages
from .embedding_service import create_embeddings
from .faiss_service import create_faiss_index
from .vector_store import save_vector_store
from .database import get_db
from .models import User, Document, ChatHistory
from .pdf_service import extract_pages_from_pdf
from .chunk_service import chunk_pdf_pages
from .schemas import UserCreate, UserLogin
from .auth import verify_password, create_access_token
from .auth import verify_password, create_access_token, get_current_user
from pwdlib import PasswordHash
from fastapi import UploadFile, File
import os
import shutil

app = FastAPI(title="Documentation AI Assistant")

password_hash = PasswordHash.recommended()


@app.get("/health")
def health_check():
    return {
        "status": "success",
        "message": "Documentation AI Backend is running"
    }


@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()

    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at
        }
        for user in users
    ]


@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = password_hash.hash(user.password)

    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id,
        "name": new_user.name,
        "email": new_user.email
    }

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        user.password,
        existing_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(existing_user.id)

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.get("/profile")
def profile(current_user_id: int = Depends(get_current_user)):
    return {
        "message": "You are authenticated!",
        "user_id": current_user_id
    }


@app.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    current_user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    upload_folder = "uploads"

    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(
        upload_folder,
        file.filename
    )

    # Save PDF
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract pages
    pages = extract_pages_from_pdf(file_path)

    # Create chunks
    chunks = chunk_pdf_pages(pages)

    # Save document information in MySQL
    document = Document(
        user_id=current_user_id,
        filename=file.filename,
        file_path=file_path
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    # Add document information to every chunk
    for chunk in chunks:
        chunk["filename"] = file.filename
        chunk["document_id"] = document.id

    # Create embeddings
    embeddings = create_embeddings(chunks)

    # Create FAISS index
    index = create_faiss_index(embeddings)

    # Save FAISS index + metadata
    save_vector_store(
    current_user_id,
    index,
    chunks
)

    return {
        "message": "Document uploaded and indexed successfully",
        "document_id": document.id,
        "filename": file.filename,
        "page_count": len(pages),
        "chunk_count": len(chunks)
    }



@app.get("/search")
def search(
    question: str,
    current_user_id: int = Depends(get_current_user)
):
    results = search_documents(question)

    return {
        "question": question,
        "results": results
    }

@app.get("/ask")
def ask(
    question: str,
    current_user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    results = search_documents(
    current_user_id,
    question
)

    if not results:
        answer = "I couldn't find this information in the provided documents."

        chat = ChatHistory(
            user_id=current_user_id,
            question=question,
            answer=answer
        )

        db.add(chat)
        db.commit()

        return {
            "question": question,
            "answer": answer,
            "sources": []
        }

    context = ""

    for result in results:
        context += (
            f"File: {result['filename']}\n"
            f"Page: {result['page']}\n"
            f"Content: {result['text']}\n\n"
        )

    answer = generate_answer(
        question,
        context
    )

    sources = []

    for result in results:
        sources.append({
            "filename": result["filename"],
        "page": result["page"]
        })

    chat = ChatHistory(
        user_id=current_user_id,
        question=question,
        answer=answer
    )

    db.add(chat)
    db.commit()

    return {
        "question": question,
        "answer": answer,
        "sources": sources
    }



@app.get("/history")
def get_history(
    current_user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    history = (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == current_user_id)
        .order_by(ChatHistory.id.desc())
        .all()
    )

    return {
        "history": [
            {
                "id": chat.id,
                "question": chat.question,
                "answer": chat.answer,
                "created_at": chat.created_at
            }
            for chat in history
        ]
    }


@app.get("/test-llm")
def test_llm():

    answer = generate_answer(
        "What programming language is mentioned?",
        "The student knows Java and Python."
    )

    return {
        "answer": answer
    }