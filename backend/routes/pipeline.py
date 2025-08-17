from fastapi import APIRouter, File, UploadFile, HTTPException
from services.pipeline_service import PipelineService
from typing import Dict

router = APIRouter()
pipeline_service = PipelineService()

@router.post("/pipeline")
async def optimize_pipeline(file: UploadFile = File(...)) -> Dict:
    """
    Endpoint for pipeline optimization.
    Accepts a YAML pipeline configuration and returns optimization suggestions.
    """
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Check file extension
        if not (file.filename.endswith('.yaml') or file.filename.endswith('.yml')):
            raise HTTPException(
                status_code=400, 
                detail="File must be YAML format (.yaml or .yml)"
            )
        
        # Read file content
        content = await file.read()
        
        # Process with service
        result = await pipeline_service.optimize(
            filename=file.filename,
            content=content
        )
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/pipeline/generate")
async def generate_pipeline(project_data: dict) -> Dict:
    """
    Endpoint for custom pipeline generation.
    Accepts project information and generates a customized CI/CD pipeline.
    """
    try:
        # Validate required fields
        if not project_data:
            raise HTTPException(status_code=400, detail="No project data provided")
        
        # Process with service
        result = await pipeline_service.generate_pipeline(project_data)
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
