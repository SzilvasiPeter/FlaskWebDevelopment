#!flask/bin/python3 -B
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
