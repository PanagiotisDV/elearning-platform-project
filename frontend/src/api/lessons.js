
/**
* Όλες οι συναρτήσεις για τις ενότητες
 */

import apiClient from './client'

// 1. Λήψη όλων των ενοτήτων ενός μαθήματος
export const getLessonsByCourse = async (courseId) => {
  /**
   * Παίρνει όλες τις ενότητες ενός μαθήματος
  */
  const response = await apiClient.get(`/api/courses/${courseId}/lessons`)
  return response.data
}

// 2. Λήψη μιας ενότητας
export const getLesson = async (lessonId) => {
 
  const response = await apiClient.get(`/api/lessons/${lessonId}`)
  return response.data
}

// 3. Ενημέρωση προόδου σε ενότητα
export const updateProgress = async (lessonId, progressData) => {
  /**
   * Ενημερώνει την πρόοδο του μαθητή σε μια ενότητα
     */
  const response = await apiClient.put(`/api/lessons/${lessonId}/progress`, progressData)
  return response.data
}