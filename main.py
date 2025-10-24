from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.db.database import engine
from app.db.models import Base
from app.routers import users
from app.db.seed_sessions import seed_sessions


app = FastAPI()

Base.metadata.create_all(bind=engine)

# seed_sessions()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","https://pomopopo.com",'https://pomopopo-git-feature-auth-songyes-projects-cb766be0.vercel.app'],

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)