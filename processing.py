import requests
import StringIO
import uuid

from PIL import Image

import imaging

# User is an object used to organize all the data for a given Facebook friend
class User:
    # Name of the user on Facebook
    name = ""
    # Whether or not the user has no profile picture
    is_silhouette = True
    # URL where the user's picture can be downloaded
    picture_url = ""
    # Score of the ELA
    score = 0
    # Names of the files where the pictures are saved
    ela_file = ""
    picture_file = ""

    def __init__(self, name, picture_url):
        self.name = name
        self.picture_url = picture_url


# parseImages downloads all the pictures of the friends into a neat array of
# objects
def parse_images(facebook_response):
    users = []
    for u in facebook_response["data"]:
        user = User(u["name"], u["picture"]["data"]["url"])
        users.append(user)
        if u["picture"]["data"]["is_silhouette"]:
            user.is_silhouette = True
            continue
    return users


# fetchImages fetches the profile images and scores them through an ELA
def fetch_images(users):
    for u in users:
        # Download of the picture of the user
        picture_download = requests.get(u.picture_url)
        picture = Image.open(StringIO.StringIO(picture_download.content))
        # ELA
        try:
            u.score, ela = imaging.apply_ela(picture)
        except:
            users.remove(u)
            continue
        # Save all the pictures for later usage
        u.picture_file = uuid.uuid4().hex
        picture.save("tmp/" + u.picture_file + ".jpg")
        u.ela_file = uuid.uuid4().hex
        ela.save("tmp/" + u.ela_file + ".jpg")


# Ranks sorts the users array based on the score of each user
def rank(users):
    users.sort(key=lambda x: x.score, reverse=True)
