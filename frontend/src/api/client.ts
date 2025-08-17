import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  // Don't set Content-Type header for multipart/form-data
  // Let axios set it automatically with the boundary
})

export const uploadCodeDiff = async (file: File) => {
  const formData = new FormData()
  formData.append('file', file)
  return apiClient.post('/review', formData)
}

export const uploadPipeline = async (file: File) => {
  const formData = new FormData()
  formData.append('file', file)
  return apiClient.post('/pipeline', formData)
}

export const uploadCoverage = async (file: File) => {
  const formData = new FormData()
  formData.append('file', file)
  return apiClient.post('/tests', formData)
}

export default apiClient
