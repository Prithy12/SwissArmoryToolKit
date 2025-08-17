from fastapi import APIRouter, File, UploadFile, HTTPException
from services.test_service import TestService
from typing import Dict

router = APIRouter()
test_service = TestService()

@router.post("/tests")
async def generate_tests(file: UploadFile = File(...)) -> Dict:
    """
    Endpoint for test generation.
    Accepts a coverage JSON file and returns generated test suggestions.
    """
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Check file extension
        if not file.filename.endswith('.json'):
            raise HTTPException(
                status_code=400, 
                detail="File must be JSON format (.json)"
            )
        
        # Read file content
        content = await file.read()
        
        # Process with service
        result = await test_service.generate_tests(
            filename=file.filename,
            content=content
        )
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
