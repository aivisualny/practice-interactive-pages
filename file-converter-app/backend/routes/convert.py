from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import FileResponse
from typing import List, Optional
import os
import uuid
import shutil
from pathlib import Path
import zipfile
from datetime import datetime

from utils.convert_helpers import FileConverter

router = APIRouter()

# 임시 파일 저장 디렉토리
TEMP_DIR = Path("temp")
TEMP_DIR.mkdir(exist_ok=True)

@router.post("/convert")
async def convert_files(
    files: List[UploadFile] = File(...),
    target_format: str = Form(...),
    compression_quality: Optional[int] = Form(85)
):
    """
    파일들을 지정된 형식으로 변환합니다.
    """
    if not files:
        raise HTTPException(status_code=400, detail="업로드된 파일이 없습니다.")
    
    # 파일 크기 제한 (50MB)
    MAX_FILE_SIZE = 50 * 1024 * 1024
    for file in files:
        if file.size and file.size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400, 
                detail=f"파일 {file.filename}이 너무 큽니다. 최대 50MB까지 허용됩니다."
            )
    
    # 세션 ID 생성
    session_id = str(uuid.uuid4())
    session_dir = TEMP_DIR / session_id
    session_dir.mkdir(exist_ok=True)
    
    try:
        converter = FileConverter()
        converted_files = []
        
        for file in files:
            # 파일 저장
            file_path = session_dir / file.filename
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # 파일 변환
            converted_path = await converter.convert_file(
                file_path, 
                target_format, 
                compression_quality
            )
            
            if converted_path:
                converted_files.append(converted_path)
        
        # 결과 파일들을 ZIP으로 압축
        if len(converted_files) == 1:
            # 단일 파일인 경우 ZIP 없이 직접 반환
            return FileResponse(
                converted_files[0],
                filename=converted_files[0].name,
                media_type='application/octet-stream'
            )
        else:
            # 여러 파일인 경우 ZIP으로 압축
            zip_path = session_dir / "converted_files.zip"
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for file_path in converted_files:
                    zipf.write(file_path, file_path.name)
            
            return FileResponse(
                zip_path,
                filename="converted_files.zip",
                media_type='application/zip'
            )
    
    except Exception as e:
        # 에러 발생 시 임시 파일 정리
        if session_dir.exists():
            shutil.rmtree(session_dir)
        raise HTTPException(status_code=500, detail=f"변환 중 오류가 발생했습니다: {str(e)}")

@router.get("/formats")
async def get_supported_formats():
    """
    지원되는 파일 형식 목록을 반환합니다.
    """
    return {
        "image": {
            "from": ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp"],
            "to": ["jpg", "png", "gif", "bmp", "tiff", "webp"]
        },
        "document": {
            "from": ["pdf", "docx", "doc", "txt", "rtf"],
            "to": ["pdf", "docx", "txt", "rtf"]
        }
    }

@router.delete("/cleanup/{session_id}")
async def cleanup_session(session_id: str):
    """
    세션의 임시 파일들을 정리합니다.
    """
    session_dir = TEMP_DIR / session_id
    if session_dir.exists():
        shutil.rmtree(session_dir)
        return {"message": "임시 파일이 정리되었습니다."}
    else:
        raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다.") 