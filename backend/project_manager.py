import os
import json
import shutil
import zipfile
from pathlib import Path
from typing import Dict, List, Any, Optional
import aiofiles
from datetime import datetime
import uuid

class ProjectManager:
    def __init__(self, base_path: str = "/tmp/emergent_projects"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
    
    async def create_project(self, user_id: str, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new project from AI-generated data"""
        try:
            project_id = str(uuid.uuid4())
            project_name = project_data.get('project_name', f'project-{project_id[:8]}')
            
            # Create project directory
            project_path = self.base_path / user_id / project_id
            project_path.mkdir(parents=True, exist_ok=True)
            
            # Create all project files
            files_created = []
            for file_path, content in project_data.get('files', {}).items():
                full_file_path = project_path / file_path
                full_file_path.parent.mkdir(parents=True, exist_ok=True)
                
                async with aiofiles.open(full_file_path, 'w') as f:
                    await f.write(content)
                files_created.append(str(file_path))
            
            # Create project metadata
            metadata = {
                "id": project_id,
                "name": project_name,
                "description": project_data.get('description', ''),
                "tech_stack": project_data.get('tech_stack', ''),
                "created_at": datetime.utcnow().isoformat(),
                "files": files_created,
                "setup_instructions": project_data.get('setup_instructions', ''),
                "status": "created"
            }
            
            metadata_path = project_path / "project_metadata.json"
            async with aiofiles.open(metadata_path, 'w') as f:
                await f.write(json.dumps(metadata, indent=2))
            
            return {
                "success": True,
                "project_id": project_id,
                "project_name": project_name,
                "path": str(project_path),
                "files_created": len(files_created),
                "metadata": metadata
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_project(self, user_id: str, project_id: str) -> Dict[str, Any]:
        """Get project details and files"""
        try:
            project_path = self.base_path / user_id / project_id
            if not project_path.exists():
                return {"success": False, "error": "Project not found"}
            
            # Read metadata
            metadata_path = project_path / "project_metadata.json"
            if metadata_path.exists():
                async with aiofiles.open(metadata_path, 'r') as f:
                    metadata = json.loads(await f.read())
            else:
                metadata = {"id": project_id, "name": "Unknown Project"}
            
            # Get all project files
            files = {}
            for file_path in project_path.rglob('*'):
                if file_path.is_file() and file_path.name != 'project_metadata.json':
                    relative_path = file_path.relative_to(project_path)
                    try:
                        async with aiofiles.open(file_path, 'r') as f:
                            files[str(relative_path)] = await f.read()
                    except UnicodeDecodeError:
                        files[str(relative_path)] = "[Binary file]"
            
            return {
                "success": True,
                "metadata": metadata,
                "files": files,
                "path": str(project_path)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def list_projects(self, user_id: str) -> Dict[str, Any]:
        """List all projects for a user"""
        try:
            user_path = self.base_path / user_id
            if not user_path.exists():
                return {"success": True, "projects": []}
            
            projects = []
            for project_dir in user_path.iterdir():
                if project_dir.is_dir():
                    metadata_path = project_dir / "project_metadata.json"
                    if metadata_path.exists():
                        async with aiofiles.open(metadata_path, 'r') as f:
                            metadata = json.loads(await f.read())
                            projects.append(metadata)
            
            return {
                "success": True,
                "projects": sorted(projects, key=lambda x: x.get('created_at', ''), reverse=True)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def update_file(self, user_id: str, project_id: str, file_path: str, content: str) -> Dict[str, Any]:
        """Update a specific file in a project"""
        try:
            project_path = self.base_path / user_id / project_id
            if not project_path.exists():
                return {"success": False, "error": "Project not found"}
            
            full_file_path = project_path / file_path
            full_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            async with aiofiles.open(full_file_path, 'w') as f:
                await f.write(content)
            
            return {
                "success": True,
                "message": f"File {file_path} updated successfully"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def delete_project(self, user_id: str, project_id: str) -> Dict[str, Any]:
        """Delete a project"""
        try:
            project_path = self.base_path / user_id / project_id
            if not project_path.exists():
                return {"success": False, "error": "Project not found"}
            
            shutil.rmtree(project_path)
            
            return {
                "success": True,
                "message": "Project deleted successfully"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def export_project(self, user_id: str, project_id: str) -> Dict[str, Any]:
        """Export project as ZIP file"""
        try:
            project_path = self.base_path / user_id / project_id
            if not project_path.exists():
                return {"success": False, "error": "Project not found"}
            
            # Create ZIP file
            zip_path = self.base_path / f"{project_id}.zip"
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in project_path.rglob('*'):
                    if file_path.is_file() and file_path.name != 'project_metadata.json':
                        arcname = file_path.relative_to(project_path)
                        zipf.write(file_path, arcname)
            
            return {
                "success": True,
                "zip_path": str(zip_path),
                "download_url": f"/api/projects/{project_id}/download"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

# Global project manager instance
project_manager = ProjectManager()