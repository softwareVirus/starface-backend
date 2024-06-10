from werkzeug.security import generate_password_hash
import requests

BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + f"/search/series/küç")
print(response.json())
"""
# Test etmek istediğiniz film ID'sini belirtin
movie_id = int(input("Give the movie id:"))
response = requests.get(BASE + f"/films/{movie_id}")
print(response.json())


# Test etmek istediğiniz Aktör ID'sini belirtin
actor_actress_id = int(input("Give the Actor/Actress id:"))
response2 = requests.get(BASE + f"/actor/{actor_actress_id}")
print(response2.json())

# Test etmek istediğiniz Dizi ID'sini belirtin
series_id = int(input("Give the Series id:"))
response3 = requests.get(BASE + f"/series/{series_id}")
print(response3.json())

password = "hashed_password_example"
hashed_password = generate_password_hash(password)
# Yeni kullanıcı verileri
new_user_data = {
    "firstname": "John",  # Updated to lowercase
    "lastname": "Doe",    # Updated to lowercase
    "email": "john.doe@example.com",
    "hashed_password": hashed_password,
    "avatar": "avatar_url",
    "gender": "Male",
    "is_verified": True,
    "roles": "USER"  # Enum değerlerinden birini kullanın (ADMIN veya USER)
}

#response = requests.post(BASE + "signup", json=new_user_data)

# Yanıtı yazdır
#print(response.status_code)
#print(response.json())

# Kullanıcı giriş verileri
login_data = {
    "email": "john.doe@example.com",
    "password": "hashed_password_example"
}

response = requests.post(BASE + "login", json=login_data)

# Yanıtı yazdır
print(response.status_code)
try:
    print(response.json())
except requests.exceptions.JSONDecodeError:
    print("Response content is not valid JSON") 
    
"""