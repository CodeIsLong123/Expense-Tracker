import requests

if __name__ == "__main__":
    # response = requests.delete("http://127.0.0.1:8000/delete/34")
    response = requests.get("http://127.0.0.1:8000/")
    # response = requests.post("http://127.0.0.1:8000/items", json={"name": "test", "amount": 100, "category": "income","id": 90})
    print(response.json())
    