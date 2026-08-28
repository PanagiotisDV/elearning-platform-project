import React from 'react'
import { useAuth } from '../context/AuthContext'
import { Link } from 'react-router-dom'
import { Navbar } from '../components'
import { useQuery } from '@tanstack/react-query'
import { getMyEnrollments } from '../api'

const Dashboard = () => {
  const { user } = useAuth()

  // Φόρτωση εγγραφών
  const { data: enrollments = [], isLoading } = useQuery({
    queryKey: ['enrollments'],
    queryFn: getMyEnrollments,
    staleTime: 5 * 60 * 1000,
  })

  // Υπολογισμός στατιστικών
  const totalCourses = enrollments.length
  const completedCourses = enrollments.filter(e => e.status === 'completed').length
  const totalProgress = enrollments.reduce((sum, e) => sum + (e.progress_percentage || 0), 0)
  const averageProgress = totalCourses > 0 ? Math.round(totalProgress / totalCourses) : 0

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Καλώς ήρθες, {user?.first_name || 'User'}! 👋
          </h1>
          <p className="text-gray-600 mt-1">
            {user?.role === 'instructor' 
              ? 'Διαχειρίσου τα μαθήματα και τους μαθητές σου' 
              : 'Συνέχισε το μαθησιακό σου ταξίδι'}
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="card bg-white shadow-md hover:shadow-lg transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500">Εγγεγραμμένα Μαθήματα</p>
                <p className="text-3xl font-bold text-primary-600">
                  {isLoading ? '...' : totalCourses}
                </p>
              </div>
              <div className="text-4xl">📚</div>
            </div>
          </div>
          <div className="card bg-white shadow-md hover:shadow-lg transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500">Μέση Πρόοδος</p>
                <p className="text-3xl font-bold text-green-600">
                  {isLoading ? '...' : `${averageProgress}%`}
                </p>
              </div>
              <div className="text-4xl">📊</div>
            </div>
          </div>
          <div className="card bg-white shadow-md hover:shadow-lg transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500">Ολοκληρωμένα</p>
                <p className="text-3xl font-bold text-yellow-600">
                  {isLoading ? '...' : completedCourses}
                </p>
              </div>
              <div className="text-4xl">🏆</div>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <Link to="/courses" className="card bg-white shadow-md hover:shadow-lg transition-shadow flex items-center gap-4">
            <div className="text-4xl">📖</div>
            <div>
              <h3 className="text-lg font-semibold">Αναζήτηση Μαθημάτων</h3>
              <p className="text-gray-600 text-sm">Ανακάλυψε νέα μαθήματα</p>
            </div>
          </Link>
          <Link to="/courses" className="card bg-white shadow-md hover:shadow-lg transition-shadow flex items-center gap-4">
            <div className="text-4xl">📚</div>
            <div>
              <h3 className="text-lg font-semibold">Τα Μαθήματά Μου</h3>
              <p className="text-gray-600 text-sm">
                {isLoading ? 'Φόρτωση...' : `${totalCourses} εγγεγραμμένα μαθήματα`}
              </p>
            </div>
          </Link>
        </div>

        {/* Coming Soon Message */}
        <div className="card bg-white shadow-md text-center py-12">
          <div className="text-6xl mb-4">🚧</div>
          <h2 className="text-2xl font-bold text-gray-700 mb-2">
            Το Dashboard κατασκευάζεται...
          </h2>
          <p className="text-gray-500">
            Σύντομα θα έχεις πρόσβαση σε περισσότερες λειτουργίες,
            <br />
            όπως αναλυτική πρόοδο και συστάσεις μαθημάτων!
          </p>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
