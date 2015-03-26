import os
import facebook

from flask import Flask, redirect, request, url_for, render_template, send_from_directory

import processing

app = Flask(__name__, static_url_path="")
client_id = '1422264258073656'
client_secret = 'b5727881a490b80253fcecdb1748bd85'
redirect_uri = 'https://cst-205.herokuapp.com/results'

# home is the main page, with just the login button
@app.route('/')
def home():
    return render_template('index.html')

# /images is the directory where images are served from
@app.route('/images/<path:path>')
def send_js(path):
    return send_from_directory('tmp', path)


# login is the Facebook login route
@app.route('/login')
def login():
    return redirect('https://www.facebook.com/dialog/oauth?client_id=' +
            client_id + '&redirect_uri=' + redirect_uri + '&scope=user_friends',
            code=302)


# results renders the result page
@app.route('/results')
def logged_in():
    user_code = request.args.get('code')
    if user_code == '':
        return redirect(url_for('/'))
    graph = facebook.GraphAPI()
    token_response = graph.get_access_token_from_code(user_code, redirect_uri, client_id, client_secret)
    graph = facebook.GraphAPI(access_token=token_response.itervalues().next(), version='2.2')
    response = graph.get_object(id='me/taggable_friends?fields=name,picture.type(large)')
    users = processing.parse_images(response)
    processing.fetch_images(users)
    processing.rank(users)
    for u in users:
        print u.name, u.score
    return "ok"


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True)
