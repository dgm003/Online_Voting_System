from flask import Flask, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('buttons.html')

@app.route("/admin")
def admin():
    subprocess.Popen(["python","main.py"])
    return "ADMIN PAGE OPENED BELOW!"

@app.route("/voter")
def voter():
    subprocess.Popen(["python","voter.py"])
    return "VOTER REGISTRATION OPENED BELOW!"

@app.route("/about")
def about():
    return render_template('about.html')



if __name__ == "__main__":
    app.run(debug=True)