from flask import Flask, render_template, render_template_string

app = Flask(__name__, template_folder='templates')

@app.route("/", methods=["GET"])
def map():
    return render_template("map.html")

@app.route("/btirix/token=<token>/", methods=['POST', 'GET'])
def to_update_db(token):
    print(str(token))
    return render_template_string(
        f"""
            <!DOCTYPE html>
            <html>
                <head></head>
                <body>
                    <h1>{token}</h1>
                </body>
            </html>
        """,
        iframe=to_update_db,
    )

if __name__ == "__main__":
    app.run(debug=True)