import { FaLock } from 'react-icons/fa'

const LoginRequiredBadge = () => {
  return (
    <span className="text-xs text-gray-400 bg-gray-50 px-3 py-1.5 rounded-lg flex items-center gap-1 whitespace-nowrap">
      <FaLock className="text-xs" />
      Σύνδεση για εγγραφή
    </span>
  )
}

export default LoginRequiredBadge