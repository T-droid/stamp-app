from fastapi import FastAPI

app = FastAPI()
@app.get("/")
def read_root():
    return {"Hello": "World"}

def main():
    app.run(host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
