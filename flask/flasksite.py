from flask import Flask
app = Flask(__name__)

# kalo mau ngerun install Flask dulu terus "python flasksite.py" di terminal

@app.route('/')
def hello_world():
    return 'Hellodsahjkdashdja, World!'



if __name__ == "__main__":
    app.run(debug=True)