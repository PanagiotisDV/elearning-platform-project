import React, { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Navbar } from '../components'
import { getCourses } from '../api'
import { FaSearch, FaPlus } from 'react-icons/fa'
import { useAuth } from '../context/AuthContext'
import { Link } from 'react-router-dom'

const InstructorCourses = () => {
  const { user } = useAuth()
  const [filters, setFilters] = useState({
    search: '',
    level: '',
    category: '',
  })

  // Φόρτωση μαθημάτων του instructor
  const { data: courses = [], isLoading, error, refetch } = useQuery({
    queryKey: ['instructorCourses', filters],
    queryFn: () => getCourses({ ...filters, my_courses: true, only_published: false }),
    staleTime: 5 * 60 * 1000,
    enabled: !!user && user.role === 'instructor',
  })

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
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">📚 Τα Μαθήματά Μου</h1>
            <p className="text-gray-600 mt-1">Διαχειρίσου τα μαθήματα που δημιούργησες</p>
          </div>
          <Link to="/instructor/courses/new" className="btn-primary flex items-center gap-2">
            <FaPlus /> Νέο Μάθημα
          </Link>
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
                placeholder="Αναζήτηση στα μαθήματά σου..."
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
                  <div key={course.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow flex flex-col h-full">
                    {/* Header */}
                    <div className="flex justify-between items-start mb-3">
                      <h3 className="text-xl font-semibold text-gray-900 line-clamp-2 flex-1">
                        {course.title}
                      </h3>
                      <span className={`text-xs px-2 py-1 rounded-full whitespace-nowrap ml-2 ${
                        course.is_published ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                      }`}>
                        {course.is_published ? 'Δημοσιευμένο' : 'Draft'}
                      </span>
                    </div>

                    {/* Description */}
                    <p className="text-gray-600 text-sm mb-4 line-clamp-3 flex-1">
                      {course.description || 'No description available'}
                    </p>

                    {/* Actions */}
                    <div className="flex items-center justify-between pt-4 border-t border-gray-100 mt-auto">
                      <div className="flex gap-2">
                        <Link
                          to={`/instructor/courses/${course.id}/edit`}
                          className="btn-secondary text-sm px-3 py-1.5"
                        >
                          Επεξεργασία
                        </Link>
                        <Link
                          to={`/courses/${course.id}`}
                          className="btn-primary text-sm px-3 py-1.5"
                        >
                          Προβολή
                        </Link>
                      </div>
                      <Link
                        to={`/instructor/courses/${course.id}/pending`}
                        className="text-sm text-yellow-600 hover:text-yellow-800"
                      >
                        📨 Αιτήματα
                      </Link>
                    </div>
                  </div>
                ))
              ) : (
                <div className="col-span-full text-center py-20">
                  <div className="text-6xl mb-4">📭</div>
                  <p className="text-gray-600">Δεν έχεις δημιουργήσει ακόμα μαθήματα</p>
                  <Link to="/instructor/courses/new" className="btn-primary mt-4 inline-block">
                    Δημιούργησε το Πρώτο σου Μάθημα
                  </Link>
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

export default InstructorCourses