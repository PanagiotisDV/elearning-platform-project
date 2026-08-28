/**
 * PROGRESS BAR
 * Εμφανίζει την πρόοδο του μαθητή
 */

import React from 'react'
import { FaCheckCircle, FaCircle } from 'react-icons/fa'

const ProgressBar = ({ percentage, label, completed, total }) => {
  // 1. Χρώμα με βάση το ποσοστό
  const color = percentage >= 100 ? 'bg-green-500' : percentage >= 50 ? 'bg-blue-500' : 'bg-yellow-500'
  const textColor = percentage >= 100 ? 'text-green-600' : percentage >= 50 ? 'text-blue-600' : 'text-yellow-600'

  return (
    <div className="w-full">
      {/* Label και ποσοστό */}
      <div className="flex justify-between items-center mb-1">
        <span className="text-sm font-medium text-gray-700">
          {label || 'Progress'}
        </span>
        <span className={`text-sm font-semibold ${textColor}`}>
          {percentage}%
        </span>
      </div>

      {/* Progress Bar */}
      <div className="w-full bg-gray-200 rounded-full h-2.5 overflow-hidden">
        <div
          className={`h-2.5 rounded-full transition-all duration-500 ${color}`}
          style={{ width: `${Math.min(percentage, 100)}%` }}
        />
      </div>

      {/* Completed / Total */}
      {completed !== undefined && total !== undefined && (
        <div className="mt-1 flex items-center gap-2 text-xs text-gray-500">
          {percentage >= 100 ? (
            <FaCheckCircle className="text-green-500" />
          ) : (
            <FaCircle className="text-gray-300 text-[10px]" />
          )}
          <span>
            {completed} of {total} lessons completed
          </span>
        </div>
      )}
    </div>
  )
}

export default ProgressBar