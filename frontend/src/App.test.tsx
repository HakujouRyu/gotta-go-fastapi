import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from './App'

describe('App routing', () => {
  beforeEach(() => {
    // App renders its own BrowserRouter, which reads real browser history —
    // reset the URL so each test starts fresh regardless of prior navigation.
    window.history.pushState({}, '', '/')

    vi.stubGlobal(
      'fetch',
      vi.fn((_url: string, init?: RequestInit) => {
        if (init?.method === 'POST') {
          return Promise.resolve({
            ok: true,
            json: () => Promise.resolve({ id: 1, name: 'Bread', description: null }),
          } as unknown as Response)
        }
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve([]),
        } as unknown as Response)
      }),
    )
  })

  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('renders the home page with links to the other pages', () => {
    render(<App />)
    expect(screen.getByRole('heading', { level: 1 })).toBeDefined()
    expect(screen.getByRole('link', { name: 'Health Check' })).toBeDefined()
    expect(screen.getByRole('link', { name: 'Items' })).toBeDefined()
  })

  it('navigates to the health page and shows backend status', async () => {
    const user = userEvent.setup()
    render(<App />)

    await user.click(screen.getByRole('link', { name: 'Health Check' }))

    expect(screen.getByRole('heading', { name: 'Health Check' })).toBeDefined()
    expect(await screen.findByText('connected')).toBeDefined()
  })

  it('navigates to the items page and creates an item via POST', async () => {
    const user = userEvent.setup()
    render(<App />)

    await user.click(screen.getByRole('link', { name: 'Items' }))
    expect(await screen.findByText('No items yet.')).toBeDefined()

    await user.type(screen.getByPlaceholderText('New item name'), 'Bread')
    await user.click(screen.getByRole('button', { name: 'Add' }))

    expect(await screen.findByText('Bread')).toBeDefined()
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining('/items'),
      expect.objectContaining({ method: 'POST' }),
    )
  })
})
