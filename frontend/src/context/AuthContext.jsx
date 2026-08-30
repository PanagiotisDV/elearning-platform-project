/**
 * AUTH CONTEXT
 * Διαχειρίζεται την κατάσταση του χρήστη σε όλη την εφαρμογή
 */

import React, { createContext, useState, useContext, useEffect } from 'react'
import { getCurrentUser, login as apiLogin, register as apiRegister, logout as apiLogout } from '../api/auth'

const AuthContext = createContext(null)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  const checkAuth = async () => {
    setIsLoading(true)
    try {
      const token = localStorage.getItem('access_token')
      if (!token) {
        setUser(null)
        setIsAuthenticated(false)
        setIsLoading(false)
        return
      }
      const userData = await getCurrentUser()
      setUser(userData)
      setIsAuthenticated(true)
    } catch (error) {
      console.error('Auth check failed:', error)
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      setUser(null)
      setIsAuthenticated(false)
    } finally {
      setIsLoading(false)
    }
  }

  const login = async (email, password) => {
    setIsLoading(true)
    try {
       localStorage.removeItem('access_token')
       localStorage.removeItem('refresh_token')
      const data = await apiLogin({ email, password })
      const userData = await getCurrentUser()
      setUser(userData)
      setIsAuthenticated(true)
      return userData
    } catch (error) {
      console.error('Login failed:', error)
      throw error
    } finally {
      setIsLoading(false)
    }
  }

  const register = async (userData) => {
    setIsLoading(true)
    try {
      const data = await apiRegister(userData)
      await login(userData.email, userData.password)
      return data
    } catch (error) {
      console.error('Registration failed:', error)
      throw error
    } finally {
      setIsLoading(false)
    }
  }

  const logout = () => {
    apiLogout()
    setUser(null)
    setIsAuthenticated(false)
  }

  useEffect(() => {
    checkAuth()
  }, [])

  const value = {
    user,
    isLoading,
    isAuthenticated,
    login,
    register,
    logout,
    checkAuth,
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

export default AuthContext