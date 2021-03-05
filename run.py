from app import app

def start_ngrok():
    from pyngrok import ngrok

    # url = ngrok.connect(port).public_url
    # print(' * Tunnel URL:', url)

if __name__ == "__main__":
    if app.config['START_NGROK']:
        start_ngrok()
    app.run(debug=True,port=4763)
