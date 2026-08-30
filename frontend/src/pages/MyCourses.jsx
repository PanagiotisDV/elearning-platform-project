import React from 'react'
import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { Navbar } from '../components'
import { getMyEnrollments, getCourse } from '../api'
import { useAuth } from '../context/AuthContext'
import { FaBook, FaClock } from 'react-icons/fa'

const MyCourses = () => {
  const { user } = useAuth()

  // Φόρτωση εγγραφών (όλες)
  const { data: enrollments = [], isLoading, error, refetch } = useQuery({
    queryKey: ['myEnrollments'],
    queryFn: getMyEnrollments,
    staleTime: 0,
    refetchOnMount: true,
  })

  // ===== DEBUG LOGS =====
  console.log('🔍 MyCourses - Raw enrollments:', enrollments)

  // Φιλτράρισμα μόνο για ACTIVE και COMPLETED εγγραφές
  const activeEnrollments = enrollments.filter(e => e.status === 'active' || e.status === 'completed')
  console.log('🔍 MyCourses - Active enrollments:', activeEnrollments)

  // Φόρτωση λεπτομερειών για κάθε μάθημα
  const { data: courses = [], isLoading: coursesLoading } = useQuery({
    queryKey: ['myCourses', activeEnrollments.map(e => e.course_id)],
    queryFn: async () => {
      const coursePromises = activeEnrollments.map(e => getCourse(e.course_id))
      return Promise.all(coursePromises)
    },
    enabled: activeEnrollments.length > 0,
    staleTime: 5 * 60 * 1000,
  })

  // Υπολογισμός στατιστικών
  const totalCourses = activeEnrollments.length
  const totalProgress = activeEnrollments.reduce((sum, e) => sum + (e.progress_percentage || 0), 0)
  const averageProgress = totalCourses > 0 ? Math.round(totalProgress / totalCourses) : 0
  const completedCourses = activeEnrollments.filter(e => e.status === 'completed').length

  if (isLoading || coursesLoading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="flex justify-center items-center h-96">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Φόρτωση μαθημάτων...</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
            <FaBook className="text-primary-600" />
            Τα Μαθήματά Μου
          </h1>
          <p className="text-gray-600 mt-1">
            {user?.first_name}, συνέχισε την εκπαιδευτική σου πορεία
          </p>
        </div>

        {/* Statistics */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-md p-6 flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Σύνολο Μαθημάτων</p>
              <p className="text-3xl font-bold text-primary-600">{totalCourses}</p>
            </div>
            <div className="text-4xl">📚</div>
          </div>
          <div className="bg-white rounded-lg shadow-md p-6 flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Μέση Πρόοδος</p>
              <p className="text-3xl font-bold text-green-600">{averageProgress}%</p>
            </div>
            <div className="text-4xl">📊</div>
          </div>
          <div className="bg-white rounded-lg shadow-md p-6 flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Ολοκληρωμένα</p>
              <p className="text-3xl font-bold text-yellow-600">{completedCourses}</p>
            </div>
            <div className="text-4xl">🏆</div>
          </div>
        </div>

        {/* Courses Grid */}
        {activeEnrollments.length === 0 ? (
          <div className="bg-white rounded-lg shadow-md p-12 text-center">
            <div className="text-6xl mb-4">📭</div>
            <h2 className="text-2xl font-semibold text-gray-700 mb-2">Δεν έχεις εγγραφεί σε κανένα μάθημα</h2>
            <p className="text-gray-500 mb-6">Ξεκίνα την εκπαιδευτική σου πορεία ανακαλύπτοντας νέα μαθήματα</p>
            <Link to="/courses" className="btn-primary px-6 py-3">
              Ανακάλυψε Μαθήματα
            </Link>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {courses.map((course, index) => {
                const enrollment = activeEnrollments.find(e => e.course_id === course.id)
                return (
                  <div key={course.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow flex flex-col h-full">
                    {/* Header */}
                    <div className="flex justify-between items-start mb-3">
                      <h3 className="text-xl font-semibold text-gray-900 line-clamp-2 flex-1">
                        {course.title}
                      </h3>
                      <span className="text-xs px-2 py-1 rounded-full whitespace-nowrap ml-2 bg-green-100 text-green-800">
                        {course.level || 'Beginner'}
                      </span>
                    </div>

                    {/* Description */}
                    <p className="text-gray-600 text-sm mb-4 line-clamp-3 flex-1">
                      {course.description || 'No description available'}
                    </p>

                    {/* Progress */}
                    <div className="mb-4">
                      <div className="flex justify-between text-sm text-gray-600 mb-1">
                        <span>Πρόοδος</span>
                        <span>{enrollment?.progress_percentage || 0}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-primary-600 h-2 rounded-full transition-all"
                          style={{ width: `${enrollment?.progress_percentage || 0}%` }}
                        />
                      </div>
                    </div>

                    {/* Actions */}
                    <div className="flex items-center justify-between pt-4 border-t border-gray-100 mt-auto">
                      <Link
                        to={`/courses/${course.id}`}
                        className="btn-primary text-sm px-4 py-1.5"
                      >
                        Συνέχισε
                      </Link>
                      <span className="text-xs text-gray-500 flex items-center gap-1">
                        <FaClock className="text-xs" />
                        {enrollment?.status === 'completed' ? 'Ολοκληρώθηκε' : 'Σε εξέλιξη'}
                      </span>
                    </div>
                  </div>
                )
              })}
            </div>

            <div className="mt-6 text-sm text-gray-500 text-center">
              Εμφάνιση {courses.length} εγγεγραμμένων μαθημάτων
            </div>
          </>
        )}
      </div>
    </div>
  )
}

export default MyCourses