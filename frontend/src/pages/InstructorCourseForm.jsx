import React, { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import toast from 'react-hot-toast'
import { FaArrowLeft, FaSave, FaPlus } from 'react-icons/fa'
import { Navbar } from '../components'
import { createCourse, getCourse, updateCourse } from '../api'
import { useAuth } from '../context/AuthContext'

const initialForm = {
  title: '',
  description: '',
  level: 'beginner',
  category: '',
  is_published: false,
}

const InstructorCourseForm = () => {
  const { user } = useAuth()
  const { courseId } = useParams()
  const navigate = useNavigate()
  const isEdit = Boolean(courseId)

  const [formData, setFormData] = useState(initialForm)
  const [isLoading, setIsLoading] = useState(false)
  const [isFetching, setIsFetching] = useState(isEdit)

  useEffect(() => {
    if (!user) return

    if (user.role !== 'instructor') {
      toast.error('Μόνο οι instructors μπορούν να διαχειρίζονται μαθήματα.')
      navigate('/dashboard')
      return
    }

    if (!isEdit) return

    const fetchCourse = async () => {
      try {
        setIsFetching(true)
        const course = await getCourse(courseId)
        setFormData({
          title: course.title || '',
          description: course.description || '',
          level: course.level || 'beginner',
          category: course.category || '',
          is_published: Boolean(course.is_published),
        })
      } catch (error) {
        console.error('Failed to load course:', error)
        toast.error('Αποτυχία φόρτωσης μαθήματος.')
        navigate('/instructor/courses')
      } finally {
        setIsFetching(false)
      }
    }

    fetchCourse()
  }, [courseId, isEdit, navigate, user])

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!formData.title.trim()) {
      toast.error('Το πεδίο τίτλος είναι υποχρεωτικό.')
      return
    }

    setIsLoading(true)

    try {
      if (isEdit) {
        await updateCourse(courseId, {
          ...formData,
          title: formData.title.trim(),
          description: formData.description.trim(),
          category: formData.category.trim(),
        })
        toast.success('Το μάθημα ενημερώθηκε επιτυχώς!')
      } else {
        await createCourse({
          ...formData,
          title: formData.title.trim(),
          description: formData.description.trim(),
          category: formData.category.trim(),
        })
        toast.success('Το μάθημα δημιουργήθηκε επιτυχώς!')
      }

      navigate('/instructor/courses')
    } catch (error) {
      const message = error.response?.data?.detail || 'Αποτυχία αποθήκευσης μαθήματος.'
      toast.error(message)
      console.error('Course save error:', error)
    } finally {
      setIsLoading(false)
    }
  }

  if (isFetching) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="max-w-5xl mx-auto px-4 py-20">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Φόρτωση μαθήματος...</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-6">
          <Link to="/instructor/courses" className="inline-flex items-center gap-2 text-primary-600 hover:text-primary-700 font-medium">
            <FaArrowLeft /> Επιστροφή στα μαθήματά μου
          </Link>
        </div>

        <div className="bg-white rounded-xl shadow-md p-6 md:p-8">
          <div className="flex items-center gap-3 mb-6">
            <div className="bg-primary-100 text-primary-700 rounded-full p-3">
              {isEdit ? <FaSave /> : <FaPlus />}
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                {isEdit ? 'Επεξεργασία Μαθήματος' : 'Νέο Μάθημα'}
              </h1>
              <p className="text-gray-600 mt-1">
                {isEdit ? 'Ανανεώστε τα στοιχεία του μαθήματός σας.' : 'Δημιουργήστε ένα καινούργιο μάθημα.'}
              </p>
            </div>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
                Τίτλος μαθήματος
              </label>
              <input
                id="title"
                name="title"
                type="text"
                value={formData.title}
                onChange={handleChange}
                className="input-field"
                placeholder="π.χ. Εισαγωγή στην Python"
                disabled={isLoading}
              />
            </div>

            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
                Περιγραφή
              </label>
              <textarea
                id="description"
                name="description"
                rows="5"
                value={formData.description}
                onChange={handleChange}
                className="input-field resize-none"
                placeholder="Περιγράψτε το μάθημα..."
                disabled={isLoading}
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div>
                <label htmlFor="level" className="block text-sm font-medium text-gray-700 mb-1">
                  Επίπεδο
                </label>
                <select
                  id="level"
                  name="level"
                  value={formData.level}
                  onChange={handleChange}
                  className="input-field"
                  disabled={isLoading}
                >
                  <option value="beginner">Αρχάριος</option>
                  <option value="intermediate">Μεσαίο</option>
                  <option value="advanced">Προχωρημένος</option>
                </select>
              </div>

              <div>
                <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-1">
                  Κατηγορία
                </label>
                <input
                  id="category"
                  name="category"
                  type="text"
                  value={formData.category}
                  onChange={handleChange}
                  className="input-field"
                  placeholder="π.χ. Programming"
                  disabled={isLoading}
                />
              </div>
            </div>

            <div className="flex items-center gap-3 p-4 border border-gray-200 rounded-lg bg-gray-50">
              <input
                id="is_published"
                name="is_published"
                type="checkbox"
                checked={formData.is_published}
                onChange={handleChange}
                className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                disabled={isLoading}
              />
              <label htmlFor="is_published" className="text-sm font-medium text-gray-700">
                Δημοσίευση μαθήματος
              </label>
            </div>

            <div className="flex justify-end gap-3 pt-4 border-t border-gray-200">
              <Link
                to="/instructor/courses"
                className="btn-secondary px-6"
              >
                Ακύρωση
              </Link>
              <button
                type="submit"
                disabled={isLoading}
                className="btn-primary px-6 disabled:opacity-60 disabled:cursor-not-allowed"
              >
                {isLoading ? (isEdit ? 'Ενημέρωση...' : 'Δημιουργία...') : isEdit ? 'Αποθήκευση αλλαγών' : 'Δημιουργία μαθήματος'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

export default InstructorCourseForm
