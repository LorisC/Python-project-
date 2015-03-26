import os
from threading import Thread

from flask import Flask, redirect, request, url_for, render_template, send_from_directory

import fbapi
import processing

app = Flask(__name__, static_url_path="")
concurrency_factor = 150
client_id = "1422264258073656"
client_secret = "b5727881a490b80253fcecdb1748bd85"
redirect_uri = "https://cst-205.herokuapp.com/results"

# home is the main page, with just the login button
@app.route("/")
def home():
    return render_template("index.html")

# /images is the directory where images are served from
@app.route("/images/<path:path>")
def send_js(path):
    return send_from_directory("tmp", path)


# login is the Facebook login route
@app.route("/login")
def login():
    return redirect(fbapi.get_login_url(client_id, redirect_uri), code=302)


# results renders the result page
@app.route("/results")
def logged_in():
    user_code = request.args.get("code")
    if user_code == "":
        return redirect(url_for("/"))
    response = fbapi.get_facebook_response(client_id, client_secret,
        redirect_uri, user_code)
    users = processing.parse_images(response)
    processing.fetch_images(concurrency_factor, users)
    processing.rank(users)
    return render_template("results.html", users=users)


if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port, debug=True)
