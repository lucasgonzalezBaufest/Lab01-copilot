import { useState } from 'react'
import './App.css'

function App() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [message, setMessage] = useState<{ text: string; type: 'success' | 'error' } | null>(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setMessage(null)

    try {
      const params = new URLSearchParams()
      params.append('username', username)
      params.append('password', password)

      const response = await fetch('http://localhost:8000/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: params.toString(),
      })

      if (response.ok) {
        setMessage({ text: `¡Bienvenido, ${username}!`, type: 'success' })
      } else {
        setMessage({ text: 'Credenciales incorrectas', type: 'error' })
      }
    } catch {
      setMessage({ text: 'Error al conectar con el servidor', type: 'error' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <h1>Iniciar Sesión</h1>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">Usuario</label>
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              placeholder="Ingrese su usuario"
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Contraseña</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="Ingrese su contraseña"
            />
          </div>
          {message && (
            <div className={`message ${message.type}`}>
              {message.text}
            </div>
          )}
          <button type="submit" disabled={loading}>
            {loading ? 'Cargando...' : 'Ingresar'}
          </button>
        </form>
      </div>
    </div>
  )
}

export default App
