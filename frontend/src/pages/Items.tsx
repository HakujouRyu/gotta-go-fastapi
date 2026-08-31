import { useEffect, useState } from 'react'
import type { FormEvent } from 'react'
import { Link } from 'react-router'
import { Button, Card, Input } from '../components'

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

interface Item {
  id: number
  name: string
  description: string | null
}

function Items() {
  const [items, setItems] = useState<Item[]>([])
  const [name, setName] = useState('')

  useEffect(() => {
    fetch(`${API_URL}/items`)
      .then((res) => res.json())
      .then(setItems)
      .catch(() => {})
  }, [])

  const addItem = (e: FormEvent) => {
    e.preventDefault()
    if (!name.trim()) return

    fetch(`${API_URL}/items`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name }),
    })
      .then((res) => res.json())
      .then((item: Item) => {
        setItems((prev) => [...prev, item])
        setName('')
      })
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
      <Card className="max-w-sm w-full space-y-4">
        <h1 className="text-xl font-semibold text-gray-900 text-center">Items</h1>

        <form onSubmit={addItem} className="flex gap-2">
          <Input value={name} onChange={(e) => setName(e.target.value)} placeholder="New item name" />
          <Button type="submit">Add</Button>
        </form>

        <ul className="space-y-1 text-sm text-gray-700">
          {items.length === 0 && <li className="text-gray-400">No items yet.</li>}
          {items.map((item) => (
            <li key={item.id} className="border-b border-gray-100 pb-1">
              {item.name}
            </li>
          ))}
        </ul>

        <Link to="/" className="block text-sm text-blue-600 hover:underline text-center">
          ← Back
        </Link>
      </Card>
    </div>
  )
}

export default Items
