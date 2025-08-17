from typing import Dict, Any, List, Optional, Set
import yaml
import re
from datetime import datetime
from services.ai_service import ai_service
from core.config import settings
import logging

logger = logging.getLogger(__name__)

class PipelineService:
    """Enhanced service for AI-powered CI/CD pipeline optimization and generation"""
    
    def __init__(self):
        self.max_file_size = settings.MAX_DIFF_SIZE
        
        # Pipeline generation templates and patterns
        self.framework_patterns = {
            'react': ['package.json', 'src/', 'public/', 'build/', 'node_modules/'],
            'vue': ['package.json', 'src/', 'public/', 'dist/', 'vue.config.js'],
            'angular': ['package.json', 'src/', 'angular.json', 'dist/'],
            'django': ['manage.py', 'requirements.txt', 'settings.py', 'wsgi.py'],
            'flask': ['app.py', 'requirements.txt', 'wsgi.py'],
            'fastapi': ['main.py', 'requirements.txt', 'app/', 'routers/'],
            'spring': ['pom.xml', 'src/main/java/', 'application.properties'],
            'express': ['package.json', 'server.js', 'app.js', 'routes/'],
            'nextjs': ['package.json', 'next.config.js', 'pages/', 'app/'],
            'nuxt': ['package.json', 'nuxt.config.js', 'pages/', 'components/'],
            'go': ['go.mod', 'main.go', 'cmd/', 'pkg/'],
            'rust': ['Cargo.toml', 'src/', 'target/'],
            'dotnet': ['*.csproj', '*.sln', 'Program.cs'],
            'laravel': ['composer.json', 'artisan', 'app/', 'routes/'],
            'rails': ['Gemfile', 'config.ru', 'app/', 'config/'],
            'docker': ['Dockerfile', 'docker-compose.yml', '.dockerignore']
        }
        
    async def optimize(self, filename: str, content: bytes) -> Dict[str, Any]:
        """
        Analyze CI/CD pipeline YAML and provide optimization suggestions.
        """
        try:
            # Decode and validate content
            text_content = content.decode('utf-8')
            
            if len(text_content) > self.max_file_size:
                return {
                    "status": "error",
                    "message": f"Pipeline file too large. Maximum size: {self.max_file_size} characters"
                }
            
            # Parse YAML content
            pipeline_data = self._parse_yaml(text_content)
            if pipeline_data.get("error"):
                return {
                    "status": "error",
                    "message": f"YAML parsing error: {pipeline_data['error']}"
                }
            
            # Analyze pipeline structure
            structure_analysis = self._analyze_pipeline_structure(pipeline_data["parsed"])
            
            # Generate AI-powered optimization suggestions
            ai_analysis = await self._generate_ai_optimization(text_content, filename, structure_analysis)
            
            # Perform static analysis for common patterns
            static_analysis = self._perform_static_analysis(text_content, pipeline_data["parsed"])
            
            # Calculate optimization metrics
            metrics = self._calculate_optimization_metrics(structure_analysis, ai_analysis, static_analysis)
            
            response = {
                "status": "success",
                "filename": filename,
                "timestamp": datetime.now().isoformat(),
                "analysis": {
                    "summary": ai_analysis.get("summary", "Pipeline optimization completed"),
                    "pipeline_type": structure_analysis.get("pipeline_type", "unknown"),
                    "structure": structure_analysis,
                    "ai_recommendations": ai_analysis.get("recommendations", []),
                    "optimization_opportunities": ai_analysis.get("optimization_opportunities", []),
                    "performance_improvements": ai_analysis.get("performance_improvements", []),
                    "security_enhancements": ai_analysis.get("security_enhancements", []),
                    "cost_optimizations": ai_analysis.get("cost_optimizations", []),
                    "static_analysis": static_analysis,
                    "metrics": metrics
                },
                "ai_agent": "PipelineOptimizerAgent-v2.0",
                "model_used": settings.AI_MODEL
            }
            
            return response
            
        except Exception as e:
            logger.error(f"Pipeline optimization failed: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to optimize pipeline: {str(e)}"
            }
    
    async def generate_pipeline(self, project_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a custom CI/CD pipeline based on project requirements and codebase analysis.
        
        Args:
            project_info: Dictionary containing:
                - codebase_files: List of files in the project
                - requirements: User requirements and preferences
                - deployment_target: Where to deploy (AWS, Azure, GCP, etc.)
                - team_size: Small, Medium, Large
                - environment: Development workflow preferences
        """
        try:
            # Analyze the codebase to detect technologies
            tech_stack = self._analyze_tech_stack(project_info.get('codebase_files', []))
            
            # Extract user requirements
            requirements = project_info.get('requirements', {})
            deployment_target = project_info.get('deployment_target', 'generic')
            team_size = project_info.get('team_size', 'small')
            
            # Generate AI-powered pipeline recommendation
            pipeline_spec = await self._generate_pipeline_specification(
                tech_stack, requirements, deployment_target, team_size
            )
            
            # Generate the actual pipeline YAML
            generated_pipelines = self._generate_pipeline_templates(pipeline_spec)
            
            # Calculate pipeline metrics and recommendations
            metrics = self._calculate_generation_metrics(tech_stack, pipeline_spec)
            
            response = {
                "status": "success",
                "timestamp": datetime.now().isoformat(),
                "analysis": {
                    "detected_technologies": tech_stack,
                    "pipeline_specification": pipeline_spec,
                    "generated_pipelines": generated_pipelines,
                    "recommendations": pipeline_spec.get("recommendations", []),
                    "best_practices": pipeline_spec.get("best_practices", []),
                    "security_considerations": pipeline_spec.get("security", []),
                    "performance_optimizations": pipeline_spec.get("performance", []),
                    "metrics": metrics
                },
                "ai_agent": "PipelineGeneratorAgent-v2.0",
                "model_used": settings.AI_MODEL
            }
            
            return response
            
        except Exception as e:
            logger.error(f"Pipeline generation failed: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to generate pipeline: {str(e)}"
            }
    
    def _parse_yaml(self, yaml_content: str) -> Dict[str, Any]:
        """Parse YAML content and handle errors gracefully"""
        try:
            parsed = yaml.safe_load(yaml_content)
            return {
                "parsed": parsed,
                "error": None
            }
        except yaml.YAMLError as e:
            return {
                "parsed": None,
                "error": str(e)
            }
    
    def _analyze_pipeline_structure(self, pipeline_data: Dict) -> Dict[str, Any]:
        """Analyze the structure of the pipeline to identify type and components"""
        if not pipeline_data:
            return {"pipeline_type": "unknown", "jobs": 0, "steps": 0}
        
        analysis = {
            "pipeline_type": self._detect_pipeline_type(pipeline_data),
            "jobs": 0,
            "steps": 0,
            "dependencies": [],
            "parallel_opportunities": [],
            "resource_usage": {},
            "triggers": [],
            "environments": set(),
            "secrets_used": [],
            "caching_present": False,
            "artifacts_used": False
        }
        
        # GitHub Actions analysis
        if "jobs" in pipeline_data:
            analysis["jobs"] = len(pipeline_data["jobs"])
            jobs = pipeline_data["jobs"]
            
            for job_name, job_config in jobs.items():
                if isinstance(job_config, dict):
                    # Count steps
                    steps = job_config.get("steps", [])
                    analysis["steps"] += len(steps) if isinstance(steps, list) else 0
                    
                    # Analyze dependencies
                    needs = job_config.get("needs", [])
                    if needs:
                        if isinstance(needs, str):
                            needs = [needs]
                        analysis["dependencies"].extend([(need, job_name) for need in needs])
                    
                    # Check for resource specifications
                    runs_on = job_config.get("runs-on", "")
                    if runs_on:
                        analysis["resource_usage"][job_name] = runs_on
                    
                    # Check for caching and artifacts
                    for step in steps if isinstance(steps, list) else []:
                        if isinstance(step, dict):
                            uses = step.get("uses", "")
                            if "cache" in uses.lower():
                                analysis["caching_present"] = True
                            if "artifact" in uses.lower():
                                analysis["artifacts_used"] = True
                            
                            # Check for secrets
                            step_content = str(step)
                            if "secrets." in step_content or "${{ secrets." in step_content:
                                analysis["secrets_used"].append(job_name)
        
        # GitLab CI analysis
        elif "stages" in pipeline_data or any(key.startswith(".") or "script" in str(value) for key, value in pipeline_data.items()):
            analysis["pipeline_type"] = "gitlab-ci"
            job_count = 0
            step_count = 0
            
            for key, value in pipeline_data.items():
                if isinstance(value, dict) and "script" in value:
                    job_count += 1
                    script = value.get("script", [])
                    step_count += len(script) if isinstance(script, list) else 1
                    
                    # Check dependencies
                    needs = value.get("needs", [])
                    dependencies = value.get("dependencies", [])
                    if needs or dependencies:
                        analysis["dependencies"].extend([(dep, key) for dep in (needs + dependencies)])
            
            analysis["jobs"] = job_count
            analysis["steps"] = step_count
        
        # Convert sets to lists for JSON serialization
        analysis["environments"] = list(analysis["environments"])
        
        return analysis
    
    def _detect_pipeline_type(self, pipeline_data: Dict) -> str:
        """Detect the type of CI/CD pipeline"""
        if "jobs" in pipeline_data and "on" in pipeline_data:
            return "github-actions"
        elif "stages" in pipeline_data or any("script" in str(v) for v in pipeline_data.values() if isinstance(v, dict)):
            return "gitlab-ci"
        elif "pipeline" in pipeline_data or "agent" in pipeline_data:
            return "azure-devops"
        elif "pipeline" in pipeline_data and "stages" in pipeline_data:
            return "jenkins"
        else:
            return "generic"
    
    async def _generate_ai_optimization(self, yaml_content: str, filename: str, structure: Dict) -> Dict[str, Any]:
        """Generate AI-powered pipeline optimization recommendations"""
        
        system_prompt = """You are an expert DevOps engineer specializing in CI/CD pipeline optimization. You have deep knowledge of:
- GitHub Actions, GitLab CI, Jenkins, Azure DevOps
- Performance optimization strategies
- Cost reduction techniques
- Security best practices
- Parallel execution strategies
- Caching and artifact management

Analyze the provided pipeline configuration and provide optimization recommendations.

Format your response as JSON with the following structure:
{
    "summary": "Brief summary of the pipeline and optimization potential",
    "recommendations": [
        {
            "category": "performance|cost|security|maintainability",
            "priority": "critical|high|medium|low",
            "title": "Short recommendation title",
            "description": "Detailed description of the issue",
            "solution": "Specific solution to implement",
            "estimated_impact": "Expected improvement (time/cost/security)",
            "complexity": "low|medium|high"
        }
    ],
    "optimization_opportunities": [
        {
            "type": "parallelization|caching|resource-optimization|dependency-management",
            "current_state": "Description of current implementation",
            "optimized_state": "Description of optimized implementation",
            "benefit": "Expected benefit",
            "implementation": "How to implement the change"
        }
    ],
    "performance_improvements": [
        {
            "area": "build-time|resource-usage|network|storage",
            "current_metric": "Current performance metric",
            "target_metric": "Target performance metric",
            "improvement": "Specific improvement strategy"
        }
    ],
    "security_enhancements": [
        {
            "issue": "Description of security concern",
            "risk_level": "critical|high|medium|low",
            "recommendation": "Security improvement recommendation",
            "implementation": "How to implement the security fix"
        }
    ],
    "cost_optimizations": [
        {
            "area": "compute|storage|network|licensing",
            "current_cost_driver": "What's driving current costs",
            "optimization": "How to reduce costs",
            "estimated_savings": "Expected cost reduction"
        }
    ]
}"""

        user_prompt = f"""Please analyze this CI/CD pipeline configuration:

Filename: {filename}
Pipeline Type: {structure.get('pipeline_type', 'unknown')}
Jobs: {structure.get('jobs', 0)}
Steps: {structure.get('steps', 0)}
Dependencies: {len(structure.get('dependencies', []))}
Caching Present: {structure.get('caching_present', False)}
Artifacts Used: {structure.get('artifacts_used', False)}

Pipeline Configuration:
```yaml
{yaml_content}
```

Provide comprehensive optimization recommendations in the specified JSON format. Focus on:
1. Performance bottlenecks and parallelization opportunities
2. Cost optimization through resource right-sizing
3. Security improvements and best practices
4. Maintainability and reliability enhancements"""

        try:
            ai_response = await ai_service.generate_response(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.1
            )
            
            # Try to parse as JSON, fallback to structured text if needed
            try:
                import json
                return json.loads(ai_response)
            except json.JSONDecodeError:
                return self._parse_ai_text_response(ai_response)
                
        except Exception as e:
            logger.error(f"AI pipeline analysis failed: {str(e)}")
            return {
                "summary": "AI analysis unavailable - using static analysis only",
                "recommendations": [],
                "optimization_opportunities": [],
                "performance_improvements": [],
                "security_enhancements": [],
                "cost_optimizations": []
            }
    
    def _parse_ai_text_response(self, response: str) -> Dict[str, Any]:
        """Parse AI text response when JSON parsing fails"""
        return {
            "summary": "AI provided text analysis (see recommendations for details)",
            "recommendations": [{
                "category": "general",
                "priority": "medium",
                "title": "AI Analysis Available",
                "description": response[:300] + "..." if len(response) > 300 else response,
                "solution": "Review the full AI analysis for specific recommendations",
                "estimated_impact": "Variable based on implementation",
                "complexity": "medium"
            }],
            "optimization_opportunities": [],
            "performance_improvements": [],
            "security_enhancements": [],
            "cost_optimizations": []
        }
    
    def _perform_static_analysis(self, yaml_content: str, pipeline_data: Dict) -> Dict[str, Any]:
        """Perform static analysis on the pipeline configuration"""
        analysis = {
            "issues": [],
            "patterns": [],
            "best_practices": [],
            "security_concerns": []
        }
        
        lines = yaml_content.split('\n')
        
        # Check for common anti-patterns
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            
            # Security issues
            if any(pattern in line_lower for pattern in ['password:', 'secret:', 'token:', 'key:']):
                if '=' in line or ':' in line:
                    if not any(secure in line_lower for secure in ['${{', 'secrets.', 'vault:', 'env.']):
                        analysis["security_concerns"].append({
                            "line": i + 1,
                            "issue": "Potential hardcoded credential",
                            "severity": "high",
                            "recommendation": "Use secrets management or environment variables"
                        })
            
            # Performance anti-patterns
            if 'npm install' in line_lower or 'pip install' in line_lower:
                analysis["patterns"].append({
                    "line": i + 1,
                    "pattern": "dependency_installation",
                    "suggestion": "Consider using dependency caching to speed up builds"
                })
            
            # Resource optimization
            if 'ubuntu-latest' in line_lower:
                analysis["patterns"].append({
                    "line": i + 1,
                    "pattern": "generic_runner",
                    "suggestion": "Consider using specific runner versions for consistency"
                })
        
        # Analyze pipeline structure for optimization opportunities
        if pipeline_data and isinstance(pipeline_data, dict):
            # Check for sequential jobs that could be parallel
            if "jobs" in pipeline_data:
                jobs = pipeline_data["jobs"]
                sequential_jobs = []
                
                for job_name, job_config in jobs.items():
                    if isinstance(job_config, dict):
                        needs = job_config.get("needs", [])
                        if not needs:  # Jobs without dependencies could potentially run in parallel
                            sequential_jobs.append(job_name)
                
                if len(sequential_jobs) > 1:
                    analysis["best_practices"].append({
                        "category": "parallelization",
                        "suggestion": f"Consider parallelizing independent jobs: {', '.join(sequential_jobs)}",
                        "impact": "Could reduce overall pipeline execution time"
                    })
        
        return analysis
    
    def _calculate_optimization_metrics(self, structure: Dict, ai_analysis: Dict, static_analysis: Dict) -> Dict[str, Any]:
        """Calculate pipeline optimization metrics"""
        
        # Base optimization score
        base_score = 7.0
        
        # Deduct points for issues
        security_issues = len(static_analysis.get("security_concerns", []))
        performance_issues = len([p for p in static_analysis.get("patterns", []) if "caching" in p.get("suggestion", "")])
        
        # Calculate optimization potential
        optimization_score = max(1.0, base_score - (security_issues * 1.5) - (performance_issues * 0.5))
        
        # Estimate time savings potential
        jobs_count = structure.get("jobs", 0)
        has_caching = structure.get("caching_present", False)
        has_artifacts = structure.get("artifacts_used", False)
        
        time_savings_potential = 0
        if not has_caching and jobs_count > 0:
            time_savings_potential += 30  # 30% potential savings with caching
        if not has_artifacts and jobs_count > 1:
            time_savings_potential += 20  # 20% potential savings with proper artifacts
        
        # Calculate complexity score
        complexity = "low"
        if jobs_count > 5 or len(structure.get("dependencies", [])) > 3:
            complexity = "medium"
        if jobs_count > 10 or len(structure.get("dependencies", [])) > 8:
            complexity = "high"
        
        return {
            "optimization_score": round(optimization_score, 1),
            "time_savings_potential": f"{min(time_savings_potential, 70)}%",  # Cap at 70%
            "complexity": complexity,
            "jobs_analyzed": jobs_count,
            "steps_analyzed": structure.get("steps", 0),
            "security_issues_found": security_issues,
            "performance_opportunities": performance_issues,
            "parallelization_potential": len(structure.get("parallel_opportunities", [])),
            "overall_health": "excellent" if optimization_score >= 8.5 else "good" if optimization_score >= 7.0 else "needs_improvement"
        }
    
    # ==================== PIPELINE GENERATION METHODS ====================
    
    def _analyze_tech_stack(self, codebase_files: List[str]) -> Dict[str, Any]:
        """Analyze codebase files to detect technologies, frameworks, and tools"""
        tech_stack = {
            "languages": [],
            "frameworks": [],
            "databases": [],
            "deployment_tools": [],
            "testing_frameworks": [],
            "build_tools": [],
            "package_managers": [],
            "confidence_score": 0.0
        }
        
        file_extensions = {}
        framework_matches = {}
        
        # Analyze file patterns
        for file_path in codebase_files:
            file_lower = file_path.lower()
            
            # Extract file extensions
            if '.' in file_path:
                ext = file_path.split('.')[-1].lower()
                file_extensions[ext] = file_extensions.get(ext, 0) + 1
            
            # Check for framework patterns
            for framework, patterns in self.framework_patterns.items():
                for pattern in patterns:
                    if pattern.lower() in file_lower:
                        framework_matches[framework] = framework_matches.get(framework, 0) + 1
        
        # Detect languages from file extensions
        language_map = {
            'js': 'JavaScript', 'ts': 'TypeScript', 'jsx': 'React', 'tsx': 'React TypeScript',
            'py': 'Python', 'java': 'Java', 'go': 'Go', 'rs': 'Rust', 'cs': 'C#',
            'php': 'PHP', 'rb': 'Ruby', 'cpp': 'C++', 'c': 'C', 'swift': 'Swift',
            'kt': 'Kotlin', 'scala': 'Scala', 'clj': 'Clojure', 'hs': 'Haskell'
        }
        
        for ext, count in file_extensions.items():
            if ext in language_map and count > 0:
                tech_stack["languages"].append({
                    "name": language_map[ext],
                    "confidence": min(count / len(codebase_files), 1.0),
                    "file_count": count
                })
        
        # Detect frameworks
        for framework, matches in framework_matches.items():
            confidence = min(matches / len(self.framework_patterns[framework]), 1.0)
            if confidence > 0.3:  # Only include if reasonably confident
                tech_stack["frameworks"].append({
                    "name": framework,
                    "confidence": confidence,
                    "matches": matches
                })
        
        # Detect specific tools and databases
        tool_patterns = {
            'docker': ['dockerfile', 'docker-compose'],
            'kubernetes': ['deployment.yaml', 'service.yaml', 'ingress.yaml'],
            'terraform': ['main.tf', 'variables.tf', 'outputs.tf'],
            'ansible': ['playbook.yml', 'inventory'],
            'jenkins': ['jenkinsfile', 'jenkins'],
            'github-actions': ['.github/workflows'],
            'gitlab-ci': ['.gitlab-ci.yml'],
            'pytest': ['test_', 'pytest.ini'],
            'jest': ['jest.config', '__tests__'],
            'mysql': ['mysql', 'my.cnf'],
            'postgresql': ['postgresql', 'postgres'],
            'redis': ['redis.conf', 'redis'],
            'mongodb': ['mongo', 'mongodb']
        }
        
        for tool, patterns in tool_patterns.items():
            for pattern in patterns:
                matches = sum(1 for f in codebase_files if pattern in f.lower())
                if matches > 0:
                    category = self._categorize_tool(tool)
                    tech_stack[category].append({
                        "name": tool,
                        "confidence": min(matches / 5, 1.0),  # Normalize confidence
                        "matches": matches
                    })
        
        # Calculate overall confidence
        total_detections = (len(tech_stack["languages"]) + len(tech_stack["frameworks"]) + 
                          len(tech_stack["databases"]) + len(tech_stack["deployment_tools"]))
        tech_stack["confidence_score"] = min(total_detections / 10, 1.0)
        
        return tech_stack
    
    def _categorize_tool(self, tool: str) -> str:
        """Categorize a detected tool into the appropriate category"""
        categories = {
            "deployment_tools": ["docker", "kubernetes", "terraform", "ansible"],
            "testing_frameworks": ["pytest", "jest", "mocha", "junit"],
            "build_tools": ["webpack", "vite", "gulp", "grunt", "maven", "gradle"],
            "databases": ["mysql", "postgresql", "redis", "mongodb", "sqlite"]
        }
        
        for category, tools in categories.items():
            if tool in tools:
                return category
        return "deployment_tools"  # Default category
    
    async def _generate_pipeline_specification(
        self, 
        tech_stack: Dict, 
        requirements: Dict, 
        deployment_target: str, 
        team_size: str
    ) -> Dict[str, Any]:
        """Generate AI-powered pipeline specification based on detected tech stack and requirements"""
        
        system_prompt = """You are an expert DevOps architect specializing in CI/CD pipeline design. You have extensive experience with:
- Multi-platform CI/CD systems (GitHub Actions, GitLab CI, Jenkins, Azure DevOps)
- Cloud deployment strategies (AWS, Azure, GCP, hybrid)
- Modern development practices (containerization, microservices, IaC)
- Security best practices and compliance
- Performance optimization and cost management

Based on the provided technology stack and requirements, design a comprehensive CI/CD pipeline specification.

Format your response as JSON with the following structure:
{
    "pipeline_type": "github-actions|gitlab-ci|azure-devops|jenkins",
    "stages": [
        {
            "name": "stage_name",
            "description": "What this stage does",
            "jobs": [
                {
                    "name": "job_name",
                    "description": "Job description",
                    "dependencies": ["job1", "job2"],
                    "parallel": true,
                    "steps": ["step1", "step2", "step3"],
                    "estimated_time": "5 minutes",
                    "resources": {"cpu": "2", "memory": "4GB"}
                }
            ]
        }
    ],
    "recommendations": [
        {
            "category": "performance|security|cost|maintainability",
            "title": "Recommendation title",
            "description": "Detailed recommendation",
            "implementation": "How to implement",
            "priority": "critical|high|medium|low"
        }
    ],
    "best_practices": [
        {
            "practice": "Best practice name",
            "description": "Why this is important",
            "implementation": "How to implement"
        }
    ],
    "security": [
        {
            "concern": "Security consideration",
            "mitigation": "How to address it",
            "tools": ["tool1", "tool2"]
        }
    ],
    "performance": [
        {
            "optimization": "Performance optimization",
            "benefit": "Expected benefit",
            "implementation": "How to implement"
        }
    ],
    "estimated_metrics": {
        "total_pipeline_time": "15-20 minutes",
        "parallel_efficiency": "70%",
        "cost_per_run": "$0.50",
        "success_rate": "95%"
    }
}"""

        # Build the user prompt with detailed context
        languages_str = ", ".join([lang["name"] for lang in tech_stack.get("languages", [])])
        frameworks_str = ", ".join([fw["name"] for fw in tech_stack.get("frameworks", [])])
        databases_str = ", ".join([db["name"] for db in tech_stack.get("databases", [])])
        
        user_prompt = f"""Design a CI/CD pipeline for the following project:

**Technology Stack:**
- Languages: {languages_str or 'Not detected'}
- Frameworks: {frameworks_str or 'Not detected'}  
- Databases: {databases_str or 'Not detected'}
- Deployment Tools: {', '.join([tool["name"] for tool in tech_stack.get("deployment_tools", [])])}

**Requirements:**
- Deployment Target: {deployment_target}
- Team Size: {team_size}
- Testing Requirements: {requirements.get('testing', 'Standard unit and integration tests')}
- Security Requirements: {requirements.get('security', 'Standard security scanning')}
- Performance Requirements: {requirements.get('performance', 'Optimized for development speed')}
- Compliance: {requirements.get('compliance', 'None specified')}

**Additional Context:**
- Budget Constraints: {requirements.get('budget', 'Standard')}
- Deployment Frequency: {requirements.get('deployment_frequency', 'Daily')}
- Environment Count: {requirements.get('environments', 'Dev, Staging, Production')}

Please generate a comprehensive pipeline specification optimized for this technology stack and requirements. Include specific steps, tools, and configurations."""

        try:
            ai_response = await ai_service.generate_response(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.2  # Lower temperature for more consistent pipeline generation
            )
            
            try:
                import json
                return json.loads(ai_response)
            except json.JSONDecodeError:
                return self._generate_fallback_pipeline_spec(tech_stack, requirements, deployment_target)
                
        except Exception as e:
            logger.error(f"AI pipeline specification generation failed: {str(e)}")
            return self._generate_fallback_pipeline_spec(tech_stack, requirements, deployment_target)
    
    def _generate_fallback_pipeline_spec(self, tech_stack: Dict, requirements: Dict, deployment_target: str) -> Dict[str, Any]:
        """Generate a fallback pipeline specification when AI is unavailable"""
        
        # Determine primary language/framework
        primary_framework = None
        if tech_stack.get("frameworks"):
            primary_framework = tech_stack["frameworks"][0]["name"]
        elif tech_stack.get("languages"):
            primary_lang = tech_stack["languages"][0]["name"].lower()
            if "javascript" in primary_lang or "typescript" in primary_lang:
                primary_framework = "node"
            elif "python" in primary_lang:
                primary_framework = "python"
            elif "java" in primary_lang:
                primary_framework = "java"
        
        # Generate basic pipeline structure
        spec = {
            "pipeline_type": "github-actions",
            "stages": [
                {
                    "name": "Build & Test",
                    "description": "Install dependencies, build, and run tests",
                    "jobs": [
                        {
                            "name": "test",
                            "description": "Run unit and integration tests",
                            "dependencies": [],
                            "parallel": False,
                            "steps": self._get_framework_build_steps(primary_framework),
                            "estimated_time": "5-8 minutes",
                            "resources": {"cpu": "2", "memory": "4GB"}
                        }
                    ]
                },
                {
                    "name": "Security & Quality",
                    "description": "Security scanning and code quality checks",
                    "jobs": [
                        {
                            "name": "security-scan",
                            "description": "Run security vulnerability scans",
                            "dependencies": [],
                            "parallel": True,
                            "steps": ["Dependency vulnerability scan", "SAST scanning", "License compliance check"],
                            "estimated_time": "3-5 minutes",
                            "resources": {"cpu": "1", "memory": "2GB"}
                        }
                    ]
                },
                {
                    "name": "Deploy",
                    "description": f"Deploy to {deployment_target}",
                    "jobs": [
                        {
                            "name": "deploy",
                            "description": f"Deploy application to {deployment_target}",
                            "dependencies": ["test", "security-scan"],
                            "parallel": False,
                            "steps": self._get_deployment_steps(deployment_target),
                            "estimated_time": "5-10 minutes",
                            "resources": {"cpu": "1", "memory": "2GB"}
                        }
                    ]
                }
            ],
            "recommendations": [
                {
                    "category": "performance",
                    "title": "Add Dependency Caching",
                    "description": "Cache dependencies to reduce build times",
                    "implementation": "Use GitHub Actions cache action for node_modules, pip cache, etc.",
                    "priority": "high"
                },
                {
                    "category": "security", 
                    "title": "Implement Secret Management",
                    "description": "Use proper secret management for credentials",
                    "implementation": "Store secrets in GitHub Secrets, use environment-specific configs",
                    "priority": "critical"
                }
            ],
            "best_practices": [
                {
                    "practice": "Parallel Job Execution",
                    "description": "Run independent jobs in parallel to reduce total pipeline time",
                    "implementation": "Structure jobs to minimize dependencies and maximize parallelism"
                }
            ],
            "security": [
                {
                    "concern": "Dependency vulnerabilities",
                    "mitigation": "Regular dependency scanning and updates",
                    "tools": ["npm audit", "safety", "OWASP dependency check"]
                }
            ],
            "performance": [
                {
                    "optimization": "Build caching",
                    "benefit": "30-50% reduction in build times",
                    "implementation": "Cache dependencies and build artifacts between runs"
                }
            ],
            "estimated_metrics": {
                "total_pipeline_time": "12-20 minutes",
                "parallel_efficiency": "60%",
                "cost_per_run": "$0.30",
                "success_rate": "90%"
            }
        }
        
        return spec
    
    def _get_framework_build_steps(self, framework: str) -> List[str]:
        """Get build steps for a specific framework"""
        framework_steps = {
            "react": [
                "Checkout code",
                "Setup Node.js",
                "Cache dependencies",
                "Install dependencies",
                "Run tests",
                "Build application",
                "Upload build artifacts"
            ],
            "python": [
                "Checkout code", 
                "Setup Python",
                "Cache pip dependencies",
                "Install dependencies",
                "Run tests with pytest",
                "Generate coverage report",
                "Build package"
            ],
            "java": [
                "Checkout code",
                "Setup JDK",
                "Cache Maven dependencies", 
                "Run tests",
                "Generate test reports",
                "Build JAR",
                "Upload artifacts"
            ],
            "go": [
                "Checkout code",
                "Setup Go",
                "Cache Go modules",
                "Download dependencies",
                "Run tests",
                "Build binary",
                "Upload binary"
            ]
        }
        
        return framework_steps.get(framework, [
            "Checkout code",
            "Setup build environment", 
            "Install dependencies",
            "Run tests",
            "Build application"
        ])
    
    def _get_deployment_steps(self, deployment_target: str) -> List[str]:
        """Get deployment steps for a specific target"""
        deployment_steps = {
            "aws": [
                "Configure AWS credentials",
                "Build Docker image", 
                "Push to ECR",
                "Deploy to ECS/EKS",
                "Run health checks",
                "Update load balancer"
            ],
            "azure": [
                "Configure Azure credentials",
                "Build Docker image",
                "Push to ACR", 
                "Deploy to AKS/Container Instances",
                "Verify deployment"
            ],
            "gcp": [
                "Configure GCP credentials",
                "Build Docker image",
                "Push to GCR",
                "Deploy to GKE/Cloud Run",
                "Verify deployment"
            ],
            "heroku": [
                "Setup Heroku CLI",
                "Deploy to Heroku",
                "Run database migrations",
                "Verify deployment"
            ],
            "vercel": [
                "Install Vercel CLI",
                "Deploy to Vercel", 
                "Verify deployment"
            ]
        }
        
        return deployment_steps.get(deployment_target.lower(), [
            "Prepare deployment artifacts",
            "Deploy to target environment",
            "Run post-deployment tests",
            "Verify deployment health"
        ])
    
    def _generate_pipeline_templates(self, pipeline_spec: Dict) -> Dict[str, str]:
        """Generate actual pipeline YAML templates from the specification"""
        
        templates = {}
        
        # Generate GitHub Actions workflow
        if pipeline_spec.get("pipeline_type") == "github-actions":
            templates["github-actions"] = self._generate_github_actions_yaml(pipeline_spec)
        
        # Generate GitLab CI template
        templates["gitlab-ci"] = self._generate_gitlab_ci_yaml(pipeline_spec)
        
        # Generate generic template
        templates["generic"] = self._generate_generic_pipeline_yaml(pipeline_spec)
        
        return templates
    
    def _generate_github_actions_yaml(self, spec: Dict) -> str:
        """Generate GitHub Actions workflow YAML"""
        
        workflow = f"""name: {spec.get('name', 'CI/CD Pipeline')}

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: '18'
  PYTHON_VERSION: '3.9'

jobs:"""

        # Generate jobs from specification
        for stage in spec.get("stages", []):
            for job in stage.get("jobs", []):
                job_name = job["name"].replace("-", "_")
                workflow += f"""
  {job_name}:
    runs-on: ubuntu-latest"""
                
                if job.get("dependencies"):
                    deps = ", ".join(job["dependencies"])
                    workflow += f"""
    needs: [{deps}]"""
                
                workflow += f"""
    steps:"""
                
                for step in job.get("steps", []):
                    workflow += f"""
      - name: {step}
        run: echo "Executing: {step}" """
        
        return workflow
    
    def _generate_gitlab_ci_yaml(self, spec: Dict) -> str:
        """Generate GitLab CI YAML"""
        
        pipeline = f"""# GitLab CI Pipeline
stages:"""
        
        # Add stages
        for stage in spec.get("stages", []):
            pipeline += f"""
  - {stage["name"].lower().replace(" ", "-")}"""
        
        pipeline += """

variables:
  NODE_VERSION: "18"
  PYTHON_VERSION: "3.9"
"""
        
        # Add jobs
        for stage in spec.get("stages", []):
            for job in stage.get("jobs", []):
                job_name = job["name"].replace("-", "_")
                pipeline += f"""
{job_name}:
  stage: {stage["name"].lower().replace(" ", "-")}
  script:"""
                
                for step in job.get("steps", []):
                    pipeline += f"""
    - echo "Executing: {step}" """
        
        return pipeline
    
    def _generate_generic_pipeline_yaml(self, spec: Dict) -> str:
        """Generate a generic pipeline description"""
        
        pipeline = f"""# Generic CI/CD Pipeline Specification
# This can be adapted to any CI/CD platform

Pipeline: {spec.get('name', 'Custom Pipeline')}
Estimated Time: {spec.get('estimated_metrics', {}).get('total_pipeline_time', 'Unknown')}

Stages:"""
        
        for i, stage in enumerate(spec.get("stages", []), 1):
            pipeline += f"""
{i}. {stage["name"]}:
   Description: {stage["description"]}
   Jobs:"""
            
            for job in stage.get("jobs", []):
                pipeline += f"""
     - {job["name"]}: {job["description"]}
       Steps: {", ".join(job.get("steps", []))}
       Estimated Time: {job.get("estimated_time", "Unknown")}"""
        
        return pipeline
    
    def _calculate_generation_metrics(self, tech_stack: Dict, pipeline_spec: Dict) -> Dict[str, Any]:
        """Calculate metrics for the generated pipeline"""
        
        total_jobs = sum(len(stage.get("jobs", [])) for stage in pipeline_spec.get("stages", []))
        total_steps = sum(
            len(job.get("steps", [])) 
            for stage in pipeline_spec.get("stages", []) 
            for job in stage.get("jobs", [])
        )
        
        # Estimate complexity based on tech stack and pipeline structure
        complexity_score = 0
        complexity_score += len(tech_stack.get("languages", [])) * 1
        complexity_score += len(tech_stack.get("frameworks", [])) * 2  
        complexity_score += len(tech_stack.get("databases", [])) * 1.5
        complexity_score += total_jobs * 0.5
        
        complexity = "low" if complexity_score < 5 else "medium" if complexity_score < 10 else "high"
        
        return {
            "tech_stack_confidence": tech_stack.get("confidence_score", 0.0),
            "pipeline_complexity": complexity,
            "total_jobs": total_jobs,
            "total_steps": total_steps,
            "estimated_setup_time": f"{max(30, total_steps * 2)} minutes",
            "maintenance_effort": "low" if total_jobs < 5 else "medium" if total_jobs < 10 else "high",
            "recommended_triggers": ["push to main", "pull request", "scheduled"],
            "optimization_potential": "high" if complexity_score > 8 else "medium",
            "security_coverage": len(pipeline_spec.get("security", [])),
            "performance_optimizations": len(pipeline_spec.get("performance", []))
        }