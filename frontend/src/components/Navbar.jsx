import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const Navbar = () => {
  const { isAuthenticated, logout } = useAuth()

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="text-2xl font-bold text-primary-600">
            🎓 E-Learning
          </Link>

          <div className="flex items-center gap-4">
            <Link to="/courses" className="text-sm text-gray-600 hover:text-gray-900">
              Courses
            </Link>
            <Link to="/dashboard" className="text-sm text-gray-600 hover:text-gray-900">
              Dashboard
            </Link>

            {isAuthenticated ? (
              <button
                type="button"
                onClick={logout}
                className="text-sm text-red-600 hover:text-red-800"
              >
                Logout
              </button>
            ) : (
              <>
                <Link to="/login" className="btn-primary text-sm">
                  Login
                </Link>
                <Link to="/register" className="btn-secondary text-sm">
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
