import React, { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Navbar } from '../components'
import { CourseCard } from '../components'
import { getCourses, getMyEnrollments } from '../api'
import { FaSearch } from 'react-icons/fa'
import { useAuth } from '../context/AuthContext'

const Courses = () => {
  const { isAuthenticated } = useAuth()
  const [filters, setFilters] = useState({
    search: '',
    level: '',
    category: '',
  })

  // Φόρτωση μαθημάτων
  const { data: courses = [], isLoading, error, refetch } = useQuery({
    queryKey: ['courses', filters],
    queryFn: () => getCourses(filters),
    staleTime: 5 * 60 * 1000,
  })

  // Φόρτωση εγγραφών
  const { data: enrollments = [] } = useQuery({
    queryKey: ['enrollments'],
    queryFn: getMyEnrollments,
    enabled: isAuthenticated,
    staleTime: 0,
    refetchOnMount: true,
    refetchOnWindowFocus: true,
  })

  // Δημιουργία sets για εγγραφές
  const enrolledCourseIds = new Set(
    enrollments
      .filter(e => e.status === 'active' || e.status === 'completed')
      .map(e => e.course_id)
  )

  const pendingCourseIds = new Set(
    enrollments
      .filter(e => e.status === 'pending')
      .map(e => e.course_id)
  )

  const handleSearch = (e) => {
    e.preventDefault()
    refetch()
  }

  const handleFilterChange = (e) => {
    const { name, value } = e.target
    setFilters(prev => ({ ...prev, [name]: value }))
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">📚 Όλα τα Μαθήματα</h1>
          <p className="text-gray-600 mt-1">Ανακάλυψε και εγγράψου σε μαθήματα από ειδικούς εκπαιδευτές</p>
        </div>

        {/* Search & Filters */}
        <div className="bg-white rounded-lg shadow-md p-4 mb-8">
          <form onSubmit={handleSearch} className="flex flex-col md:flex-row gap-4">
            <div className="flex-1 relative">
              <FaSearch className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
              <input
                type="text"
                name="search"
                value={filters.search}
                onChange={(e) => setFilters(prev => ({ ...prev, search: e.target.value }))}
                placeholder="Αναζήτηση μαθημάτων..."
                className="input-field pl-10"
              />
            </div>
            <select
              name="level"
              value={filters.level}
              onChange={handleFilterChange}
              className="input-field md:w-48"
            >
              <option value="">Όλα τα Επίπεδα</option>
              <option value="beginner">Αρχάριος</option>
              <option value="intermediate">Μέτριος</option>
              <option value="advanced">Προχωρημένος</option>
            </select>
            <input
              type="text"
              name="category"
              value={filters.category}
              onChange={handleFilterChange}
              placeholder="Κατηγορία..."
              className="input-field md:w-48"
            />
            <button type="submit" className="btn-primary px-6">
              Αναζήτηση
            </button>
          </form>
        </div>

        {/* Loading */}
        {isLoading && (
          <div className="flex justify-center items-center py-20">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
              <p className="mt-4 text-gray-600">Φόρτωση μαθημάτων...</p>
            </div>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="text-center py-20">
            <div className="text-6xl mb-4">😅</div>
            <p className="text-red-600">Αποτυχία φόρτωσης μαθημάτων</p>
            <button onClick={() => refetch()} className="btn-primary mt-4">
              Δοκίμασε Ξανά
            </button>
          </div>
        )}

        {/* Courses Grid */}
        {!isLoading && !error && (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {courses.length > 0 ? (
                courses.map((course) => (
                  <CourseCard 
                    key={course.id} 
                    course={course} 
                    isEnrolled={enrolledCourseIds.has(course.id)}
                    isPending={pendingCourseIds.has(course.id)}
                  />
                ))
              ) : (
                <div className="col-span-full text-center py-20">
                  <div className="text-6xl mb-4">🔍</div>
                  <p className="text-gray-600">Δεν βρέθηκαν μαθήματα</p>
                  <button
                    onClick={() => setFilters({ search: '', level: '', category: '' })}
                    className="btn-secondary mt-4"
                  >
                    Καθαρισμός Φίλτρων
                  </button>
                </div>
              )}
            </div>

            <div className="mt-6 text-sm text-gray-500 text-center">
              Εμφάνιση {courses.length} μαθημάτων
            </div>
          </>
        )}
      </div>
    </div>
  )
}

export default Courses