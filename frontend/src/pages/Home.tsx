import { Link } from 'react-router'
import { Card } from '../components'

const linkStyles = 'block rounded px-4 py-2 text-center font-medium bg-blue-600 text-white hover:bg-blue-700'

function Home() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
      <Card className="max-w-sm w-full text-center space-y-4">
        <h1 className="text-xl font-semibold text-gray-900">FastAPI + React Template</h1>
        <div className="space-y-2">
          <Link to="/health" className={linkStyles}>
            Health Check
          </Link>
          <Link to="/items" className={linkStyles}>
            Items
          </Link>
        </div>
      </Card>
    </div>
  )
}

export default Home
