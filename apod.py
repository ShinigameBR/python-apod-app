import requests
import json
import os


class Apod():
    def __init__(self):
        self.response = get_response("")

    def get_status(self):
        if self.response is not None:
            return True
        else:
            return False

    def get_image(self):
        if self.response is not None:
            if self.response['hdurl'] is not None:
                file_path = os.path.join('cache/imgs/')
                file_name = self.response['hdurl'].split("/")[-1]
                res = requests.get(self.response['hdurl'])
                if res.status_code:
                    with open(os.path.join(file_path, file_name), "wb") as file:
                        file.write(res.content)
                        file.close()
                return file_path + file_name
            elif self.response['url'] is not None:
                file_path = os.path.join('cache/imgs/')
                file_name = self.response['url'].split("/")[-1]
                res = requests.get(self.response['url'])
                if res.status_code:
                    with open(os.path.join(file_path, file_name), "wb") as file:
                        file.write(res.content)
                        file.close()
                return file_path + file_name
        else:
            return None

    def get_title(self):
        if self.response is not None:
            return self.response['title']
        else:
            return None

    def get_date(self):
        if self.response is not None:
            return self.response['date']
        else:
            return None

    def get_description(self):
        if self.response is not None:
            return self.response['explanation']
        else:
            return None

    def get_search(self, search):
        self.response = get_response("&date="+search)

    def erease_cached_images(self, location):
        for filename in os.listdir(location):
            file_path = os.path.join(location, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
            except Exception as e:
                return 'Failed to delete %s. Reason: %s' % (file_path, e)


def get_response(search):
    api_url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"+search
    try:
        response = requests.get(api_url)
        return json.loads(response.text)
    except:
        return None
