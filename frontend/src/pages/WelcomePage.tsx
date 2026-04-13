import { useNavigate } from 'react-router-dom'
import { removeToken } from '../utils/auth'

function WelcomePage() {
  const navigate = useNavigate()

  const handleLogout = () => {
    removeToken()
    navigate('/login')
  }

  return (
    <div className="welcome-container">
      <button className="logout-btn" onClick={handleLogout}>
        Cerrar sesión
      </button>
      <h1>Bienvenido</h1>
    </div>
  )
}

export default WelcomePage
