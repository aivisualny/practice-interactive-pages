import asyncio
from pathlib import Path
from PIL import Image
import subprocess
import os
import shutil
from typing import Optional

class FileConverter:
    def __init__(self):
        self.supported_image_formats = {
            'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp'
        }
        self.supported_document_formats = {
            'pdf', 'docx', 'doc', 'txt', 'rtf'
        }
    
    async def convert_file(
        self, 
        file_path: Path, 
        target_format: str, 
        compression_quality: int = 85
    ) -> Optional[Path]:
        """
        파일을 지정된 형식으로 변환합니다.
        """
        file_extension = file_path.suffix.lower().lstrip('.')
        
        # 이미지 파일 변환
        if file_extension in self.supported_image_formats and target_format in self.supported_image_formats:
            return await self._convert_image(file_path, target_format, compression_quality)
        
        # 문서 파일 변환 (기본적으로는 지원하지 않지만 확장 가능)
        elif file_extension in self.supported_document_formats and target_format in self.supported_document_formats:
            return await self._convert_document(file_path, target_format)
        
        else:
            raise ValueError(f"지원하지 않는 변환: {file_extension} → {target_format}")
    
    async def _convert_image(
        self, 
        file_path: Path, 
        target_format: str, 
        compression_quality: int
    ) -> Path:
        """
        이미지 파일을 변환합니다.
        """
        try:
            # PIL을 사용한 이미지 변환
            with Image.open(file_path) as img:
                # RGBA 모드를 RGB로 변환 (JPEG는 알파 채널을 지원하지 않음)
                if target_format.lower() in ['jpg', 'jpeg'] and img.mode in ['RGBA', 'LA']:
                    # 흰색 배경으로 합성
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'RGBA':
                        background.paste(img, mask=img.split()[-1])  # 알파 채널을 마스크로 사용
                    else:
                        background.paste(img)
                    img = background
                
                # 출력 파일 경로 생성
                output_path = file_path.parent / f"{file_path.stem}.{target_format}"
                
                # 이미지 저장
                if target_format.lower() in ['jpg', 'jpeg']:
                    img.save(output_path, 'JPEG', quality=compression_quality, optimize=True)
                elif target_format.lower() == 'png':
                    img.save(output_path, 'PNG', optimize=True)
                elif target_format.lower() == 'gif':
                    img.save(output_path, 'GIF')
                elif target_format.lower() == 'bmp':
                    img.save(output_path, 'BMP')
                elif target_format.lower() == 'tiff':
                    img.save(output_path, 'TIFF', compression='tiff_lzw')
                elif target_format.lower() == 'webp':
                    img.save(output_path, 'WEBP', quality=compression_quality)
                else:
                    raise ValueError(f"지원하지 않는 이미지 형식: {target_format}")
                
                return output_path
                
        except Exception as e:
            raise Exception(f"이미지 변환 중 오류 발생: {str(e)}")
    
    async def _convert_document(
        self, 
        file_path: Path, 
        target_format: str
    ) -> Path:
        """
        문서 파일을 변환합니다. (기본 구현 - 확장 가능)
        """
        # 현재는 기본적인 텍스트 파일 변환만 지원
        if file_path.suffix.lower() == '.txt' and target_format == 'txt':
            return file_path
        
        # LibreOffice를 사용한 변환 (시스템에 설치되어 있는 경우)
        try:
            output_path = file_path.parent / f"{file_path.stem}.{target_format}"
            
            # LibreOffice 명령어 실행
            cmd = [
                'libreoffice', 
                '--headless', 
                '--convert-to', target_format,
                '--outdir', str(file_path.parent),
                str(file_path)
            ]
            
            # 비동기로 명령어 실행
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0 and output_path.exists():
                return output_path
            else:
                raise Exception(f"LibreOffice 변환 실패: {stderr.decode()}")
                
        except FileNotFoundError:
            raise Exception("LibreOffice가 설치되어 있지 않습니다. 문서 변환을 위해서는 LibreOffice를 설치해주세요.")
        except Exception as e:
            raise Exception(f"문서 변환 중 오류 발생: {str(e)}")
    
    def get_file_info(self, file_path: Path) -> dict:
        """
        파일 정보를 반환합니다.
        """
        try:
            with Image.open(file_path) as img:
                return {
                    "format": img.format,
                    "mode": img.mode,
                    "size": img.size,
                    "file_size": file_path.stat().st_size
                }
        except Exception:
            return {
                "format": "unknown",
                "file_size": file_path.stat().st_size
            } 