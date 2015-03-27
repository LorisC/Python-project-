import facepy
from urlparse import parse_qs

# get_login_url returns the Facebook URL the user should be redirected to to
# obtain a Facebook Graph token
def get_login_url(client_id, redirect_uri):
    return "https://www.facebook.com/dialog/oauth?client_id=" + client_id + \
            "&redirect_uri=" + redirect_uri + "&scope=user_friends"

# get_facebook_response does the Facebook Graph request to Facebook
def get_facebook_response(client_id, client_secret, redirect_uri, user_code):
    graph = facepy.GraphAPI()
    response = graph.get(path="oauth/access_token", client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, code=user_code)
    data = parse_qs(response)
    graph = facepy.GraphAPI(data['access_token'][0])
    return graph.get(path="me/taggable_friends?fields=name,picture.type(large)")

