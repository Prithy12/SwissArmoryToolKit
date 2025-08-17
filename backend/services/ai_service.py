"""
AI Service abstraction layer for multiple LLM providers
"""
import asyncio
from typing import Dict, Any, Optional, List
from enum import Enum
import openai
import anthropic
from core.config import settings
import logging

logger = logging.getLogger(__name__)

class AIProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"

class AIService:
    """Unified AI service that can work with multiple LLM providers"""
    
    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        
        # Initialize clients based on available API keys
        if settings.OPENAI_API_KEY:
            self.openai_client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            
        if settings.ANTHROPIC_API_KEY:
            self.anthropic_client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
    
    async def generate_response(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        provider: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> str:
        """
        Generate AI response using the specified or default provider
        """
        provider = provider or settings.DEFAULT_AI_PROVIDER
        max_tokens = max_tokens or settings.MAX_TOKENS
        temperature = temperature or settings.TEMPERATURE
        
        try:
            if provider == AIProvider.OPENAI.value and self.openai_client:
                return await self._generate_openai_response(
                    prompt, system_prompt, max_tokens, temperature
                )
            elif provider == AIProvider.ANTHROPIC.value and self.anthropic_client:
                return await self._generate_anthropic_response(
                    prompt, system_prompt, max_tokens, temperature
                )
            else:
                # Fallback to mock response if no provider available
                logger.warning(f"AI provider {provider} not available, using mock response")
                return await self._generate_mock_response(prompt)
                
        except Exception as e:
            logger.error(f"AI generation failed: {str(e)}")
            return await self._generate_mock_response(prompt)
    
    async def _generate_openai_response(
        self, 
        prompt: str, 
        system_prompt: Optional[str], 
        max_tokens: int, 
        temperature: float
    ) -> str:
        """Generate response using OpenAI"""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        response = await self.openai_client.chat.completions.create(
            model=settings.AI_MODEL,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        return response.choices[0].message.content
    
    async def _generate_anthropic_response(
        self, 
        prompt: str, 
        system_prompt: Optional[str], 
        max_tokens: int, 
        temperature: float
    ) -> str:
        """Generate response using Anthropic Claude"""
        response = await self.anthropic_client.messages.create(
            model=settings.AI_MODEL,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt or "You are a helpful AI assistant.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.content[0].text
    
    async def _generate_mock_response(self, prompt: str) -> str:
        """Generate mock response when no AI provider is available"""
        await asyncio.sleep(0.5)  # Simulate API delay
        
        if "code review" in prompt.lower():
            return """Based on the code diff analysis:

**Issues Found:**
1. **Security**: Potential SQL injection vulnerability in line 15
2. **Performance**: Inefficient loop in the data processing section
3. **Code Style**: Missing error handling for API calls

**Suggestions:**
- Use parameterized queries for database operations
- Consider using list comprehension for better performance
- Add try-catch blocks around external API calls

**Overall Score: 7.2/10**
*Note: This is a mock response. Configure AI provider for real analysis.*"""

        elif "pipeline" in prompt.lower():
            return """Pipeline optimization analysis:

**Optimization Opportunities:**
1. **Parallelization**: Jobs can run in parallel to reduce build time
2. **Caching**: Add dependency caching to speed up builds
3. **Resource Optimization**: Right-size container resources

**Recommendations:**
- Use matrix builds for testing multiple environments
- Implement proper artifact caching strategy
- Consider using faster base images

**Estimated Time Savings: 40%**
*Note: This is a mock response. Configure AI provider for real analysis.*"""

        elif "test" in prompt.lower():
            return """Test generation analysis:

**Generated Test Cases:**
1. **Unit Tests**: 12 new test cases for uncovered functions
2. **Integration Tests**: 5 API endpoint tests
3. **Edge Cases**: 8 boundary condition tests

**Coverage Improvement:**
- Current: 72% → Target: 90%
- Focus areas: Error handling, edge cases, API validation

**Priority Tests:**
- Authentication flow validation
- Database transaction rollback
- Input sanitization

*Note: This is a mock response. Configure AI provider for real analysis.*"""

        return "AI analysis complete. Configure API keys for detailed insights."

# Global AI service instance
ai_service = AIService()
