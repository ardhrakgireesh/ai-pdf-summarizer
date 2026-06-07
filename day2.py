import requests
response = requests.get("https://api.genderize.io/?name=Sachu")
data = response.json()

print("Name:",data["name"])
print("Gender:",data["gender"])
print("Probability",data["probability"])
