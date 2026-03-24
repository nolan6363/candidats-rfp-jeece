import axios from 'axios'

const api = axios.create({ baseURL: '' })

api.interceptors.request.use(config => {
  const token = localStorage.getItem('admin_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  res => res,
  err => {
    const status = err.response?.status
    if ((status === 401 || status === 422) && localStorage.getItem('admin_token')) {
      localStorage.removeItem('admin_token')
      window.location.reload()
    }
    return Promise.reject(err)
  }
)

export default api
