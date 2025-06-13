from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks, Depends
from fastapi.responses import FileResponse
import shutil
from  services.image_processor import extract_stamp
from services.pdf_stamper import stamp_pdf
from helpers.remove_file import remove_file
from dependencies.authorisation import authorise_user

router = APIRouter(prefix='/stamps')

@router.post("/extract_stamp/")
async def extract_stamp_endpoint(file: UploadFile = File(...), user=Depends(authorise_user)):
    with open(f"app/static/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    stamp_path = extract_stamp(f"app/static/{file.filename}")
    return FileResponse(stamp_path, filename="extracted_stamp.png", media_type="image/png")

@router.post("/stamp-pdf/")
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