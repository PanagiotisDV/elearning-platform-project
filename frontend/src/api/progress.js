/**
 * PROGRESS API
 * Όλες οι συναρτήσεις για την πρόοδο
 */

import apiClient from './client'

// 1. Λήψη προόδου σε μια ενότητα
export const getLessonProgress = async (lessonId) => {
  const response = await apiClient.get(`/api/lessons/${lessonId}/progress`)
  return response.data
}

// 2. Λήψη συνολικής προόδου σε ένα μάθημα
export const getCourseProgress = async (courseId) => {
  const response = await apiClient.get(`/api/courses/${courseId}/progress`)
  return response.data
}

// 3. Ενημέρωση προόδου σε ενότητα
export const updateLessonProgress = async (lessonId, data) => {
  const response = await apiClient.put(`/api/lessons/${lessonId}/progress`, data)
  return response.data
}