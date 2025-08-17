# 🛠️ SwissArmory DevOps Toolkit

> **AI-Powered Multi-Agent DevOps Automation Platform**

A comprehensive, intelligent DevOps toolkit that leverages AI to automate code review, pipeline optimization, test generation, and custom CI/CD pipeline creation. Built with FastAPI, React, and integrated with OpenAI/Anthropic for intelligent analysis.

## ✨ Features

### 🔍 **AI-Powered Code Review Agent**
- **Intelligent Diff Analysis**: Parse and analyze code changes with detailed statistics
- **Security Vulnerability Detection**: Identify SQL injection, hardcoded secrets, and security anti-patterns
- **Performance Optimization**: Detect inefficient loops, missing caching, and performance bottlenecks
- **Best Practices Enforcement**: Ensure code quality and maintainability standards
- **Comprehensive Scoring**: Quantitative metrics for code quality, security, and complexity

### ⚙️ **Pipeline Optimization Agent**
- **Multi-Platform Support**: Analyze GitHub Actions, GitLab CI, Jenkins, Azure DevOps pipelines
- **Dependency Analysis**: Map job dependencies and identify parallelization opportunities
- **Performance Optimization**: Detect duplicate installations, missing caching, resource inefficiencies
- **Security Scanning**: Find hardcoded secrets, insecure practices, and compliance issues
- **Cost Optimization**: Suggest resource right-sizing and efficiency improvements

### 🚀 **Custom Pipeline Generation Agent** (NEW!)
- **Tech Stack Detection**: Automatically analyze project files to detect languages, frameworks, and tools
- **Intelligent Pipeline Creation**: Generate custom CI/CD pipelines based on project requirements
- **Multi-Platform Templates**: Create GitHub Actions, GitLab CI, and generic pipeline configurations
- **Enterprise-Grade Features**: Include security scanning, testing, deployment, and monitoring
- **Compliance Ready**: Built-in support for SOC 2, GDPR, and other compliance requirements

### 🧪 **Test Generation Agent**
- **Coverage Analysis**: Parse test coverage reports to identify gaps
- **Intelligent Test Suggestions**: Generate targeted test cases for uncovered code
- **Priority-Based Recommendations**: Focus on critical paths and high-risk areas
- **Framework Agnostic**: Support for Jest, pytest, JUnit, and other testing frameworks

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────────┐    ┌─────────────────────┐
│   React Frontend │    │   FastAPI Backend    │    │   AI/LLM Services   │
│                 │    │                      │    │                     │
│ • Code Review   │◄──►│ • Pipeline Service   │◄──►│ • OpenAI GPT-4      │
│ • Pipeline UI   │    │ • Code Review Service│    │ • Anthropic Claude  │
│ • Test Genie    │    │ • Test Service       │    │ • Intelligent       │
│ • File Upload   │    │ • AI Service Layer   │    │   Fallback System   │
└─────────────────┘    └──────────────────────┘    └─────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- **Python 3.9+**
- **Node.js 18+**
- **npm or yarn**

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
pip install -r requirements.txt
python main.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Access the Application
- **Frontend UI**: http://localhost:5173
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🧪 Testing

### Test Files Included
The repository includes comprehensive test files in the `testing_files/` directory:

- **Code Review**: `code_review_test.diff`, `simple_code_change.diff`
- **Pipeline Optimization**: `pipeline_optimization_test.yml`, `gitlab_pipeline_test.yml`
- **Test Generation**: `test_coverage_report.json`
- **Pipeline Generation**: `pipeline_generation_request.json`

### API Testing
```bash
# Code Review
curl -X POST "http://localhost:8000/api/review" -F "file=@testing_files/code_review_test.diff"

# Pipeline Optimization
curl -X POST "http://localhost:8000/api/pipeline" -F "file=@testing_files/pipeline_optimization_test.yml"

# Custom Pipeline Generation
curl -X POST "http://localhost:8000/api/pipeline/generate" \
  -H "Content-Type: application/json" \
  -d @testing_files/pipeline_generation_request.json
```

## ⚙️ Configuration

### AI Provider Setup (Optional)
Create a `.env` file in the backend directory:
```env
# AI/LLM API Keys (at least one required for full functionality)
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# AI Configuration
DEFAULT_AI_PROVIDER=openai
AI_MODEL=gpt-4o-mini
MAX_TOKENS=4000
TEMPERATURE=0.1
```

**Note**: The system works with intelligent mock responses even without API keys!

## 📊 Key Capabilities

### Real Analysis Examples

**Pipeline Optimization Results:**
- ✅ **5 jobs, 19 steps analyzed** with dependency mapping
- ✅ **50% time savings potential** identified through caching
- ✅ **Security issues detected** (hardcoded secrets, insecure practices)
- ✅ **Parallelization opportunities** for independent jobs

**Custom Pipeline Generation:**
- ✅ **Tech stack detection** with 100% confidence scores
- ✅ **Multi-platform templates** (GitHub Actions, GitLab CI, Generic)
- ✅ **Enterprise-grade recommendations** (security, performance, cost)
- ✅ **Realistic time estimates** and resource optimization

## 🛡️ Security Features

- **Static Security Analysis**: Detect hardcoded secrets, SQL injection vulnerabilities
- **Dependency Scanning**: Identify vulnerable packages and outdated dependencies  
- **Best Practices Enforcement**: Ensure secure coding and deployment practices
- **Compliance Support**: Built-in recommendations for SOC 2, GDPR, and other standards

## 📈 Performance Metrics

- **Optimization Scoring**: Quantitative assessment of code and pipeline quality
- **Time Savings Calculations**: Realistic estimates for performance improvements
- **Resource Optimization**: CPU, memory, and cost optimization recommendations
- **Complexity Analysis**: Maintainability and scalability assessments

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/review` | POST | AI-powered code review analysis |
| `/api/pipeline` | POST | Pipeline optimization suggestions |
| `/api/pipeline/generate` | POST | Custom pipeline generation |
| `/api/tests` | POST | Test generation from coverage data |
| `/health` | GET | Service health check |
| `/docs` | GET | Interactive API documentation |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 Roadmap

- [ ] **Database Integration**: Persistent storage for analysis history
- [ ] **Real-time Collaboration**: Multi-user pipeline editing
- [ ] **Advanced Visualizations**: Interactive pipeline dependency graphs
- [ ] **Webhook Integration**: Automated analysis on Git events
- [ ] **Enterprise SSO**: SAML and OAuth integration
- [ ] **Custom AI Models**: Fine-tuned models for specific domains

## 🙏 Acknowledgments

- **OpenAI & Anthropic** for providing powerful AI models
- **FastAPI** for the excellent Python web framework
- **React** for the modern frontend framework
- **The DevOps Community** for inspiration and best practices

---

**Built with ❤️ for the DevOps community**

*Transform your development workflow with AI-powered automation!* 🚀