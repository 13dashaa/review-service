import enum
import os
from datetime import datetime
from typing import List, Optional

from fastapi import Depends, FastAPI, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker


DATABASE_FILE = "reviews.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.abspath(DATABASE_FILE)}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    sentiment = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


POSITIVE_KEYWORDS = {"хорош", "отлично", "супер", "нравится", "люблю", "прекрасно"}
NEGATIVE_KEYWORDS = {"плохо", "ужасно", "ненавижу", "проблема", "ошибка", "не работает"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def analyze_sentiment(text: str) -> str:

    text_lower = text.lower()

    if any(word in text_lower for word in NEGATIVE_KEYWORDS):
        return "negative"

    if any(word in text_lower for word in POSITIVE_KEYWORDS):
        return "positive"

    return "neutral"


class ReviewIn(BaseModel):
    text: str


class ReviewOut(BaseModel):
    id: int
    text: str
    sentiment: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Sentiment(str, enum.Enum):
    positive = "positive"
    neutral = "neutral"
    negative = "negative"
app = FastAPI()


@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)


@app.post(
    "/review",response_model=ReviewOut, status_code=status.HTTP_201_CREATED
)
def create_review(review_in: ReviewIn, db: Session = Depends(get_db)):
    sentiment = analyze_sentiment(review_in.text)

    db_review = Review(text=review_in.text, sentiment=sentiment)

    db.add(db_review)
    db.commit()
    db.refresh(db_review)

    return db_review


@app.get("/reviews", response_model=List[ReviewOut])
def read_reviews(sentiment: Optional[Sentiment] = None, db: Session = Depends(get_db)):

    query = db.query(Review)

    if sentiment:
       query = query.filter(Review.sentiment == sentiment)

    reviews = query.all()

    return reviews
