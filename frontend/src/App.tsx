import { BrowserRouter, Routes, Route } from 'react-router'
import Home from './pages/Home'
import Health from './pages/Health'
import Items from './pages/Items'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/health" element={<Health />} />
        <Route path="/items" element={<Items />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
