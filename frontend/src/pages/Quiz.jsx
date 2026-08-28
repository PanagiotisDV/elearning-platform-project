/**
 * QUIZ PAGE
 * Εκτέλεση τεστ
 */

import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery, useMutation } from '@tanstack/react-query'
import { getQuiz, submitQuiz } from '../api'
import { Navbar } from '../components'
import { FaArrowLeft, FaClock, FaCheck, FaTimes, FaAward } from 'react-icons/fa'
import toast from 'react-hot-toast'

const Quiz = () => {
  const { id } = useParams()  // quizId
  const navigate = useNavigate()
  const [answers, setAnswers] = useState({})
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [submitted, setSubmitted] = useState(false)
  const [result, setResult] = useState(null)

  // ===== 1. ΦΟΡΤΩΣΗ QUIZ =====
  const { data: quiz, isLoading, error } = useQuery({
    queryKey: ['quiz', id],
    queryFn: () => getQuiz(id),
    staleTime: 5 * 60 * 1000,
  })

  // ===== 2. MUTATION ΓΙΑ ΥΠΟΒΟΛΗ =====
  const submitMutation = useMutation({
    mutationFn: (answersArray) => submitQuiz(id, answersArray),
    onSuccess: (data) => {
      setResult(data)
      setSubmitted(true)
      toast.success('Quiz submitted! 🎉')
    },
    onError: (error) => {
      const message = error.response?.data?.detail || 'Failed to submit quiz'
      toast.error(message)
    },
  })

  // ===== 3. HANDLE ANSWER CHANGE =====
  const handleAnswerChange = (questionIndex, answer) => {
    setAnswers(prev => ({
      ...prev,
      [questionIndex]: answer
    }))
  }

  // ===== 4. HANDLE SUBMIT =====
  const handleSubmit = () => {
    // Έλεγχος αν απαντήθηκαν όλες οι ερωτήσεις
    const totalQuestions = quiz?.questions?.length || 0
    const answeredCount = Object.keys(answers).length

    if (answeredCount < totalQuestions) {
      toast.error(`Please answer all questions (${answeredCount}/${totalQuestions})`)
      return
    }

    // Δημιουργία πίνακα απαντήσεων στη σωστή σειρά
    const answersArray = Array.from({ length: totalQuestions }, (_, i) => answers[i] || '')
    submitMutation.mutate(answersArray)
  }

  // ===== 5. LOADING =====
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="flex justify-center items-center h-96">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading quiz...</p>
          </div>
        </div>
      </div>
    )
  }

  // ===== 6. ERROR =====
  if (error || !quiz) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="max-w-4xl mx-auto px-4 py-20 text-center">
          <div className="text-6xl mb-4">😅</div>
          <p className="text-red-600 text-xl">Quiz not found</p>
          <button onClick={() => navigate(-1)} className="btn-primary mt-4">
            Go Back
          </button>
        </div>
      </div>
    )
  }

  // ===== 7. ΑΠΟΤΕΛΕΣΜΑΤΑ =====
  if (submitted && result) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="max-w-3xl mx-auto px-4 py-8">
          <div className="bg-white rounded-lg shadow-md p-8 text-center">
            <div className="text-6xl mb-4">
              {result.is_passed ? '🎉' : '😅'}
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              {result.is_passed ? 'Congratulations!' : 'Keep Learning!'}
            </h2>
            <p className="text-gray-600 mb-4">
              You scored {result.percentage}% ({result.score}/{result.max_score})
            </p>
            <div className="w-full bg-gray-200 rounded-full h-4 mb-6 max-w-md mx-auto">
              <div
                className={`h-4 rounded-full transition-all duration-500 ${result.is_passed ? 'bg-green-500' : 'bg-yellow-500'}`}
                style={{ width: `${result.percentage}%` }}
              />
            </div>
            <p className="text-sm text-gray-500 mb-6">
              {result.is_passed ? 'You passed the quiz! 🏆' : 'Try again to improve your score.'}
            </p>
            <div className="flex gap-4 justify-center">
              <button onClick={() => navigate(-1)} className="btn-primary">
                Back to Course
              </button>
              <button
                onClick={() => {
                  setAnswers({})
                  setCurrentQuestion(0)
                  setSubmitted(false)
                  setResult(null)
                }}
                className="btn-secondary"
              >
                Retry Quiz
              </button>
            </div>
          </div>
        </div>
      </div>
    )
  }

  // ===== 8. RENDER QUIZ =====
  const questions = quiz.questions || []
  const totalQuestions = questions.length
  const currentQ = questions[currentQuestion]

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="max-w-3xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex items-center gap-4 mb-6">
          <button
            onClick={() => navigate(-1)}
            className="text-gray-600 hover:text-gray-900"
          >
            <FaArrowLeft className="text-xl" />
          </button>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{quiz.title}</h1>
            <p className="text-sm text-gray-500">{quiz.description}</p>
          </div>
        </div>

        {/* Progress */}
        <div className="bg-white rounded-lg shadow-md p-4 mb-6">
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">
              Question {currentQuestion + 1} of {totalQuestions}
            </span>
            <span className="text-sm text-gray-600 flex items-center gap-1">
              <FaClock /> {quiz.time_limit_minutes || 0} min
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
            <div
              className="bg-primary-600 h-2 rounded-full transition-all"
              style={{ width: `${((currentQuestion + 1) / totalQuestions) * 100}%` }}
            />
          </div>
        </div>

        {/* Question */}
        {currentQ && (
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <div className="mb-4">
              <span className="text-xs font-medium text-gray-400 uppercase">
                Question {currentQuestion + 1}
              </span>
              <p className="text-lg font-medium text-gray-900 mt-1">
                {currentQ.question_text}
              </p>
            </div>

            {/* Options */}
            <div className="space-y-3">
              {currentQ.options?.map((option, index) => (
                <label
                  key={index}
                  className={`flex items-center gap-3 p-3 rounded-lg border cursor-pointer transition-colors ${
                    answers[currentQuestion] === option
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-gray-200 hover:bg-gray-50'
                  }`}
                >
                  <input
                    type="radio"
                    name={`question-${currentQuestion}`}
                    value={option}
                    checked={answers[currentQuestion] === option}
                    onChange={() => handleAnswerChange(currentQuestion, option)}
                    className="w-4 h-4 text-primary-600"
                  />
                  <span className="text-gray-700">{option}</span>
                </label>
              ))}
            </div>
          </div>
        )}

        {/* Navigation */}
        <div className="flex justify-between">
          <button
            onClick={() => setCurrentQuestion(prev => Math.max(0, prev - 1))}
            disabled={currentQuestion === 0}
            className="btn-secondary disabled:opacity-50"
          >
            Previous
          </button>

          {currentQuestion < totalQuestions - 1 ? (
            <button
              onClick={() => setCurrentQuestion(prev => Math.min(totalQuestions - 1, prev + 1))}
              className="btn-primary"
            >
              Next
            </button>
          ) : (
            <button
              onClick={handleSubmit}
              disabled={submitMutation.isPending}
              className="btn-primary flex items-center gap-2 disabled:opacity-50"
            >
              {submitMutation.isPending ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  Submitting...
                </>
              ) : (
                'Submit Quiz'
              )}
            </button>
          )}
        </div>

        {/* Progress Info */}
        <div className="mt-4 text-center text-sm text-gray-500">
          Answered: {Object.keys(answers).length} / {totalQuestions}
        </div>
      </div>
    </div>
  )
}

export default Quiz