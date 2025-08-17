import { useState, ChangeEvent } from 'react'
import { uploadCoverage } from '../api/client'

const TestGenie = () => {
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
      setError(null)
      setResult(null)
    }
  }

  const handleSubmit = async () => {
    if (!file) {
      setError('Please select a file to upload')
      return
    }

    setLoading(true)
    setError(null)
    
    try {
      const response = await uploadCoverage(file)
      setResult(response.data)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to process file')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page-container">
      <h2>🧪 Test Genie Agent</h2>
      <p>Upload test coverage JSON to generate comprehensive test suites</p>
      
      <div className="upload-section">
        <div className="file-input">
          <input
            type="file"
            onChange={handleFileChange}
            accept=".json"
          />
          {file && <p>Selected: {file.name}</p>}
        </div>
        
        <button 
          onClick={handleSubmit} 
          disabled={!file || loading}
        >
          {loading ? 'Generating Tests...' : 'Generate Tests'}
        </button>
      </div>

      {error && (
        <div className="error">
          Error: {error}
        </div>
      )}

      {result && (
        <div className="result-section">
          <h3>Generated Tests:</h3>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  )
}

export default TestGenie
