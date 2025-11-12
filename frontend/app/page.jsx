'use client'
import { useState } from 'react'

export default function Home() {
  const [loading, setLoading] = useState(false)
  const [status, setStatus] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      const formData = new FormData(e.target)
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

      console.log('🔍 API_URL utilisée:', API_URL)
      console.log('🔍 NEXT_PUBLIC_API_URL:', process.env.NEXT_PUBLIC_API_URL)

      const response = await fetch(`${API_URL}/api/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: formData.get('name'),
          description: formData.get('description'),
          stack: formData.get('stack')
        })
      })

      if (!response.ok) {
        throw new Error(`Erreur ${response.status}`)
      }

      const project = await response.json()
      setStatus(`✅ Projet créé : ${project.project_id}`)
    } catch (error) {
      setStatus(`❌ Erreur: ${error.message}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{padding: '2rem', maxWidth: '600px', margin: 'auto'}}>
      <h1>🚀 OK Computer Clone</h1>
      
      <form onSubmit={handleSubmit}>
        <input name="name" placeholder="Nom du projet" required style={{width: '100%', padding: '8px', margin: '10px 0'}} />
        
        <textarea name="description" placeholder="Décris ton application..." rows={5} required style={{width: '100%', padding: '8px', margin: '10px 0'}} />
        
        <select name="stack" style={{width: '100%', padding: '8px', margin: '10px 0'}}>
          <option value="react-node-mongodb">React + Node.js + MongoDB</option>
        </select>
        
        <button type="submit" disabled={loading} style={{padding: '10px 20px'}}>
          {loading ? 'Génération...' : 'Générer'}
        </button>
      </form>
      
      {status && <pre>{status}</pre>}
    </div>
  )
}
