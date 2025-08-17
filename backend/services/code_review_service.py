from typing import Dict, Any, List, Optional
import json
import re
from datetime import datetime
from services.ai_service import ai_service
from core.config import settings
import logging

logger = logging.getLogger(__name__)

class CodeReviewService:
    """Enhanced service for AI-powered code review analysis"""
    
    def __init__(self):
        self.max_diff_size = settings.MAX_DIFF_SIZE
        
    async def analyze_diff(self, filename: str, content: bytes) -> Dict[str, Any]:
        """
        Analyze code diff using AI and provide comprehensive review suggestions.
        """
        try:
            # Decode and validate content
            text_content = content.decode('utf-8')
            
            if len(text_content) > self.max_diff_size:
                return {
                    "status": "error",
                    "message": f"Diff file too large. Maximum size: {self.max_diff_size} characters"
                }
            
            # Parse the diff to extract meaningful information
            diff_analysis = self._parse_diff(text_content)
            
            # Generate AI-powered analysis
            ai_analysis = await self._generate_ai_analysis(text_content, filename, diff_analysis)
            
            # Combine with static analysis
            static_analysis = self._perform_static_analysis(text_content)
            
            # Calculate metrics
            metrics = self._calculate_metrics(diff_analysis, ai_analysis, static_analysis)
            
            response = {
                "status": "success",
                "filename": filename,
                "timestamp": datetime.now().isoformat(),
                "analysis": {
                    "summary": ai_analysis.get("summary", "Code review completed"),
                    "diff_stats": diff_analysis,
                    "ai_insights": ai_analysis.get("insights", []),
                    "static_analysis": static_analysis,
                    "suggestions": ai_analysis.get("suggestions", []),
                    "security_issues": ai_analysis.get("security_issues", []),
                    "performance_issues": ai_analysis.get("performance_issues", []),
                    "code_quality": ai_analysis.get("code_quality", {}),
                    "metrics": metrics
                },
                "ai_agent": "CodeReviewAgent-v2.0",
                "model_used": settings.AI_MODEL
            }
            
            return response
            
        except Exception as e:
            logger.error(f"Code review analysis failed: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to analyze code diff: {str(e)}"
            }
    
    def _parse_diff(self, diff_content: str) -> Dict[str, Any]:
        """Parse diff content to extract statistics and metadata"""
        lines = diff_content.split('\n')
        
        stats = {
            "total_lines": len(lines),
            "files_changed": 0,
            "lines_added": 0,
            "lines_removed": 0,
            "files": []
        }
        
        current_file = None
        
        for line in lines:
            if line.startswith('diff --git'):
                # Extract file paths
                match = re.search(r'diff --git a/(.*?) b/(.*?)$', line)
                if match:
                    current_file = match.group(2)
                    stats["files_changed"] += 1
                    stats["files"].append({
                        "name": current_file,
                        "additions": 0,
                        "deletions": 0
                    })
            elif line.startswith('+') and not line.startswith('+++'):
                stats["lines_added"] += 1
                if current_file and stats["files"]:
                    stats["files"][-1]["additions"] += 1
            elif line.startswith('-') and not line.startswith('---'):
                stats["lines_removed"] += 1
                if current_file and stats["files"]:
                    stats["files"][-1]["deletions"] += 1
        
        return stats
    
    async def _generate_ai_analysis(self, diff_content: str, filename: str, diff_stats: Dict) -> Dict[str, Any]:
        """Generate AI-powered code analysis"""
        
        system_prompt = """You are an expert code reviewer with deep knowledge of software engineering best practices, security, performance, and code quality. 

Analyze the provided code diff and provide:
1. A brief summary of changes
2. Key insights about the code changes
3. Specific suggestions for improvement
4. Security vulnerabilities or concerns
5. Performance implications
6. Code quality assessment

Format your response as JSON with the following structure:
{
    "summary": "Brief summary of the changes",
    "insights": ["Key insight 1", "Key insight 2"],
    "suggestions": [
        {
            "type": "security|performance|style|logic|testing",
            "severity": "critical|high|medium|low",
            "line_range": "approximate line numbers",
            "issue": "Description of the issue",
            "recommendation": "Specific recommendation to fix",
            "impact": "Potential impact if not addressed"
        }
    ],
    "security_issues": [
        {
            "type": "SQL injection|XSS|Authentication|Authorization|etc",
            "severity": "critical|high|medium|low",
            "description": "Detailed description",
            "mitigation": "How to fix"
        }
    ],
    "performance_issues": [
        {
            "type": "Algorithm|Database|Memory|Network|etc",
            "impact": "high|medium|low",
            "description": "Issue description",
            "optimization": "Suggested optimization"
        }
    ],
    "code_quality": {
        "readability": "excellent|good|fair|poor",
        "maintainability": "excellent|good|fair|poor",
        "testability": "excellent|good|fair|poor",
        "overall_score": 8.5,
        "strengths": ["Strength 1", "Strength 2"],
        "improvements": ["Improvement 1", "Improvement 2"]
    }
}"""

        user_prompt = f"""Please analyze this code diff:

File: {filename}
Files changed: {diff_stats.get('files_changed', 0)}
Lines added: {diff_stats.get('lines_added', 0)}
Lines removed: {diff_stats.get('lines_removed', 0)}

Diff content:
```
{diff_content}
```

Provide a comprehensive code review analysis in the specified JSON format."""

        try:
            ai_response = await ai_service.generate_response(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.1
            )
            
            # Try to parse as JSON, fallback to structured text if needed
            try:
                return json.loads(ai_response)
            except json.JSONDecodeError:
                # If AI doesn't return valid JSON, extract key information
                return self._parse_ai_text_response(ai_response)
                
        except Exception as e:
            logger.error(f"AI analysis failed: {str(e)}")
            return {
                "summary": "AI analysis unavailable - using static analysis only",
                "insights": ["Static analysis completed"],
                "suggestions": [],
                "security_issues": [],
                "performance_issues": [],
                "code_quality": {
                    "overall_score": 6.0,
                    "readability": "fair",
                    "maintainability": "fair",
                    "testability": "fair"
                }
            }
    
    def _parse_ai_text_response(self, response: str) -> Dict[str, Any]:
        """Parse AI text response when JSON parsing fails"""
        return {
            "summary": "AI provided text analysis (see insights for details)",
            "insights": [response[:500] + "..." if len(response) > 500 else response],
            "suggestions": [],
            "security_issues": [],
            "performance_issues": [],
            "code_quality": {
                "overall_score": 7.0,
                "readability": "good",
                "maintainability": "good",
                "testability": "good"
            }
        }
    
    def _perform_static_analysis(self, diff_content: str) -> Dict[str, Any]:
        """Perform basic static analysis on the diff"""
        analysis = {
            "potential_issues": [],
            "complexity_indicators": [],
            "patterns": []
        }
        
        lines = diff_content.split('\n')
        added_lines = [line[1:] for line in lines if line.startswith('+') and not line.startswith('+++')]
        
        # Check for common issues in added lines
        for i, line in enumerate(added_lines):
            line_lower = line.lower().strip()
            
            # Security patterns
            if any(pattern in line_lower for pattern in ['password', 'secret', 'api_key', 'token']):
                if '=' in line and not line_lower.startswith('#'):
                    analysis["potential_issues"].append({
                        "type": "security",
                        "line": i + 1,
                        "issue": "Potential hardcoded credential",
                        "severity": "high"
                    })
            
            # SQL injection patterns
            if any(pattern in line_lower for pattern in ['select *', 'drop table', 'delete from']):
                if 'format' in line_lower or '%s' in line or '".format(' in line:
                    analysis["potential_issues"].append({
                        "type": "security",
                        "line": i + 1,
                        "issue": "Potential SQL injection vulnerability",
                        "severity": "critical"
                    })
            
            # Performance patterns
            if any(pattern in line_lower for pattern in ['for ', 'while ', 'loop']):
                if any(nested in line_lower for nested in ['for ', 'while ', 'select', 'query']):
                    analysis["complexity_indicators"].append({
                        "type": "performance",
                        "line": i + 1,
                        "issue": "Nested loop or query in loop detected",
                        "impact": "medium"
                    })
        
        return analysis
    
    def _calculate_metrics(self, diff_stats: Dict, ai_analysis: Dict, static_analysis: Dict) -> Dict[str, Any]:
        """Calculate comprehensive code quality metrics"""
        
        # Base score from AI analysis
        base_score = ai_analysis.get("code_quality", {}).get("overall_score", 7.0)
        
        # Adjust based on static analysis findings
        critical_issues = len([issue for issue in static_analysis.get("potential_issues", []) 
                             if issue.get("severity") == "critical"])
        high_issues = len([issue for issue in static_analysis.get("potential_issues", []) 
                          if issue.get("severity") == "high"])
        
        # Penalty for issues
        penalty = (critical_issues * 2.0) + (high_issues * 1.0)
        adjusted_score = max(1.0, base_score - penalty)
        
        # Calculate change impact
        total_changes = diff_stats.get("lines_added", 0) + diff_stats.get("lines_removed", 0)
        change_impact = "low" if total_changes < 50 else "medium" if total_changes < 200 else "high"
        
        return {
            "overall_score": round(adjusted_score, 1),
            "security_score": max(1.0, 10.0 - (critical_issues * 3.0) - (high_issues * 1.5)),
            "complexity_score": base_score,  # Could be enhanced with cyclomatic complexity
            "change_impact": change_impact,
            "files_affected": diff_stats.get("files_changed", 0),
            "total_changes": total_changes,
            "risk_level": "high" if critical_issues > 0 else "medium" if high_issues > 0 else "low"
        }