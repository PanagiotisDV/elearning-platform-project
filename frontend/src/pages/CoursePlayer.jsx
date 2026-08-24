/**
 * COURSE PLAYER
 * Σελίδα παρακολούθησης μαθήματος
 */

import React, { useState, useEffect } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { getCourse, getLessonsByCourse, updateProgress } from '../api'
import { Navbar } from '../components'
import { 
  FaArrowLeft, FaPlay, FaCheck, FaCheckCircle, 
  FaBook, FaVideo, FaFileAlt, FaClock 
} from 'react-icons/fa'
import toast from 'react-hot-toast'

const CoursePlayer = () => {
  const { id } = useParams()  
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const [selectedLessonId, setSelectedLessonId] = useState(null)
  const [progress, setProgress] = useState({})

  // 1. Φόρτωση μαθήματος
  const { data: course, isLoading: courseLoading } = useQuery({
    queryKey: ['course', id],
    queryFn: () => getCourse(id),
    staleTime: 5 * 60 * 1000,
  })

  // 2. Φόρτωση ενοτήτων
  const { data: lessons = [], isLoading: lessonsLoading } = useQuery({
    queryKey: ['lessons', id],
    queryFn: () => getLessonsByCourse(id),
    staleTime: 5 * 60 * 1000,
  })

  // 3. Επιλέγουμε την πρώτη ενότητα αυτόματα
  useEffect(() => {
    if (lessons.length > 0 && !selectedLessonId) {
      setSelectedLessonId(lessons[0].id)
    }
  }, [lessons, selectedLessonId])

  // 4. Βρίσκουμε την τρέχουσα ενότητα
  const currentLesson = lessons.find(l => l.id === selectedLessonId)

  // 5. Mutation για ενημέρωση προόδου
  const progressMutation = useMutation({
    mutationFn: ({ lessonId, data }) => updateProgress(lessonId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['lessons', id] })
      toast.success('Progress updated! 🎉')
    },
  })

  // 6. Handle mark as complete
  const handleMarkComplete = () => {
    if (!currentLesson) return
    progressMutation.mutate({
      lessonId: currentLesson.id,
      data: { is_completed: true, progress_percentage: 100 }
    })
  }

  // 7. Loading
  if (courseLoading || lessonsLoading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="flex justify-center items-center h-96">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading course content...</p>
          </div>
        </div>
      </div>
    )
  }

  // 8. Error
  if (!course) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="max-w-4xl mx-auto px-4 py-20 text-center">
          <div className="text-6xl mb-4">😅</div>
          <p className="text-red-600 text-xl">Course not found</p>
          <button onClick={() => navigate('/courses')} className="btn-primary mt-4">
            Back to Courses
          </button>
        </div>
      </div>
    )
  }

  // 9. Render
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="flex items-center gap-4 mb-6">
          <button
            onClick={() => navigate(`/courses/${id}`)}
            className="text-gray-600 hover:text-gray-900"
          >
            <FaArrowLeft className="text-xl" />
          </button>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{course.title}</h1>
            <p className="text-sm text-gray-500">Course Player</p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Content */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-md p-6">
              {currentLesson ? (
                <>
                  {/* Lesson Header */}
                  <div className="flex justify-between items-start mb-4">
                    <h2 className="text-xl font-semibold text-gray-900">
                      {currentLesson.title}
                    </h2>
                    <span className="text-sm text-gray-500 flex items-center gap-1">
                      <FaClock /> {currentLesson.duration_minutes || 0} min
                    </span>
                  </div>

                  {/* Lesson Content */}
                  <div className="prose max-w-none">
                    {currentLesson.content_type === 'video' ? (
                      <div className="aspect-video bg-gray-900 rounded-lg flex items-center justify-center">
                        <div className="text-center text-white">
                          <FaPlay className="text-6xl mx-auto mb-4 opacity-50" />
                          <p className="text-sm opacity-50">
                            {currentLesson.content_url || 'Video player coming soon'}
                          </p>
                        </div>
                      </div>
                    ) : (
                      <div className="bg-gray-50 rounded-lg p-6">
                        <p className="text-gray-700">
                          {currentLesson.content_text || 'Lesson content coming soon...'}
                        </p>
                      </div>
                    )}
                  </div>

                  {/* Actions */}
                  <div className="flex justify-between items-center mt-6 pt-6 border-t border-gray-100">
                    <div className="flex gap-3">
                      {currentLesson.id > lessons[0]?.id && (
                        <button className="btn-secondary text-sm">
                          Previous
                        </button>
                      )}
                      {currentLesson.id < lessons[lessons.length - 1]?.id && (
                        <button className="btn-secondary text-sm">
                          Next
                        </button>
                      )}
                    </div>
                    <button
                      onClick={handleMarkComplete}
                      disabled={progressMutation.isPending}
                      className="btn-primary text-sm flex items-center gap-2 disabled:opacity-50"
                    >
                      <FaCheck /> Mark as Complete
                    </button>
                  </div>
                </>
              ) : (
                <p className="text-gray-500 text-center py-12">
                  No lessons available for this course yet.
                </p>
              )}
            </div>
          </div>

          {/* Sidebar - Lessons List */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-md p-4">
              <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <FaBook /> Lessons ({lessons.length})
              </h3>
              <div className="space-y-2 max-h-[600px] overflow-y-auto">
                {lessons.map((lesson, index) => (
                  <button
                    key={lesson.id}
                    onClick={() => setSelectedLessonId(lesson.id)}
                    className={`w-full text-left p-3 rounded-lg transition-colors flex items-center gap-3 ${
                      selectedLessonId === lesson.id
                        ? 'bg-primary-50 border-primary-200 border'
                        : 'hover:bg-gray-50'
                    }`}
                  >
                    <span className="text-sm font-medium text-gray-400">
                      {String(index + 1).padStart(2, '0')}
                    </span>
                    <span className={`flex-1 text-sm ${
                      selectedLessonId === lesson.id ? 'text-primary-700 font-medium' : 'text-gray-700'
                    }`}>
                      {lesson.title}
                    </span>
                    {lesson.content_type === 'video' ? (
                      <FaVideo className="text-gray-400 text-xs" />
                    ) : (
                      <FaFileAlt className="text-gray-400 text-xs" />
                    )}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default CoursePlayer