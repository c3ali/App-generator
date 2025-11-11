export async function POST(request) {
  const body = await request.json();
  
  // URL du backend Railway (définie dans Vercel)
  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  
  const response = await fetch(`${API_URL}/api/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
  
  return new Response(response.body, {
    status: response.status,
    headers: response.headers
  });
}
