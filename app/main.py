from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user, post, auth, vote

#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origin = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello World"}

###uvicorn app.main:app --reload
