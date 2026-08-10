
// AUTHENTICATION API
// Όλες οι συναρτήσεις για authentication

import apiClient from './client'


export const register = async (userData) => {
 const response = await apiClient.post('/api/auth/register', userData)
  return response.data
}


export const login = async (credentials) => {
 const response = await apiClient.post('/api/auth/login', credentials)
  
  
  if (response.data.access_token) {
    localStorage.setItem('access_token', response.data.access_token)
    localStorage.setItem('refresh_token', response.data.refresh_token)
  }
  
  return response.data
}


export const logout = () => {
 
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
}


export const getCurrentUser = async () => {
 const response = await apiClient.get('/api/auth/me')
  return response.data
}

export const refreshToken = async () => {
  const refreshToken = localStorage.getItem('refresh_token')
  
  if (!refreshToken) {
    throw new Error('No refresh token available')
  }
  
  const response = await apiClient.post('/api/auth/refresh', {
    refresh_token: refreshToken,
  })
    
  if (response.data.access_token) {
    localStorage.setItem('access_token', response.data.access_token)
    localStorage.setItem('refresh_token', response.data.refresh_token)
  }
  
  return response.data
}


export const isAuthenticated = () => {
   return !!localStorage.getItem('access_token')
}