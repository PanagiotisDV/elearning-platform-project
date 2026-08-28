
/**
 * ENROLLMENTS API
 * Όλες οι συναρτήσεις για εγγραφές σε μαθήματα
 */

import apiClient from './client'

// 1. Εγγραφή σε μάθημα (στέλνει αίτημα)
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

// 4. INSTRUCTOR: Λήψη pending αιτημάτων
export const getPendingEnrollments = async (courseId) => {
  const response = await apiClient.get(`/api/courses/${courseId}/enrollments/pending`)
  return response.data
}

// 5. INSTRUCTOR: Έγκριση εγγραφής
export const approveEnrollment = async (enrollmentId) => {
  const response = await apiClient.put(`/api/enrollments/${enrollmentId}/approve`)
  return response.data
}

// 6. INSTRUCTOR: Απόρριψη εγγραφής
export const rejectEnrollment = async (enrollmentId) => {
  const response = await apiClient.put(`/api/enrollments/${enrollmentId}/reject`)
  return response.data
}