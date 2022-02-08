import urllib.request
file = open('images.txt', "r")
lines = file.readlines()
file.close()
nb=0
for line in lines:
    url=line
    nom="image"+str(nb)+".jpg"
    urllib.request.urlretrieve(url, nom)
    nb+=1