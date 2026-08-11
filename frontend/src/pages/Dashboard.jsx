
import React from 'react'
import { useAuth } from '../context/AuthContext'
import { Link } from 'react-router-dom'

const Dashboard = () => {
  const { user, logout } = useAuth()

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navbar */}
      <nav className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <span className="text-2xl font-bold text-primary-600">🎓 E-Learning</span>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-600">
                👋 {user?.full_name || 'User'}
              </span>
              <button
                onClick={logout}
                className="text-sm text-red-600 hover:text-red-800"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Dashboard Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Welcome back, {user?.full_name || 'User'}! 👋
          </h1>
          <p className="text-gray-600 mt-1">
            {user?.role === 'instructor' 
              ? 'Manage your courses and students' 
              : 'Continue your learning journey'}
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="card">
            <div className="text-3xl mb-2">📚</div>
            <h3 className="text-lg font-semibold">My Courses</h3>
            <p className="text-2xl font-bold text-primary-600">0</p>
          </div>
          <div className="card">
            <div className="text-3xl mb-2">📊</div>
            <h3 className="text-lg font-semibold">Progress</h3>
            <p className="text-2xl font-bold text-green-600">0%</p>
          </div>
          <div className="card">
            <div className="text-3xl mb-2">🏆</div>
            <h3 className="text-lg font-semibold">Completed</h3>
            <p className="text-2xl font-bold text-yellow-600">0</p>
          </div>
        </div>

        {/* Coming Soon Message */}
        <div className="card text-center py-12">
          <div className="text-6xl mb-4">🚧</div>
          <h2 className="text-2xl font-bold text-gray-700 mb-2">
            Dashboard Under Construction
          </h2>
          <p className="text-gray-500">
            We're building your personalized learning dashboard.
            <br />
            Check back soon for courses, progress tracking, and more!
          </p>
          <div className="mt-6 flex gap-4 justify-center">
            <Link to="/courses" className="btn-primary">
              Browse Courses
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard