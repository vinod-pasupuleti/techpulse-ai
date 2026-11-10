from sqlalchemy import select
from sqlalchemy.orm import Session
from database import engine
from models import Article

with Session(engine) as session:
    statement = select(Article)

    articles = session.scalars(statement).all()

    for article in articles:
        print(f"ID: {article.id}")
        print(f"Title: {article.title}")
        print(f"Source: {article.source}")
        print(f"Link: {article.link}")
        print("-" * 40)
