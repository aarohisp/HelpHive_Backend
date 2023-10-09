#The main entry point.


from flask import Flask
from apis.user_resources import set_user_routes

app = Flask(__name__)

# Set up routes for Module 1
set_user_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
