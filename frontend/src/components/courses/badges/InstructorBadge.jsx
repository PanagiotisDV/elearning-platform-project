
import { FaChalkboardTeacher } from 'react-icons/fa'

const InstructorBadge = () => {
  return (
    <span className="text-xs text-gray-500 bg-gray-100 px-3 py-1.5 rounded-lg flex items-center gap-1 whitespace-nowrap">
      <FaChalkboardTeacher className="text-xs" />
      Instructor
    </span>
  )
}

export default InstructorBadge