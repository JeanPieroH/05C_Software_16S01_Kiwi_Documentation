from fastapi import APIRouter, Request, Depends, HTTPException, UploadFile, File, Form
# from schemas import Quiz, QuizGenerationInput
from utils.auth import verify_token
import httpx
import os
from schemas import *
timeout = httpx.Timeout(30.0)  # 30 segundos


router = APIRouter(dependencies=[Depends(verify_token)])

users_url = os.getenv("USERS_API_URL", "http://localhost:8080")
classrooms_url = os.getenv("CLASSROOMS_API_URL", "http://localhost:3000")
quices_url = os.getenv("QUICES_API_URL", "http://localhost:8001/api/v1")



@router.get("/{quiz_id}", response_model=QuizDetail)
async def get_quiz(quiz_id: int,request: Request):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{quices_url}/quiz/{quiz_id}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@router.get("/{quiz_id}/student/{student_id}/result", response_model=QuizResultDetail)
async def get_quiz(quiz_id: int,student_id: int, request: Request):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{quices_url}/quiz/{quiz_id}/student/{student_id}/result")
            response.raise_for_status()

            
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
        
# @router.post("/{teacher_id}/classroom/{classroom_id}/quiz", status_code=201)
# async def create_quiz(teacher_id: int, classroom_id: int, quiz: Quiz, request: Request):
#     headers = dict(request.headers)
#     quiz_data = quiz.model_dump()
#     quiz_data["id_classroom"] = classroom_id
#     quiz_data["id_teacher"] = teacher_id

#     async with httpx.AsyncClient() as client:
#         try:
#             res = await client.post(f"{quices_url}/quiz", json=quiz_data, headers=headers)
#             res.raise_for_status()
#             return res.json()
#         except httpx.HTTPStatusError as e:
#             raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

# @router.post("/{teacher_id}/classroom/{classroom_id}/quiz/generate", status_code=201)
# async def generate_quiz(teacher_id: int, classroom_id: int, input_data: QuizGenerationInput, request: Request):
#     headers = dict(request.headers)
#     data = input_data.model_dump()
#     data["id_classroom"] = classroom_id
#     data["id_teacher"] = teacher_id

#     async with httpx.AsyncClient() as client:
#         try:
#             res = await client.post(f"{quices_url}/quiz/generate", json=data, headers=headers)
#             res.raise_for_status()
#             return res.json()
#         except httpx.HTTPStatusError as e:
#             raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

# @router.post("/{teacher_id}/classroom/{classroom_id}/quiz/generate-from-pdf", status_code=201)
# async def generate_quiz_from_pdf(
#     teacher_id: int,
#     classroom_id: int,
#     request: Request,
#     title: str = Form(...),
#     description: str = Form(""),
#     num_questions: int = Form(5),
#     file: UploadFile = File(...)
# ):
#     form_data = {
#         "title": title,
#         "description": description,
#         "num_questions": str(num_questions),
#         "id_classroom": str(classroom_id),
#         "id_teacher": str(teacher_id)
#     }

#     files = {
#         "file": (file.filename, file.file, file.content_type)
#     }

#     async with httpx.AsyncClient(timeout=timeout) as client:
#         try:
#             # Paso 1: crear el quiz
#             response = await client.post(
#                 f"{quices_url}/quiz/generate-from-pdf",
#                 data=form_data,
#                 files=files,
#                 headers=None  # deja que httpx maneje multipart headers
#             )
#             response.raise_for_status()
#             creation_data = response.json()
#             quiz_id = creation_data["quiz_id"]
#         except httpx.HTTPStatusError as e:
#             raise HTTPException(status_code=e.response.status_code, detail=f"Error creando quiz: {e.response.text}")
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"Error interno creando quiz: {str(e)}")

#         try:
#             # Paso 2: obtener el quiz completo con preguntas
#             quiz_response = await client.get(f"{quices_url}/quiz/{quiz_id}")
#             quiz_response.raise_for_status()
#             return quiz_response.json()
#         except httpx.HTTPStatusError as e:
#             raise HTTPException(status_code=e.response.status_code, detail=f"Error obteniendo quiz: {e.response.text}")
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"Error interno obteniendo quiz: {str(e)}")
