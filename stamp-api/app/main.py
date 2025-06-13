from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from helpers.db import init_db
import sys

import api.auth as auth
import api.stamp as stamp

app = FastAPI()

try:
    init_db()
except Exception as e:
    print(f"Database connection failed: {e}")
    sys.exit(1)


origins = [
    "http://localhost:5173",
    "http://172.0.0.1:5173/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(stamp.router)

def main():
    import uvicorn
    uvicorn.run(app, port=8000)

if __name__ == "__main__":
    main()