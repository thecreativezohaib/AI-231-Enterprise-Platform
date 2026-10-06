import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from neo4j import GraphDatabase
import redis

# PostgreSQL Setup
POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql://admin:password@localhost:5432/ai231")
engine = create_engine(POSTGRES_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Neo4j Setup
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

try:
    neo4j_driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
except Exception as e:
    print(f"Neo4j connection error: {e}")
    neo4j_driver = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Redis Setup
try:
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
except Exception as e:
    redis_client = None
