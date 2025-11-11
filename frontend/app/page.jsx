'use client'
import { useState } from 'react'

export default function Home() {
  const [loading, setLoading] = useState(false)
  const [status, setStatus] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    
    const formData = new FormData(e.target)
    const response = await fetch('/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: formData.get('name'),
        description: formData.get('description'),
        stack: formData.get('stack')
      })
    })
    
    const project = await response.json()
    setStatus(`✅ Projet créé : ${project.project_id}`)
    setLoading(false)
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
