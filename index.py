from app import app

# Handler para Vercel serverless function
def handler(request, **kwargs):
    return app(request.environ, start_response=request.start_response) 