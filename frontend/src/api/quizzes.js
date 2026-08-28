// frontend/src/api/quizzes.js
/**
 * QUIZZES API
 * Όλες οι συναρτήσεις για τα τεστ
 */

import apiClient from './client'

// 1. Λήψη όλων των quizzes μιας ενότητας
export const getQuizzesByLesson = async (lessonId) => {
  const response = await apiClient.get(`/api/lessons/${lessonId}/quizzes`)
  return response.data
}

// 2. Λήψη ενός quiz με τις ερωτήσεις του
export const getQuiz = async (quizId) => {
  const response = await apiClient.get(`/api/quizzes/${quizId}`)
  return response.data
}

// 3. Υποβολή απαντήσεων σε quiz
export const submitQuiz = async (quizId, answers) => {
  const response = await apiClient.post(`/api/quizzes/${quizId}/submit`, { answers })
  return response.data
}

// 4. Λήψη των προσπαθειών μου σε ένα quiz
export const getMyQuizAttempts = async (quizId) => {
  const response = await apiClient.get(`/api/quizzes/${quizId}/attempts/me`)
  return response.data
}