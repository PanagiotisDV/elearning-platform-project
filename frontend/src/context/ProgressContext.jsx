import React, { createContext, useContext, useState } from 'react'

const ProgressContext = createContext(null)

export const useProgress = () => {
  const context = useContext(ProgressContext)
  if (!context) {
    throw new Error('useProgress must be used within ProgressProvider')
  }
  return context
}

export const ProgressProvider = ({ children }) => {
  const [progress, setProgress] = useState({})

  const updateProgress = (lessonId, data) => {
    setProgress(prev => ({
      ...prev,
      [lessonId]: { ...prev[lessonId], ...data }
    }))
  }

  const value = {
    progress,
    updateProgress,
  }

  return (
    <ProgressContext.Provider value={value}>
      {children}
    </ProgressContext.Provider>
  )
}