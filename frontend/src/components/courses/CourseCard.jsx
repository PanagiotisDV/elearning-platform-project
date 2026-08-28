import { Link } from 'react-router-dom'
import { FaUser, FaBook, FaPlus } from 'react-icons/fa'
import { useAuth } from '../../context/AuthContext'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { enrollInCourse } from '../../api'
import toast from 'react-hot-toast'

const CourseCard = ({ course, isEnrolled = false, isPending = false }) => {
  const { isAuthenticated, user } = useAuth()
  const queryClient = useQueryClient()

  const levelColors = {
    beginner: 'bg-green-100 text-green-800',
    intermediate: 'bg-yellow-100 text-yellow-800',
    advanced: 'bg-red-100 text-red-800',
  }

  const enrollMutation = useMutation({
    mutationFn: () => enrollInCourse(course.id),
    onSuccess: () => {
      toast.success('Το αίτημα εγγραφής στάλθηκε! 📨')
      queryClient.invalidateQueries({ queryKey: ['enrollments'] })
      queryClient.invalidateQueries({ queryKey: ['courses'] })
    },
    onError: (error) => {
      const message = error.response?.data?.detail || 'Αποτυχία αιτήματος'
      toast.error(message)
    },
  })

  const handleEnroll = (e) => {
    e.preventDefault()
    if (!isAuthenticated) {
      toast.error('Πρέπει να συνδεθείς πρώτα')
      return
    }
    enrollMutation.mutate()
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow flex flex-col h-full">
      {/* Header */}
      <div className="flex justify-between items-start mb-3">
        <h3 className="text-xl font-semibold text-gray-900 line-clamp-2 flex-1">
          {course.title}
        </h3>
        <span className={`text-xs px-2 py-1 rounded-full whitespace-nowrap ml-2 ${levelColors[course.level] || 'bg-gray-100 text-gray-800'}`}>
          {course.level || 'Beginner'}
        </span>
      </div>

      {/* Description */}
      <p className="text-gray-600 text-sm mb-4 line-clamp-3 flex-1">
        {course.description || 'No description available'}
      </p>

      {/* Instructor & Category */}
      <div className="flex items-center gap-4 text-sm text-gray-500 mb-4">
        <span className="flex items-center gap-1">
          <FaUser className="text-xs" />
          {course.instructor_name || 'Unknown'}
        </span>
        <span className="flex items-center gap-1">
          <FaBook className="text-xs" />
          {course.category || 'General'}
        </span>
      </div>

      {/* ===== ACTIONS ===== */}
      <div className="flex items-center justify-between pt-4 border-t border-gray-100 mt-auto">
        <Link
          to={`/courses/${course.id}`}
          className="btn-primary text-sm px-4 py-1.5"
        >
          Λεπτομέρειες
        </Link>

        {isAuthenticated && user?.role === 'student' ? (
          isEnrolled ? (
            <span className="text-xs text-green-600 bg-green-50 px-3 py-1.5 rounded-lg flex items-center border border-green-200 whitespace-nowrap">
              ✅ Εγγεγραμμένος
            </span>
          ) : isPending ? (
            <span className="text-xs text-yellow-600 bg-yellow-50 px-3 py-1.5 rounded-lg flex items-center border border-yellow-200 whitespace-nowrap">
              ⏳ Αναμονή έγκρισης
            </span>
          ) : (
            <button
              onClick={handleEnroll}
              disabled={enrollMutation.isPending}
              className="btn-secondary text-sm px-4 py-1.5 flex items-center gap-1 disabled:opacity-50 whitespace-nowrap"
            >
              <FaPlus className="text-xs" />
              {enrollMutation.isPending ? '...' : 'Αίτημα Εγγραφής'}
            </button>
          )
        ) : isAuthenticated && user?.role === 'instructor' ? (
          <span className="text-xs text-gray-500 bg-gray-100 px-3 py-1.5 rounded-lg flex items-center whitespace-nowrap">
            👨‍🏫 Instructor
          </span>
        ) : (
          <span className="text-xs text-gray-400 bg-gray-50 px-3 py-1.5 rounded-lg flex items-center whitespace-nowrap">
            🔒 Σύνδεση για εγγραφή
          </span>
        )}
      </div>
    </div>
  )
}

export default CourseCard