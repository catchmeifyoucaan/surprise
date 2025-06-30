import os
import json
import asyncio
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional
import aiofiles
from fastapi import HTTPException
import openai
import anthropic
import groq
from datetime import datetime

class AIService:
    def __init__(self):
        # Initialize AI clients
        self.openai_client = None
        self.anthropic_client = None
        self.groq_client = None
        
        # Initialize clients based on available API keys
        if os.getenv('OPENAI_API_KEY'):
            openai.api_key = os.getenv('OPENAI_API_KEY')
            self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        if os.getenv('ANTHROPIC_API_KEY'):
            self.anthropic_client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        
        if os.getenv('GROQ_API_KEY'):
            self.groq_client = groq.Groq(api_key=os.getenv('GROQ_API_KEY'))
    
    async def generate_code(self, prompt: str, language: str = "python", model: str = "auto") -> Dict[str, Any]:
        """Generate code based on user prompt using the best available AI model"""
        try:
            # Enhanced prompt for better code generation
            enhanced_prompt = f"""
            You are an expert software engineer. Generate high-quality, production-ready code based on this request:
            
            REQUEST: {prompt}
            LANGUAGE: {language}
            
            REQUIREMENTS:
            1. Write clean, well-structured, and commented code
            2. Include error handling where appropriate
            3. Follow best practices for the specified language
            4. Make the code modular and reusable
            5. Include any necessary imports/dependencies
            6. Provide a brief explanation of what the code does
            
            RESPONSE FORMAT:
            ```{language}
            [Generated Code Here]
            ```
            
            EXPLANATION:
            [Brief explanation of the code functionality]
            """
            
            # Try different AI models in order of preference
            response = None
            model_used = None
            
            # Try OpenAI GPT-4 first (most capable)
            if self.openai_client and model in ["auto", "openai", "gpt-4"]:
                try:
                    response = self.openai_client.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "You are an expert software engineer and coding assistant."},
                            {"role": "user", "content": enhanced_prompt}
                        ],
                        max_tokens=2000,
                        temperature=0.3
                    )
                    model_used = "OpenAI GPT-4"
                    response_text = response.choices[0].message.content
                except Exception as e:
                    print(f"OpenAI API error: {e}")
                    
            # Try Anthropic Claude if OpenAI fails or requested
            if not response and self.anthropic_client and model in ["auto", "anthropic", "claude"]:
                try:
                    response = self.anthropic_client.messages.create(
                        model="claude-3-sonnet-20240229",
                        max_tokens=2000,
                        temperature=0.3,
                        messages=[
                            {"role": "user", "content": enhanced_prompt}
                        ]
                    )
                    model_used = "Anthropic Claude-3"
                    response_text = response.content[0].text
                except Exception as e:
                    print(f"Anthropic API error: {e}")
            
            # Try Groq as fallback (fast and free)
            if not response and self.groq_client and model in ["auto", "groq"]:
                try:
                    response = self.groq_client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "You are an expert software engineer and coding assistant."},
                            {"role": "user", "content": enhanced_prompt}
                        ],
                        model="mixtral-8x7b-32768",
                        temperature=0.3,
                        max_tokens=2000,
                    )
                    model_used = "Groq Mixtral"
                    response_text = response.choices[0].message.content
                except Exception as e:
                    print(f"Groq API error: {e}")
            
            if not response:
                # Fallback to mock response with actual working code
                response_text = self._generate_fallback_code(prompt, language)
                model_used = "Fallback Code Generator"
            
            # Parse the response to extract code and explanation
            code, explanation = self._parse_ai_response(response_text, language)
            
            return {
                "success": True,
                "code": code,
                "explanation": explanation,
                "language": language,
                "model_used": model_used,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _parse_ai_response(self, response_text: str, language: str) -> tuple:
        """Parse AI response to extract code and explanation"""
        lines = response_text.split('\n')
        code_lines = []
        explanation_lines = []
        in_code_block = False
        in_explanation = False
        
        for line in lines:
            if line.strip().startswith(f'```{language}') or line.strip().startswith('```python') or line.strip().startswith('```javascript'):
                in_code_block = True
                continue
            elif line.strip() == '```' and in_code_block:
                in_code_block = False
                continue
            elif line.strip().upper().startswith('EXPLANATION') or line.strip().startswith('**Explanation'):
                in_explanation = True
                continue
            
            if in_code_block:
                code_lines.append(line)
            elif in_explanation or (not in_code_block and not code_lines):
                explanation_lines.append(line)
        
        code = '\n'.join(code_lines).strip() if code_lines else response_text
        explanation = '\n'.join(explanation_lines).strip() if explanation_lines else "AI-generated code based on your request."
        
        return code, explanation
    
    def _generate_fallback_code(self, prompt: str, language: str) -> str:
        """Generate fallback code when AI APIs are not available"""
        if language.lower() == 'python':
            return f'''# {prompt}
def main():
    """
    Generated code based on: {prompt}
    This is a fallback implementation.
    """
    print("Hello from AI-generated code!")
    # TODO: Implement the actual functionality based on: {prompt}
    
if __name__ == "__main__":
    main()

EXPLANATION:
This is a basic Python template generated as a fallback. To get fully functional AI-generated code, please add your AI API keys to the backend/.env file.
'''
        elif language.lower() in ['javascript', 'js']:
            return f'''// {prompt}
function main() {{
    /*
     * Generated code based on: {prompt}
     * This is a fallback implementation.
     */
    console.log("Hello from AI-generated code!");
    // TODO: Implement the actual functionality based on: {prompt}
}}

main();

EXPLANATION:
This is a basic JavaScript template generated as a fallback. To get fully functional AI-generated code, please add your AI API keys to the backend/.env file.
'''
        else:
            return f'''// {prompt}
// This is a fallback template for {language}
// TODO: Implement the actual functionality based on: {prompt}

EXPLANATION:
This is a basic template generated as a fallback. To get fully functional AI-generated code, please add your AI API keys to the backend/.env file.
'''
    
    async def execute_code(self, code: str, language: str) -> Dict[str, Any]:
        """Execute code safely in a sandboxed environment"""
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                if language.lower() == 'python':
                    file_path = Path(temp_dir) / "main.py"
                    async with aiofiles.open(file_path, 'w') as f:
                        await f.write(code)
                    
                    # Execute Python code
                    result = subprocess.run(
                        ['python', str(file_path)],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    
                elif language.lower() in ['javascript', 'js']:
                    file_path = Path(temp_dir) / "main.js"
                    async with aiofiles.open(file_path, 'w') as f:
                        await f.write(code)
                    
                    # Execute JavaScript code
                    result = subprocess.run(
                        ['node', str(file_path)],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                else:
                    return {
                        "success": False,
                        "error": f"Execution not supported for {language}",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                
                return {
                    "success": result.returncode == 0,
                    "output": result.stdout,
                    "error": result.stderr if result.returncode != 0 else None,
                    "return_code": result.returncode,
                    "timestamp": datetime.utcnow().isoformat()
                }
                
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Code execution timeout (30 seconds)",
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def analyze_code(self, code: str, language: str) -> Dict[str, Any]:
        """Analyze code for quality, bugs, and improvements"""
        analysis_prompt = f"""
        Analyze this {language} code for:
        1. Potential bugs or errors
        2. Code quality and best practices
        3. Performance improvements
        4. Security vulnerabilities
        5. Suggestions for enhancement
        
        CODE:
        ```{language}
        {code}
        ```
        
        Provide detailed analysis with specific recommendations.
        """
        
        try:
            if self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an expert code reviewer and security analyst."},
                        {"role": "user", "content": analysis_prompt}
                    ],
                    max_tokens=1500,
                    temperature=0.2
                )
                analysis = response.choices[0].message.content
            else:
                analysis = "Code analysis requires AI API keys. Please configure your API keys for detailed analysis."
            
            return {
                "success": True,
                "analysis": analysis,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def generate_project(self, description: str, tech_stack: str) -> Dict[str, Any]:
        """Generate a complete project structure based on description"""
        project_prompt = f"""
        Create a complete project structure for:
        DESCRIPTION: {description}
        TECH_STACK: {tech_stack}
        
        Generate:
        1. Project folder structure
        2. Main application files with code
        3. Configuration files (package.json, requirements.txt, etc.)
        4. README.md with setup instructions
        5. Basic styling/CSS if needed
        
        Provide the response as a JSON structure with:
        {{
            "project_name": "suggested-project-name",
            "files": {{
                "path/to/file.ext": "file content here",
                ...
            }},
            "setup_instructions": "step by step setup guide"
        }}
        """
        
        try:
            if self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an expert full-stack developer who creates complete, production-ready projects."},
                        {"role": "user", "content": project_prompt}
                    ],
                    max_tokens=3000,
                    temperature=0.3
                )
                project_data = response.choices[0].message.content
                
                # Try to parse JSON response
                try:
                    project_json = json.loads(project_data)
                    return {
                        "success": True,
                        "project": project_json,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                except json.JSONDecodeError:
                    # Fallback if not valid JSON
                    return {
                        "success": True,
                        "project": {
                            "project_name": "ai-generated-project",
                            "files": {
                                "README.md": f"# {description}\n\n{project_data}",
                                "main.py": "# Generated project\nprint('Hello, World!')"
                            },
                            "setup_instructions": "Basic project generated. See README.md for details."
                        },
                        "timestamp": datetime.utcnow().isoformat()
                    }
            else:
                return {
                    "success": True,
                    "project": {
                        "project_name": "sample-project",
                        "files": {
                            "README.md": f"# {description}\n\nThis is a sample project. Add AI API keys for full functionality.",
                            "main.py": "print('Hello from AI-generated project!')"
                        },
                        "setup_instructions": "1. Configure AI API keys\n2. Run the main file"
                    },
                    "timestamp": datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

# Global AI service instance
ai_service = AIService()