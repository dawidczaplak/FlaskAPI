import requests

BASE = "http://127.0.0.1:5000/"

data = [{"likes": 10, "name": "Tim", "views": 11},
        {"likes": 1, "name": "RRR", "views": 331},
        {"likes": 5, "name": "xxx", "views": 123}]

for i in range(len(data)):
    response = requests.put(BASE + "video/" + str(i), data[i])
    print(response.json())

# input()
# response = requests.delete(BASE + "video/")
# print(response)
# input()
# response = requests.get(BASE + "video/2")
# print(response.json())
response = requests.patch(BASE + "video/2", {"views":99, "likes":101})
print(response.json())