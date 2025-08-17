import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import CodeReview from './pages/CodeReview'
import PipelineTuner from './pages/PipelineTuner'
import TestGenie from './pages/TestGenie'

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Navigate to="/code-review" replace />} />
          <Route path="/code-review" element={<CodeReview />} />
          <Route path="/pipeline-tuner" element={<PipelineTuner />} />
          <Route path="/test-genie" element={<TestGenie />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App
