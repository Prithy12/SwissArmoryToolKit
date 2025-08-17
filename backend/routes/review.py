from fastapi import APIRouter, File, UploadFile, HTTPException
from services.code_review_service import CodeReviewService
from typing import Dict

router = APIRouter()
review_service = CodeReviewService()

@router.post("/review")
async def review_code(file: UploadFile = File(...)) -> Dict:
    """
    Endpoint for code review analysis.
    Accepts a code diff file and returns AI-powered review suggestions.
    """
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Read file content
        content = await file.read()
        
        # Process with service
        result = await review_service.analyze_diff(
            filename=file.filename,
            content=content
        )
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
