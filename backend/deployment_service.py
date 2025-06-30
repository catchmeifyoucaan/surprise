import os
import json
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional
import aiofiles
from datetime import datetime
import requests

class DeploymentService:
    def __init__(self):
        self.vercel_token = os.getenv('VERCEL_TOKEN')
        self.netlify_token = os.getenv('NETLIFY_TOKEN')
    
    async def deploy_to_vercel(self, project_path: str, project_name: str) -> Dict[str, Any]:
        """Deploy project to Vercel"""
        try:
            if not self.vercel_token:
                return {
                    "success": False,
                    "error": "Vercel token not configured",
                    "setup_instructions": "Add VERCEL_TOKEN to backend/.env file"
                }
            
            # Create vercel.json configuration
            vercel_config = {
                "name": project_name,
                "version": 2,
                "builds": [
                    {"src": "*.html", "use": "@vercel/static"},
                    {"src": "*.js", "use": "@vercel/node"},
                    {"src": "*.py", "use": "@vercel/python"}
                ]
            }
            
            config_path = Path(project_path) / "vercel.json"
            async with aiofiles.open(config_path, 'w') as f:
                await f.write(json.dumps(vercel_config, indent=2))
            
            # Deploy using Vercel CLI (if available)
            try:
                result = subprocess.run(
                    ['vercel', '--token', self.vercel_token, '--yes'],
                    cwd=project_path,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                if result.returncode == 0:
                    # Extract deployment URL from output
                    output_lines = result.stdout.split('\n')
                    deployment_url = None
                    for line in output_lines:
                        if 'https://' in line and 'vercel.app' in line:
                            deployment_url = line.strip()
                            break
                    
                    return {
                        "success": True,
                        "platform": "Vercel",
                        "url": deployment_url or "Deployment successful (check Vercel dashboard)",
                        "output": result.stdout
                    }
                else:
                    return {
                        "success": False,
                        "error": result.stderr,
                        "suggestion": "Make sure Vercel CLI is installed and token is valid"
                    }
                    
            except FileNotFoundError:
                return {
                    "success": False,
                    "error": "Vercel CLI not found",
                    "setup_instructions": "Install Vercel CLI: npm install -g vercel"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def deploy_to_netlify(self, project_path: str, project_name: str) -> Dict[str, Any]:
        """Deploy project to Netlify"""
        try:
            if not self.netlify_token:
                return {
                    "success": False,
                    "error": "Netlify token not configured",
                    "setup_instructions": "Add NETLIFY_TOKEN to backend/.env file"
                }
            
            # Create netlify.toml configuration
            netlify_config = f"""
[build]
  publish = "."
  command = "echo 'Build complete'"

[build.environment]
  NODE_VERSION = "18"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
"""
            
            config_path = Path(project_path) / "netlify.toml"
            async with aiofiles.open(config_path, 'w') as f:
                await f.write(netlify_config)
            
            # Deploy using Netlify CLI (if available)
            try:
                result = subprocess.run(
                    ['netlify', 'deploy', '--prod', '--auth', self.netlify_token],
                    cwd=project_path,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                if result.returncode == 0:
                    # Extract deployment URL from output
                    output_lines = result.stdout.split('\n')
                    deployment_url = None
                    for line in output_lines:
                        if 'https://' in line and 'netlify.app' in line:
                            deployment_url = line.strip()
                            break
                    
                    return {
                        "success": True,
                        "platform": "Netlify",
                        "url": deployment_url or "Deployment successful (check Netlify dashboard)",
                        "output": result.stdout
                    }
                else:
                    return {
                        "success": False,
                        "error": result.stderr,
                        "suggestion": "Make sure Netlify CLI is installed and token is valid"
                    }
                    
            except FileNotFoundError:
                return {
                    "success": False,
                    "error": "Netlify CLI not found",
                    "setup_instructions": "Install Netlify CLI: npm install -g netlify-cli"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def create_preview_deployment(self, project_path: str, project_name: str) -> Dict[str, Any]:
        """Create a preview deployment (simplified local server)"""
        try:
            # Create a simple HTML preview if no index.html exists
            index_path = Path(project_path) / "index.html"
            if not index_path.exists():
                # Generate basic HTML preview
                html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name}</title>
    <style>
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 800px; 
            margin: 50px auto; 
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{ color: #333; }}
        .file-list {{ margin-top: 30px; }}
        .file {{ 
            background: #f8f9fa; 
            padding: 15px; 
            margin: 10px 0; 
            border-radius: 5px; 
            border-left: 4px solid #007bff;
        }}
        pre {{ 
            background: #282c34; 
            color: #abb2bf; 
            padding: 15px; 
            border-radius: 5px; 
            overflow-x: auto;
            white-space: pre-wrap;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 {project_name}</h1>
        <p>Your AI-generated project is ready!</p>
        
        <div class="file-list">
            <h3>Project Files:</h3>
"""
                
                # Add project files to preview
                for file_path in Path(project_path).rglob('*'):
                    if file_path.is_file() and file_path.name not in ['index.html', 'project_metadata.json']:
                        relative_path = file_path.relative_to(project_path)
                        try:
                            with open(file_path, 'r') as f:
                                content = f.read()
                                html_content += f"""
            <div class="file">
                <h4>📄 {relative_path}</h4>
                <pre><code>{content}</code></pre>
            </div>
"""
                        except UnicodeDecodeError:
                            html_content += f"""
            <div class="file">
                <h4>📄 {relative_path}</h4>
                <p><em>Binary file</em></p>
            </div>
"""
                
                html_content += """
        </div>
        <p><strong>Next Steps:</strong></p>
        <ul>
            <li>Download your project files</li>
            <li>Set up the development environment</li>
            <li>Deploy to production platforms</li>
        </ul>
    </div>
</body>
</html>
"""
                
                async with aiofiles.open(index_path, 'w') as f:
                    await f.write(html_content)
            
            # Try to start a simple HTTP server for preview
            try:
                import http.server
                import socketserver
                import threading
                from functools import partial
                
                # Find available port
                port = 8080
                handler = partial(http.server.SimpleHTTPRequestHandler, directory=project_path)
                
                def start_server():
                    with socketserver.TCPServer(("", port), handler) as httpd:
                        httpd.serve_forever()
                
                # Start server in background thread
                server_thread = threading.Thread(target=start_server, daemon=True)
                server_thread.start()
                
                preview_url = f"http://localhost:{port}"
                
                return {
                    "success": True,
                    "platform": "Preview Server",
                    "url": preview_url,
                    "message": f"Preview available at {preview_url}",
                    "note": "This is a temporary preview. For production deployment, use Vercel or Netlify."
                }
                
            except Exception as server_error:
                return {
                    "success": True,
                    "platform": "Static Preview",
                    "url": str(index_path),
                    "message": "Preview HTML file created",
                    "note": f"Open {index_path} in your browser to view the project"
                }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_deployment_status(self, deployment_id: str) -> Dict[str, Any]:
        """Get status of a deployment"""
        return {
            "success": True,
            "status": "deployed",
            "message": "Deployment tracking requires platform-specific implementation"
        }

# Global deployment service instance
deployment_service = DeploymentService()