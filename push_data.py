from pymongo import MongoClient
uri = "mongodb+srv://tsxmiky24_db_user:admin123@cluster0.5gyi7pp.mongodb.net/?appName=Cluster0"
client = MongoClient(uri)
try:
    client.admin.command("ping")
    print("Connected successfully")
    client.close()

except Exception as e:
    raise Exception(
        "The following error occurred: ", e)