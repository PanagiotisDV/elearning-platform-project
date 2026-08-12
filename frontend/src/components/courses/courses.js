/**
 * COURSES API
 * Όλες οι συναρτήσεις για τα μαθήματα
 */

import apiClient from './client'

// 1. Λήψη όλων των μαθημάτων
export const getCourses = async (params = {}) => {
  const response = await apiClient.get('/api/courses/', { params })
  return response.data
}

// 2. Λήψη ενός μαθήματος με βάση το ID 
export const getCourse = async (id) => {
  
  const response = await apiClient.get(`/api/courses/${id}`)
  return response.data
}

// 3. Δημιουργία μαθήματος (μόνο instructor)
export const createCourse = async (courseData) => {
  const response = await apiClient.post('/api/courses/', courseData)
  return response.data
}

// 4. Ενημέρωση μαθήματος (μόνο instructor)
export const updateCourse = async (id, courseData) => {
  const response = await apiClient.put(`/api/courses/${id}`, courseData)
  return response.data
}

// 5. Διαγραφή μαθήματος (μόνο instructor)
export const deleteCourse = async (id) => {
  await apiClient.delete(`/api/courses/${id}`)
}