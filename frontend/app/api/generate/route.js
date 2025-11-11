export async function POST(request) {
  const body = await request.json()
  
  const response = await fetch('http://backend:8000/api/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  })
  
  return new Response(response.body, {
    status: response.status,
    headers: response.headers
  })
}
