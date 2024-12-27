import discord
import requests as req
from discord.ext import commands

url = "https://api.tomorrow.io/v4?apikey=8OHC9R2jap91HFQCAS39f670YlbtJi0s"
response = req.get(url)
print(response.text)

headers = {
    "accept": "application/json",
    "Accept-Encoding": "gzip"
}

response = req.post(url, headers=headers)

print(response.text)