import apiClient from './client'

export const getCourses = async (filters = {}) => {
  const response = await apiClient.get('/api/courses/', {
    params: {
      search: filters.search || undefined,
      level: filters.level || undefined,
      category: filters.category || undefined,
    },
  })
  return response.data
}

export const getCourse = async (courseId) => {
  const response = await apiClient.get(`/api/courses/${courseId}`)
  return response.data
}
