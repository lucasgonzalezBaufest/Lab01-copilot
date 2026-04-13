import { getToken } from '../utils/auth'

const BASE_URL = 'http://localhost:8000'

export async function apiFetch(path: string, options: RequestInit = {}): Promise<Response> {
  const token = getToken()
  const headers: Record<string, string> = {
    ...(options.headers as Record<string, string>),
  }

  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }

  return fetch(`${BASE_URL}${path}`, { ...options, headers })
}

export async function login(username: string, password: string): Promise<{ access_token: string }> {
  const params = new URLSearchParams()
  params.append('username', username)
  params.append('password', password)

  const response = await fetch(`${BASE_URL}/token`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: params.toString(),
  })

  if (!response.ok) {
    throw new Error('Usuario o password incorrectos')
  }

  return response.json()
}
