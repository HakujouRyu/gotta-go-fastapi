import { useEffect, useState } from 'react'
import { Link } from 'react-router'
import { Button, Card } from '../components'

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

type Status = 'checking' | 'ok' | 'error'

function Health() {
  const [status, setStatus] = useState<Status>('checking')

  const fetchHealth = () =>
    fetch(`${API_URL}/health`)
      .then((res) => setStatus(res.ok ? 'ok' : 'error'))
      .catch(() => setStatus('error'))

  useEffect(() => {
    fetchHealth()
  }, [])

  const recheck = () => {
    setStatus('checking')
    fetchHealth()
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
      <Card className="max-w-sm w-full text-center space-y-4">
        <h1 className="text-xl font-semibold text-gray-900">Health Check</h1>
        <p className="text-sm text-gray-600">
          Backend:{' '}
          <span
            className={
              status === 'ok'
                ? 'text-green-600'
                : status === 'error'
                  ? 'text-red-600'
                  : 'text-gray-500'
            }
          >
            {status === 'checking' && 'checking…'}
            {status === 'ok' && 'connected'}
            {status === 'error' && 'unreachable — is the backend running?'}
          </span>
        </p>
        <Button onClick={recheck}>Recheck</Button>
        <Link to="/" className="block text-sm text-blue-600 hover:underline">
          ← Back
        </Link>
      </Card>
    </div>
  )
}

export default Health
