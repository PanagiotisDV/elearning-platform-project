
/**
 * ENROLLMENTS API
 * Όλες οι συναρτήσεις για εγγραφές σε μαθήματα
 */

import apiClient from './client'

// 1. Εγγραφή σε μάθημα
export const enrollInCourse = async (courseId) => {
   const response = await apiClient.post('/api/enroll', { course_id: courseId })
  return response.data
}

// 2. Λήψη των εγγραφών μου
export const getMyEnrollments = async () => {
  const response = await apiClient.get('/api/enrollments/me')
  return response.data
}

// 3. Διαγραφή εγγραφής (drop course)
export const dropCourse = async (enrollmentId) => {
await apiClient.delete(`/api/enrollments/${enrollmentId}`)
}