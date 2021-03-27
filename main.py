# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import json
import sys
from urllib.parse import urlparse

import requests
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtCore import QObject, Signal, Slot


url = ''


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


def download_douyin_video(link_url):
    # url = 'https://v.douyin.com/edMM3xM/'
    headers = {
        "authority": "v.douyin.com",
        "method": "GET",
        # ":path": "/edMM3xM/"
        "scheme": "https",
        "accept": "text / html, application / xhtml + xml, application / xml;q = 0.9, image / avif, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;v = b3;q = 0.9",
        "accept - encoding": "gzip, deflate, br",
        "accept - language": "en, zh - CN;q = 0.9, zh;q = 0.8, ja;q = 0.7",
        "cache - control": "no - cache",
        "dnt": "1",
        "pragma": "no - cache",
        "sec-ch-ua": "\"Chromium\";v = \"88\", \"Google Chrome\";v = \"88\", \";Not A Brand\";v = \"99\"",
        # sec - ch - ua - mobile: ?0
        # sec - fetch - dest: document
        # sec - fetch - mode: navigate
        # sec - fetch - site: none
        # sec - fetch - user: ?1
        "upgrade - insecure - requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36"
    }
    # 以初始链接进行请求，会进行302跳转
    r = requests.get(link_url, headers=headers)
    # print(r.url)
    # 跳转后url会变，其中包含了后续请求的一个id
    r = requests.get(r.url)
    # print(r.url)
    # 通过解析url，获取id
    parsed_url = urlparse(r.url)
    url_path = parsed_url.path
    end = url_path.rindex('/')
    start = url_path.rindex('/', 0, end - 1)
    id = url_path[start + 1: end]

    request_url = 'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={0}'

    headers = {
        "authority": "www.iesdouyin.com",
        "method": "GET",
        "path": "/web/api/v2/aweme/iteminfo/?item_ids={0}".format(id),
        "scheme": "https",
        "accept": "*/*",
        "cookie": "_ba=BA0.2-20190804-5199e-ju4rlZVUr3DUAKoGuCzg; _ga=GA1.2.2052427955.1564850335;",
        "referer": r.url,
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36",
        "x-request-width": "XMLHttpRequest"
    }
    # 'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=6936055700275694879'
    r = requests.get(request_url.format(id), headers=headers)
    dict = json.loads(r.text)
    download_url = dict['item_list'][0]['video']['play_addr']['url_list'][0]
    download_url_no_wm = str(download_url).replace('playwm', 'play')

    r = requests.get(download_url_no_wm, stream=True)

    file_name = '{0}.mp4'.format(id)
    with open(file_name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)
    print("{0} has been downloaded!".format(file_name))


class Downloader(QWidget):
    def __init__(self):
        super(Downloader, self).__init__()
        self.download_url = ''
        lay = QHBoxLayout()
        lineEdit = QLineEdit()
        lineEdit.setMinimumWidth(300)
        lineEdit.textChanged.connect(self.change_text)
        lineEdit.returnPressed.connect(self.start_download)
        lay.addWidget(lineEdit)
        self.setLayout(lay)
        self.setWindowTitle("Douyin Downloader")

    @Slot(str)
    def change_text(self, str):
        self.download_url = str
        # print(url, len(url))

    def start_download(self):
        if len(self.download_url) > 28:
            print('start to download {0}.'.format(self.download_url))
            download_douyin_video(self.download_url)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # w = QWidget()
    # lay = QHBoxLayout()
    # lineEdit = QLineEdit()
    # lineEdit.setMinimumWidth(300)
    # lineEdit.textChanged.connect(change_text)
    # lineEdit.returnPressed.connect(start_download)
    # lay.addWidget(lineEdit)
    # w.setLayout(lay)
    # w.show()
    w = Downloader()
    w.show()
    sys.exit(app.exec_())
    # url = 'https://v.douyin.com/edMM3xM/'
    # if len(sys.argv) < 2:
    #     download_douyin_video(url)
    # else:
    #     for link_url in sys.argv[1:]:
    #         download_douyin_video(link_url)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
