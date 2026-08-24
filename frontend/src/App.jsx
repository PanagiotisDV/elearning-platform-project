import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { Home, Login, Register, Dashboard, Courses, CourseDetails, Quiz  } from './pages'
import { ProtectedRoute } from './components'  
import './App.css'
import { CoursePlayer } from './pages'

function App() {
  return (
    <Router>
      <Toaster position="top-right" />
      <div className="min-h-screen bg-gray-50">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/courses" element={<Courses />} />
          <Route path="/courses/:id" element={<CourseDetails />} />
          
          <Route 
            path="/dashboard" 
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } 
          />

          <Route path="/courses/:id/player" element={<CoursePlayer />} /><Route
            path="/courses/:id/learn"
            element={
              <ProtectedRoute>
              <CoursePlayer />
              </ProtectedRoute>
            }
          />

          <Route  path="/quiz/:id"   element={
            <ProtectedRoute>
            <Quiz />
           </ProtectedRoute>
          }
          />

        </Routes>
      </div>
    </Router>
  )
}

export default App