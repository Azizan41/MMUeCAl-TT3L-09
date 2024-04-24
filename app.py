from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/home", methods=["POST","GET"])
def main():
    if request.method == "POST":
        ID = request.form.get('ID')
        print(ID)
    return render_template()

if __name__ == '__main__':
    app.run(debug=True)