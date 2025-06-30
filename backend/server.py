from fastapi import FastAPI, APIRouter, HTTPException, File, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime
import json

# Import our AI services (with error handling)
try:
    from ai_service import ai_service
    AI_AVAILABLE = True
except Exception as e:
    print(f"Warning: AI service not available: {e}")
    AI_AVAILABLE = False
    ai_service = None

try:
    from project_manager import project_manager
    PROJECT_MANAGER_AVAILABLE = True
except Exception as e:
    print(f"Warning: Project manager not available: {e}")
    PROJECT_MANAGER_AVAILABLE = False
    project_manager = None

try:
    from deployment_service import deployment_service
    DEPLOYMENT_AVAILABLE = True
except Exception as e:
    print(f"Warning: Deployment service not available: {e}")
    DEPLOYMENT_AVAILABLE = False
    deployment_service = None

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'emergent_ai')]

# Create the main app without a prefix
app = FastAPI(title="Emergent AI Coding Assistant", version="2.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Define Models
class ChatMessage(BaseModel):
    message: str
    user_id: str = "anonymous"
    language: str = "python"
    model: str = "auto"

class CodeExecutionRequest(BaseModel):
    code: str
    language: str = "python"
    user_id: str = "anonymous"

class ProjectCreationRequest(BaseModel):
    description: str
    tech_stack: str = "Python"
    user_id: str = "anonymous"

class FileUpdateRequest(BaseModel):
    file_path: str
    content: str
    user_id: str
    project_id: str

class DeploymentRequest(BaseModel):
    project_id: str
    user_id: str
    platform: str = "vercel"  # vercel, netlify, preview

class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

# AI Chat Endpoints
@api_router.post("/chat")
async def chat_with_ai(request: ChatMessage):
    """Chat with AI and generate code based on user message"""
    try:
        # Always try to generate code, even without API keys
        if AI_AVAILABLE and ai_service:
            result = await ai_service.generate_code(
                prompt=request.message,
                language=request.language,
                model=request.model
            )
        else:
            # Create a local fallback AI service for demonstration
            from ai_service import AIService
            temp_ai_service = AIService()
            result = await temp_ai_service.generate_code(
                prompt=request.message,
                language=request.language,
                model=request.model
            )
        
        # Store chat history in database
        try:
            chat_record = {
                "user_id": request.user_id,
                "message": request.message,
                "response": result,
                "timestamp": datetime.utcnow(),
                "language": request.language,
                "model": request.model
            }
            await db.chat_history.insert_one(chat_record)
        except Exception as db_error:
            print(f"Database error: {db_error}")
        
        return {
            "success": True,
            "response": result,
            "message": "Code generated successfully!" if result.get("success") else "Code generation completed with fallback",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        # Provide meaningful error response
        fallback_result = {
            "success": True,
            "code": f"# Error handling example\ntry:\n    # Your code here\n    print('Hello, World!')\nexcept Exception as e:\n    print(f'Error: {{e}}')",
            "explanation": f"An error occurred while processing your request: {str(e)}. This is a basic template to get you started.",
            "model_used": "Error Handler",
            "language": request.language,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return {
            "success": True,
            "response": fallback_result,
            "message": f"Fallback response due to error: {str(e)}",
            "timestamp": datetime.utcnow().isoformat()
        }

@api_router.post("/execute")
async def execute_code(request: CodeExecutionRequest):
    """Execute code safely in a sandboxed environment"""
    try:
        result = await ai_service.execute_code(request.code, request.language)
        
        # Store execution history
        execution_record = {
            "user_id": request.user_id,
            "code": request.code,
            "language": request.language,
            "result": result,
            "timestamp": datetime.utcnow()
        }
        await db.execution_history.insert_one(execution_record)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/analyze")
async def analyze_code(request: CodeExecutionRequest):
    """Analyze code for quality, bugs, and improvements"""
    try:
        result = await ai_service.analyze_code(request.code, request.language)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Project Management Endpoints
@api_router.post("/projects")
async def create_project(request: ProjectCreationRequest):
    """Create a new project from AI-generated code"""
    try:
        # Generate project structure using AI
        project_data = await ai_service.generate_project(
            description=request.description,
            tech_stack=request.tech_stack
        )
        
        if not project_data.get("success"):
            raise HTTPException(status_code=500, detail=project_data.get("error"))
        
        # Create the project files
        result = await project_manager.create_project(
            user_id=request.user_id,
            project_data=project_data["project"]
        )
        
        if result.get("success"):
            # Store project in database
            project_record = {
                "project_id": result["project_id"],
                "user_id": request.user_id,
                "name": result["project_name"],
                "description": request.description,
                "tech_stack": request.tech_stack,
                "created_at": datetime.utcnow(),
                "status": "created"
            }
            await db.projects.insert_one(project_record)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/projects/{user_id}")
async def list_projects(user_id: str):
    """List all projects for a user"""
    try:
        result = await project_manager.list_projects(user_id)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/projects/{user_id}/{project_id}")
async def get_project(user_id: str, project_id: str):
    """Get project details and files"""
    try:
        result = await project_manager.get_project(user_id, project_id)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.put("/projects/files")
async def update_file(request: FileUpdateRequest):
    """Update a file in a project"""
    try:
        result = await project_manager.update_file(
            user_id=request.user_id,
            project_id=request.project_id,
            file_path=request.file_path,
            content=request.content
        )
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.delete("/projects/{user_id}/{project_id}")
async def delete_project(user_id: str, project_id: str):
    """Delete a project"""
    try:
        result = await project_manager.delete_project(user_id, project_id)
        
        # Remove from database
        await db.projects.delete_one({"project_id": project_id, "user_id": user_id})
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/projects/{user_id}/{project_id}/export")
async def export_project(user_id: str, project_id: str):
    """Export project as ZIP file"""
    try:
        result = await project_manager.export_project(user_id, project_id)
        
        if result.get("success"):
            zip_path = result["zip_path"]
            return FileResponse(
                zip_path,
                media_type="application/zip",
                filename=f"project-{project_id}.zip"
            )
        else:
            raise HTTPException(status_code=404, detail=result.get("error"))
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Deployment Endpoints
@api_router.post("/deploy")
async def deploy_project(request: DeploymentRequest):
    """Deploy project to cloud platforms"""
    try:
        # Get project details
        project_result = await project_manager.get_project(request.user_id, request.project_id)
        
        if not project_result.get("success"):
            raise HTTPException(status_code=404, detail="Project not found")
        
        project_path = project_result["path"]
        project_name = project_result["metadata"].get("name", f"project-{request.project_id}")
        
        # Deploy based on platform
        if request.platform == "vercel":
            result = await deployment_service.deploy_to_vercel(project_path, project_name)
        elif request.platform == "netlify":
            result = await deployment_service.deploy_to_netlify(project_path, project_name)
        elif request.platform == "preview":
            result = await deployment_service.create_preview_deployment(project_path, project_name)
        else:
            raise HTTPException(status_code=400, detail="Unsupported deployment platform")
        
        # Store deployment record
        if result.get("success"):
            deployment_record = {
                "project_id": request.project_id,
                "user_id": request.user_id,
                "platform": request.platform,
                "url": result.get("url"),
                "deployed_at": datetime.utcnow(),
                "status": "deployed"
            }
            await db.deployments.insert_one(deployment_record)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/deployments/{user_id}")
async def list_deployments(user_id: str):
    """List all deployments for a user"""
    try:
        deployments = await db.deployments.find({"user_id": user_id}).to_list(100)
        for deployment in deployments:
            deployment["_id"] = str(deployment["_id"])
        
        return {
            "success": True,
            "deployments": deployments
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Original endpoints for compatibility
@api_router.get("/")
async def root():
    return {
        "message": "Emergent AI Coding Assistant API",
        "version": "2.0.0",
        "features": [
            "AI Code Generation",
            "Code Execution",
            "Project Management",
            "Cloud Deployment",
            "Code Analysis"
        ]
    }

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
