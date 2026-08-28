import { FaPlus } from 'react-icons/fa'

const EnrollButton = ({ onClick, isLoading = false }) => {
  return (
    <button
      onClick={onClick}
      disabled={isLoading}
      className="btn-secondary text-sm px-4 py-1.5 flex items-center gap-1 disabled:opacity-50 whitespace-nowrap"
    >
      <FaPlus className="text-xs" />
      {isLoading ? '...' : 'Αίτημα Εγγραφής'}
    </button>
  )
}

export default EnrollButton