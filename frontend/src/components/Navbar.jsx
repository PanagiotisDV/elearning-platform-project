import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { FaGraduationCap } from 'react-icons/fa'

const Navbar = () => {
  const { isAuthenticated, user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2 hover:opacity-80 transition-opacity">
            {isAuthenticated && (
              <FaGraduationCap className="text-3xl text-primary-600" />
            )}
            <span className="text-2xl font-bold text-primary-600">🎓 E-Learning</span>
          </Link>

          {/* Navigation Links */}
          <div className="flex items-center gap-4">
            {/* ===== COURSES (Ορατό σε όλους) ===== */}
            <Link to="/courses" className="text-sm text-gray-600 hover:text-gray-900">
              Courses
            </Link>

            {/* ===== MY COURSES (Μόνο για authenticated) ===== */}
            {isAuthenticated && (
              <Link to="/my-courses" className="text-sm text-gray-600 hover:text-gray-900">
                Τα Μαθήματά Μου
              </Link>
            )}

            {/* ===== DASHBOARD (Μόνο για authenticated) ===== */}
            {isAuthenticated && (
              <Link to="/dashboard" className="text-sm text-gray-600 hover:text-gray-900">
                Dashboard
              </Link>
            )}

            {/* ===== AUTH BUTTONS ===== */}
            {isAuthenticated ? (
              <div className="flex items-center gap-4">
                <span className="text-sm text-gray-600">
                  👋 {user?.first_name || 'User'}
                </span>
                <button
                  onClick={handleLogout}
                  className="text-sm text-red-600 hover:text-red-800"
                >
                  Logout
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-4">
                <Link to="/login" className="btn-primary text-sm">
                  Login
                </Link>
                <Link to="/register" className="btn-secondary text-sm">
                  Register
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar