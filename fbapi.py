import facebook

# get_login_url returns the Facebook URL the user should be redirected to to
# obtain a Facebook Graph token
def get_login_url(client_id, redirect_uri):
    return "https://www.facebook.com/dialog/oauth?client_id=" + client_id + \
            "&redirect_uri=" + redirect_uri + "&scope=user_friends"

# get_facebook_response does the Facebook Graph request to Facebook
def get_facebook_response(client_id, client_secret, redirect_uri, user_code):
    graph = facebook.GraphAPI()
    token = graph.get_access_token_from_code(user_code, redirect_uri, client_id,
            client_secret)
    graph = facebook.GraphAPI(access_token=token.itervalues().next(),
        version='2.2')
    return graph.get_object(
            id='me/taggable_friends?fields=name,picture.type(large)')
