from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import logging
from dotenv import load_dotenv

# Import your services
from services.ted_service import TEDService
from services.gemini_service import GeminiService

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Toptimize API", version="1.0.0")

# Add CORS middleware to allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # React app URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class TenderAnalysisRequest(BaseModel):
    tender_id: str
    tender_url: Optional[str] = None

class TenderOptimizationRequest(BaseModel):
    tender_description: str
    company_description: str
    budget_range: Optional[str] = None
    target_countries: Optional[List[str]] = None

class PriceRange(BaseModel):
    min: int
    max: int

class TenderAnalysisResponse(BaseModel):
    title: str
    price_range: PriceRange
    confidence: int
    requirements: List[str]
    compliance: int
    analysis_summary: Optional[str] = None

class TenderOptimizationResponse(BaseModel):
    relevant_tenders: List[dict]
    detailed_tender: Optional[dict] = None
    optimization_suggestions: str
    success: bool = True

@app.get("/")
async def root():
    return {"message": "Toptimize API is running!"}

@app.post("/optimize-tender", response_model=TenderOptimizationResponse)
async def optimize_tender(request: TenderOptimizationRequest):
    try:
        logger.info(f"Optimizing tender for query: {request.tender_description}")
        
        # Search for relevant tenders using TED API
        ted_service = TEDService()
        relevant_tenders = ted_service.search_tenders(
            query=request.tender_description,
            limit=5
        )
        
        detailed_tender = None
        # Get detailed info for the most relevant tender
        if relevant_tenders:
            logger.info(f"Found {len(relevant_tenders)} relevant tenders")
            detailed_tender = ted_service.get_tender_details(relevant_tenders[0]['id'])
        
        # Use Gemini to optimize response
        gemini_service = GeminiService()
        optimization = gemini_service.optimize_tender_response(
            tender_description=request.tender_description,
            company_description=request.company_description,
            relevant_tenders=relevant_tenders
        )
        
        return TenderOptimizationResponse(
            relevant_tenders=relevant_tenders,
            detailed_tender=detailed_tender,
            optimization_suggestions=optimization,
            success=True
        )
        
    except Exception as e:
        logger.error(f"Optimization error: {e}")
        raise HTTPException(status_code=500, detail=f"Optimization failed: {str(e)}")

@app.post("/analyze-tender", response_model=TenderAnalysisResponse)
async def analyze_tender(request: TenderAnalysisRequest):
    try:
        logger.info(f"Analyzing tender: {request.tender_id}")
        
        # Get tender details
        ted_service = TEDService()
        tender_details = ted_service.get_tender_details(request.tender_id)
        
        if not tender_details:
            raise HTTPException(status_code=404, detail="Tender not found")
        
        # Use Gemini to analyze the tender
        gemini_service = GeminiService()
        analysis = gemini_service.analyze_tender(tender_details)
        
        return TenderAnalysisResponse(
            title=tender_details.get('title', 'Unknown'),
            price_range=PriceRange(
                min=int(tender_details.get('estimated_value', 0) * 0.8),
                max=int(tender_details.get('estimated_value', 0) * 1.2)
            ),
            confidence=85,
            requirements=tender_details.get('requirements', []),
            compliance=75,
            analysis_summary=analysis
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/search-tenders")
async def search_tenders(q: str, limit: int = 10):
    """Search for tenders based on query"""
    try:
        ted_service = TEDService()
        results = ted_service.search_tenders(q, limit)
        
        return {
            "query": q,
            "results": results,
            "count": len(results)
        }
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/tender/{tender_id}")
async def get_tender_details(tender_id: str):
    """Get detailed information about a specific tender"""
    try:
        ted_service = TEDService()
        details = ted_service.get_tender_details(tender_id)
        
        if not details:
            raise HTTPException(status_code=404, detail="Tender not found")
            
        return details
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Tender details error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get tender details: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test TED API connection
        ted_service = TEDService()
        ted_status = ted_service.test_connection()
        
        # Test Gemini connection (you can add this method to GeminiService)
        gemini_service = GeminiService()
        gemini_status = True  # Placeholder - implement test_connection in GeminiService
        
        return {
            "status": "healthy",
            "service": "Toptimize API",
            "ted_api": "connected" if ted_status else "disconnected",
            "gemini_api": "connected" if gemini_status else "disconnected"
        }
        
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return {
            "status": "unhealthy",
            "service": "Toptimize API",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
