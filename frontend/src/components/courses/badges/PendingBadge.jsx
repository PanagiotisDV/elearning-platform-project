
import { FaClock } from 'react-icons/fa'

const PendingBadge = () => {
  return (
    <span className="text-xs text-yellow-600 bg-yellow-50 px-3 py-1.5 rounded-lg flex items-center gap-1 border border-yellow-200 whitespace-nowrap">
      <FaClock className="text-xs" />
      Αναμονή έγκρισης
    </span>
  )
}

export default PendingBadge