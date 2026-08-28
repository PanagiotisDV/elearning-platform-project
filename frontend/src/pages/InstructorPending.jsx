
import React from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { getPendingEnrollments, approveEnrollment, rejectEnrollment } from '../api'
import { Navbar } from '../components'
import { FaCheck, FaTimes, FaUser } from 'react-icons/fa'
import toast from 'react-hot-toast'
import { useAuth } from '../context/AuthContext'

const InstructorPending = () => {
  const { courseId } = useParams()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const { user } = useAuth()

  // Φόρτωση pending αιτημάτων
  const { data: pendingEnrollments = [], isLoading, error, refetch } = useQuery({
    queryKey: ['pendingEnrollments', courseId],
    queryFn: () => getPendingEnrollments(courseId),
    enabled: !!courseId,
    staleTime: 0,
  })

  // Mutation για έγκριση
  const approveMutation = useMutation({
    mutationFn: approveEnrollment,
    onSuccess: () => {
      toast.success('Εγγραφή εγκρίθηκε! ✅')
      queryClient.invalidateQueries({ queryKey: ['pendingEnrollments', courseId] })
      queryClient.invalidateQueries({ queryKey: ['enrollments'] })
      refetch()
    },
    onError: (error) => {
      const message = error.response?.data?.detail || 'Αποτυχία έγκρισης'
      toast.error(message)
    },
  })

  // Mutation για απόρριψη
  const rejectMutation = useMutation({
    mutationFn: rejectEnrollment,
    onSuccess: () => {
      toast.success('Εγγραφή απορρίφθηκε ❌')
      queryClient.invalidateQueries({ queryKey: ['pendingEnrollments', courseId] })
      refetch()
    },
    onError: (error) => {
      const message = error.response?.data?.detail || 'Αποτυχία απόρριψης'
      toast.error(message)
    },
  })

  const handleApprove = (enrollmentId) => {
    approveMutation.mutate(enrollmentId)
  }

  const handleReject = (enrollmentId) => {
    if (window.confirm('Είσαι σίγουρος ότι θέλεις να απορρίψεις αυτή την εγγραφή;')) {
      rejectMutation.mutate(enrollmentId)
    }
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="flex justify-center items-center h-96">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Φόρτωση αιτημάτων...</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex items-center gap-4 mb-6">
          <button onClick={() => navigate(-1)} className="text-gray-600 hover:text-gray-900">
            ← Πίσω
          </button>
          <h1 className="text-2xl font-bold text-gray-900">
            📨 Αιτήματα Εγγραφής
          </h1>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-600">
            Αποτυχία φόρτωσης αιτημάτων
          </div>
        )}

        {pendingEnrollments.length === 0 ? (
          <div className="bg-white rounded-lg shadow-md p-12 text-center">
            <div className="text-6xl mb-4">📭</div>
            <p className="text-gray-600">Δεν υπάρχουν εκκρεμή αιτήματα εγγραφής</p>
          </div>
        ) : (
          <div className="space-y-4">
            {pendingEnrollments.map((enrollment) => (
              <div
                key={enrollment.id}
                className="bg-white rounded-lg shadow-md p-6 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4"
              >
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-600">
                    <FaUser />
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">
                      {enrollment.user?.full_name || `User #${enrollment.user_id}`}
                    </p>
                    <p className="text-sm text-gray-500">
                      Αίτημα: {new Date(enrollment.enrolled_at).toLocaleDateString('el-GR')}
                    </p>
                  </div>
                </div>
                <div className="flex gap-2 w-full sm:w-auto">
                  <button
                    onClick={() => handleApprove(enrollment.id)}
                    disabled={approveMutation.isPending}
                    className="btn-primary text-sm px-4 py-2 flex items-center gap-1 disabled:opacity-50"
                  >
                    <FaCheck className="text-xs" />
                    {approveMutation.isPending ? '...' : 'Έγκριση'}
                  </button>
                  <button
                    onClick={() => handleReject(enrollment.id)}
                    disabled={rejectMutation.isPending}
                    className="btn-secondary text-sm px-4 py-2 flex items-center gap-1 disabled:opacity-50"
                  >
                    <FaTimes className="text-xs" />
                    {rejectMutation.isPending ? '...' : 'Απόρριψη'}
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        <div className="mt-6 text-sm text-gray-500 text-center">
          {pendingEnrollments.length} εκκρεμή αιτήματα
        </div>
      </div>
    </div>
  )
}

export default InstructorPending