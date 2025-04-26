from app import app

# Handler para Vercel serverless function
def handler(request, **kwargs):
    return app(request.environ, request.start_response)

# Para desarrollo local
if __name__ == '__main__':
    app.run() 