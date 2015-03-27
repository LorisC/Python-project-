import requests
import StringIO
import uuid
from threading import Thread
from Queue import Queue

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
def fetch_images(concurrency_factor, users):
    # Threading for parallel downloads
    q = Queue(concurrency_factor * 2)
    stop = [False]
    for u in range(concurrency_factor):
        t = Thread(target=fetch_images_worker(q, stop))
        t.daemon = True
        t.start()
    for u in users:
        u.picture_file = uuid.uuid4().hex
        q.put((u.picture_url, u.picture_file))
    q.join()
    stop[0] = True

    # Serial processing of the ELA tasks
    for u in users:
        picture = Image.open("tmp/" + u.picture_file + ".jpg")
        # Display optimization
        (w, h) = picture.size
        if h > 220:
            picture = picture.crop((0, (h - 220) / 2, w, (h + 220) / 2))
            picture.save("tmp/" + u.picture_file + ".jpg", "jpeg", quality=99)
        # ELA
        try:
            u.score, ela = imaging.apply_ela(picture)
        except:
            users.remove(u)
            continue
        # Save the pictures for later usage
        u.ela_file = uuid.uuid4().hex
        ela.save("tmp/" + u.ela_file + ".jpg")


def fetch_images_worker(q, stop):
    # stop is an array whose first element is a boolean that indicated whether
    # or not the worker should stop
    def worker():
        while not stop[0]:
            url, id = q.get()
            picture_data = requests.get(url)
            picture = Image.open(StringIO.StringIO(picture_data.content))
            picture.save("tmp/" + id + ".jpg", "jpeg", quality=99)
            q.task_done()
    return worker


# Ranks sorts the users array based on the score of each user
def rank(users):
    users.sort(key=lambda x: x.score, reverse=True)
