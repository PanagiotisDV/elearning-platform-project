import apiClient from './client'

// ===== ΜΟΝΟ ΜΙΑ ΦΟΡΑ =====
export const getCourses = async (params = {}) => {
  const response = await apiClient.get('/api/courses/', { params })
  return response.data
}

export const getCourse = async (id) => {
  const response = await apiClient.get(`/api/courses/${id}`)
  return response.data
}

export const createCourse = async (courseData) => {
  const response = await apiClient.post('/api/courses/', courseData)
  return response.data
}

export const updateCourse = async (id, courseData) => {
  const response = await apiClient.put(`/api/courses/${id}`, courseData)
  return response.data
}

export const deleteCourse = async (id) => {
  await apiClient.delete(`/api/courses/${id}`)
}