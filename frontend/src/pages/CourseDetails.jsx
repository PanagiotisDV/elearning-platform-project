/**
 * COURSE DETAILS
 * Σελίδα λεπτομερειών ενός μαθήματος
 */

import React from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'


import { useQuery } from '@tanstack/react-query'
import { getCourse } from '../api'
import { Navbar } from '../components'
import { FaUser, FaBook, FaClock, FaArrowLeft } from 'react-icons/fa'

const CourseDetails = () => {
  // 1. Παίρνουμε το ID από το URL
  const { id } = useParams()
  const navigate = useNavigate()

  // 2. Φορτώνουμε το μάθημα
  const { data: course, isLoading, error } = useQuery({
    queryKey: ['course', id],
    queryFn: () => getCourse(id),
    staleTime: 5 * 60 * 1000,
  })

  // 3. Loading state
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="flex justify-center items-center h-96">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading course details...</p>
          </div>
        </div>
      </div>
    )
  }

  // 4. Error state
  if (error || !course) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="max-w-4xl mx-auto px-4 py-20 text-center">
          <div className="text-6xl mb-4">😅</div>
          <p className="text-red-600 text-xl">Course not found</p>
          <button
            onClick={() => navigate('/courses')}
            className="btn-primary mt-4"
          >
            Back to Courses
          </button>
        </div>
      </div>
    )
  }

  // 5. Level badge color
  const levelColors = {
    beginner: 'bg-green-100 text-green-800',
    intermediate: 'bg-yellow-100 text-yellow-800',
    advanced: 'bg-red-100 text-red-800',
  }

  // 6. Render
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Back button */}
        <button
          onClick={() => navigate('/courses')}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-6"
        >
          <FaArrowLeft /> Back to Courses
        </button>

        {/* Course Header */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="flex justify-between items-start">
            <div className="flex-1">
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                {course.title}
              </h1>
              <p className="text-gray-600 mb-4">{course.description}</p>
            </div>
            <span className={`text-sm px-3 py-1 rounded-full ${levelColors[course.level] || 'bg-gray-100'}`}>
              {course.level || 'Beginner'}
            </span>
          </div>

          {/* Course Info */}
          <div className="flex flex-wrap gap-6 text-sm text-gray-600">
            <span className="flex items-center gap-2">
              <FaUser /> {course.instructor_name || 'Unknown Instructor'}
            </span>
            <span className="flex items-center gap-2">
              <FaBook /> {course.category || 'General'}
            </span>
            <span className="flex items-center gap-2">
              <FaClock /> Created: {new Date(course.created_at).toLocaleDateString()}
            </span>
          </div>
        </div>

        {/* Actions */}
        <div className="flex flex-wrap gap-4">
          <Link
            to={`/courses/${course.id}/learn`}
            className="btn-primary px-6 py-2.5"
          >
            Start Learning
          </Link>
          <button className="btn-secondary px-6 py-2.5">
            Enroll Now
          </button>
        </div>

        {/* Coming Soon */}
        <div className="mt-8 bg-yellow-50 border border-yellow-200 rounded-lg p-4 text-yellow-800">
          <p className="text-sm">
            📝 Lessons and quizzes coming soon! Enroll to access all content.
          </p>
        </div>
      </div>
    </div>
  )
}

export default CourseDetails