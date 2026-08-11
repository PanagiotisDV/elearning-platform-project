import { Link } from 'react-router-dom'

const Home = () => {
  return (
    <div className="min-h-screen">
      {/* Navbar */}
      <nav className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <span className="text-2xl font-bold text-primary-600">🎓 E-Learning</span>
            </div>
            <div className="flex items-center gap-4">
              <Link to="/login" className="btn-primary text-sm">
                Login
              </Link>
              <Link to="/register" className="btn-secondary text-sm">
                Register
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            Learn Anything,{' '}
            <span className="text-primary-600">Anytime</span>
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto mb-8">
            Discover thousands of courses from expert instructors.
            Start learning today and advance your career.
          </p>
          <div className="flex gap-4 justify-center">
            <Link to="/register" className="btn-primary text-lg px-8 py-3">
              Get Started Free
            </Link>
            <Link to="/login" className="btn-secondary text-lg px-8 py-3">
              Sign In
            </Link>
          </div>

          {/* Features */}
          <div className="grid md:grid-cols-3 gap-8 mt-20">
            <div className="card">
              <div className="text-4xl mb-4">📚</div>
              <h3 className="text-xl font-semibold mb-2">Expert Courses</h3>
              <p className="text-gray-600">Learn from industry experts with real-world experience</p>
            </div>
            <div className="card">
              <div className="text-4xl mb-4">🎯</div>
              <h3 className="text-xl font-semibold mb-2">Track Progress</h3>
              <p className="text-gray-600">Monitor your learning journey and achievements</p>
            </div>
            <div className="card">
              <div className="text-4xl mb-4">🏆</div>
              <h3 className="text-xl font-semibold mb-2">Certificates</h3>
              <p className="text-gray-600">Earn certificates to showcase your skills</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home