import requests

# response = requests.get(
#     'http://127.0.0.1:5000/status'
# )
# print(response)
# print(response.status_code)
# print(response.headers)
# print(response.text)
# print(response.json()['name'])

name = input('Введите имя: ')

while True:
    text = input()
    response = requests.post(
        'http://127.0.0.1:5000/send',
        json={'name': name, 'text': text}
    )
