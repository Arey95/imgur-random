import array
import os
import random
import string
import sys
import http.client
import threading

if len(sys.argv) < 2:
    sys.exit("\033[37mUsage: python " + sys.argv[0] + " (Number of threads)")
threadAmount = int(sys.argv[1])


class MyThread(threading.Thread):
    def __init__(self, thread_id, name, counter):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.counter = counter

    def run(self):
        print("Starting " + self.name)
        scrape_pictures()
        print("Exiting " + self.name)


def scrape_pictures():
    while True:
        amount = int(''.join(random.choice('5' + '6') for _ in range(1)))

        choice = string.digits + string.ascii_lowercase
        picture_url = ""
        name = ""

        if amount == 6:
            n = 3

            picture = str(''.join(random.choice(string.ascii_uppercase + choice) for _ in range(n)))
            picture2 = str(''.join(random.choice(choice) for _ in range(n)))
            name = str(picture) + str(picture2)
            picture_url = name + ".jpg"

        if amount == 5:
            n = 5

            picture = str(''.join(random.choice(string.ascii_uppercase + choice) for _ in range(n)))
            name = str(picture)
            picture_url = name + ".jpg"

        if exists('i.imgur.com', str(picture_url)):
            print(picture_url)

            with open('index.html', 'r+') as fh:
                lines = fh.readlines()
                fh.seek(0)
                lines.insert(6, "<a href=\"https://imgur.com/" + name + "\">\n" +
                             "    <div class=\"image\">\n" +
                             "        <img src = \"" + "http://i.imgur.com/" + picture_url + "\" alt="">\n" +
                             "    </div>\n" +
                             "</a>\n")
                fh.writelines(lines)


def exists(site, path):
    conn = http.client.HTTPConnection(site)
    conn.request('HEAD', path)
    response = conn.getresponse()
    conn.close()
    return response.status == 200


threads = []

tempVar2 = 1
while tempVar2 <= threadAmount:
    threads.append(MyThread(tempVar2, "Thread-" + str(tempVar2), tempVar2))
    tempVar2 += 1

for t in threads:
    t.start()

for t in threads:
    t.join()

print("Exiting Main Thread")
