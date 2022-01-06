from meizi.items import PW_Album
import requests

proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}

page_size = 10
current_index = 1

find = PW_Album.select().where(PW_Album.enabled == 1).order_by(PW_Album.id).paginate(int(current_index), int(page_size))
while len(find) > 0:
    index = 0
    while index < len(find):
        album = find[index]
        try:
            #response = requests.head(album.cover_url, proxies=proxies)
            response = requests.head(album.cover_url)
            print(str(album.id) + " - " + album.title + " - " + str(response.status_code))
            if response.status_code == 404:
                query = PW_Album.update({
                    PW_Album.enabled: 0
                }).where(PW_Album.id == album.id)
                result = query.execute()
                print("update: " + str(query) + ", result:" + str(result))
        except ConnectionError:
            print("connect error:skip!")
        except Exception:
            print("123")
        index += 1
    current_index += 1
    find = PW_Album.select().where(PW_Album.enabled == 1).order_by(PW_Album.id).paginate(int(current_index),
                                                                                         int(page_size))
