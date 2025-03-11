from app import create_app

if __name__ == '__main__':
    app = create_app()
    # Do not use run() in a production setting. It is not intended to
    # meet security and performance requirements for a production server.
    app.run(host="127.0.0.1", port=5000, debug=True) # debug=app.config['DEBUG']
    