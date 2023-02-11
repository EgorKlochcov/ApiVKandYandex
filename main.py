import requests



class VK:
    url = "https://api.vk.com/method/"

    def __init__(self, token, userid, version="5.131"):
        self.params = {"access_token": token, "v": version}
        self.id = userid

    def filter_data(self, response):
        filter_data = []
        max_size = "s"
        photo_data = response["response"]["items"]
        for s in photo_data:
            d = {}
            for i in s["sizes"]:
                if i["type"] > max_size:
                    max_size = i["type"]
                    s["sizes"] = i

                elif i["type"] == "w":
                    max_size = i["type"]
                    s["sizes"] = i
                    break
                else:
                    continue
            d["name"] = str(s["likes"]["count"]) + "_" + str(s["date"])
            d["url"] = s["sizes"]["url"]
            d["type_size"] = s["sizes"]["type"]
            filter_data.append(d)
            max_size = "s"
        return filter_data

    def get_photo(self):
        photo_url = self.url + "photos.get"
        params = {"owner_id": self.id,
                  "album_id": "profile",
                  "extended": "1", "count": 5, "rev": 1}
        response = requests.get(photo_url, params={**self.params, **params})
        return self.filter_data(response.json())


class YandexDisk:
    url = "https://cloud-api.yandex.net/v1/disk/resources"

    def __init__(self, token):
        self.token = token

    def create_folder(self, name_folder):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }
        params = {"path": "/" + name_folder, "overwrite": "true"}
        response = requests.put(self.url, headers=headers, params=params)
        if response.status_code == 201:
            print(f"Папка '{name_folder}' создана на Яндекc.Диск")

    def upload(self, data_photos, name_folder):
        self.create_folder(name_folder)
        for file in data_photos:
            file_path = f'{name_folder}/{file["name"]}'
            url = self.url + "/upload"
            headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.token}'}
            params = {"path": file_path, "overwrite": "true"}
            href = requests.get(url, headers=headers, params=params).json()['href']
            data = requests.get(file["url"]).content
            response = requests.put(href, data=data)
            if response.status_code == 201:
                print(f"Файл '{file['name']}' загружен")


ya_token =
vk_token =
userid =


def work(yandex_token, vk_token, user_id, name_folder):
    vk = VK(vk_token, user_id)
    photo = vk.get_photo()
    yandex = YandexDisk(yandex_token)
    yandex.upload(photo, name_folder)


work(ya_token, vk_token, userid, "some_folder")