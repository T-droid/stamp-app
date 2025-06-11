from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
from  services.image_processor import extract_stamp
from services.pdf_stamper import stamp_pdf
from helpers.remove_file import remove_file
from helpers.db import init_db
import sys
import api.auth as auth

app = FastAPI()
app.include_router(auth.router)
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


@app.post("/extract_stamp/")
async def extract_stamp_endpoint(file: UploadFile = File(...)):
    with open(f"app/static/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    stamp_path = extract_stamp(f"app/static/{file.filename}")
    return FileResponse(stamp_path, filename="extracted_stamp.png", media_type="image/png")

@app.post("/stamp-pdf/")
async def stamp_pdf_endpoint(
    pdf_file: UploadFile = File(...),
    stamp_file: UploadFile = File(...),
    x: int = Form(100),
    y: int = Form(100),
    scale: float = Form(0.5),
    page_num: int = Form(0),
    background_tasks: BackgroundTasks = None
    ):
    with open(f"app/static/{pdf_file.filename}", "wb") as pdf_buffer:
        shutil.copyfileobj(pdf_file.file, pdf_buffer)
    with open(f"app/static/{stamp_file.filename}", "wb") as stamp_buffer:
        shutil.copyfileobj(stamp_file.file, stamp_buffer)

    output_pdf = stamp_pdf(
        pdf_path=f"app/static/{pdf_file.filename}",
        stamp_path=f"app/static/{stamp_file.filename}",
        position=(x, y),
        scale=scale,
        page_number=page_num
    )

    # Clean up the uploaded files
    background_tasks.add_task(remove_file, f"app/static/{pdf_file.filename}")
    background_tasks.add_task(remove_file, f"app/static/{stamp_file.filename}")
    background_tasks.add_task(remove_file, output_pdf)

    return FileResponse(output_pdf, filename="stamped_output.pdf", media_type="application/pdf")

def main():
    import uvicorn
    uvicorn.run(app, port=8000)

if __name__ == "__main__":
    main()