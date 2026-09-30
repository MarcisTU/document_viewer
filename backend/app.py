from typing import List

from fastapi import FastAPI, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import select

from models.db import Document, DocumentPublic
from dependencies.database import SessionDependency


app = FastAPI(
    title="XML dokumentu serviss",
    description="Backend risinājums XML dokumentu ielādei un izgūšanai.",
    version="1.0.0",
    contact={
        "name": "Mārcis Upenieks",
        "email": "marcisreb@gmail.com",
    },
)

# Lai frontend risinājums varētu sasniegt un piekļūt backend API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/api/v1/documents",
    status_code=status.HTTP_200_OK,
    response_model=List[DocumentPublic],
    description="Get all documents. Supports pagination, so will return 10 documents by default with offset 0."
)
async def get_documents(
    session: SessionDependency,
    limit: int = Query(default=10, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
):
    statement = (
        select(Document)
        .offset(offset)
        .limit(limit)
    )

    result = await session.exec(statement)

    return result.all()
