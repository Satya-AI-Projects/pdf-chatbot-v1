from pymongo import MongoClient
from dotenv import load_dotenv
import os
import certifi

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

print("Testing MongoDB connection...")
print(f"URI: {MONGODB_URI}")

try:
    # Try with certifi
    client = MongoClient(
        MONGODB_URI,
        tls=True,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=5000
    )
    client.admin.command('ping')
    print("✅ Connection successful with certifi!")

except Exception as e:
    print(f"❌ Connection with certifi failed: {e}")

    try:
        # Try allowing invalid certificates
        client = MongoClient(
            MONGODB_URI,
            tls=True,
            tlsAllowInvalidCertificates=True,
            serverSelectionTimeoutMS=5000
        )
        client.admin.command('ping')
        print("✅ Connection successful with invalid certificates allowed!")

    except Exception as e2:
        print(f"❌ Connection with invalid certificates failed: {e2}")