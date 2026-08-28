import { FaCheckCircle } from 'react-icons/fa'

const EnrolledBadge = () => {
  return (
    <span className="text-xs text-green-600 bg-green-50 px-3 py-1.5 rounded-lg flex items-center gap-1 border border-green-200 whitespace-nowrap">
      <FaCheckCircle className="text-xs" />
      Εγγεγραμμένος
    </span>
  )
}

export default EnrolledBadge