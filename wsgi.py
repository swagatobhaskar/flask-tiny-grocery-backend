from app import create_app

app = create_app()

# run in production mode with: gunicorn -b 0.0.0.0:5000 wsgi:app  (or any other port)
# app.run() is intended for the development server, not for production use.
# When you use app.run(), Flask starts the built-in development server,
# which is not compatible with Gunicorn since it's already designed to be a WSGI server.

