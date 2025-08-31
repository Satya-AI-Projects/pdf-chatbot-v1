from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
import config
import certifi
import ssl


class MongoDBManager:
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        self.connected = False
        self.connection_error = None
        self.connect()

    def connect(self):
        """Establish connection to MongoDB with multiple connection options"""
        try:
            if not config.MONGODB_URI:
                self.connection_error = "MongoDB URI not configured"
                return

            print("🔄 Attempting to connect to MongoDB...")

            # Try different connection options
            connection_options = [
                # Option 1: Standard connection with certifi
                {
                    'tls': True,
                    'tlsCAFile': certifi.where(),
                    'serverSelectionTimeoutMS': 10000
                },
                # Option 2: Allow invalid certificates
                {
                    'tls': True,
                    'tlsAllowInvalidCertificates': True,
                    'serverSelectionTimeoutMS': 10000
                },
                # Option 3: No TLS (shouldn't work with Atlas but trying anyway)
                {
                    'serverSelectionTimeoutMS': 10000
                }
            ]

            for i, options in enumerate(connection_options):
                try:
                    print(f"🔄 Trying connection option {i + 1}...")
                    self.client = MongoClient(config.MONGODB_URI, **options)

                    # Test the connection
                    self.client.admin.command('ping')
                    self.db = self.client[config.DATABASE_NAME]
                    self.collection = self.db[config.COLLECTION_NAME]

                    self.connected = True
                    self.connection_error = None
                    print("✅ Successfully connected to MongoDB!")
                    print(f"✅ Database: {config.DATABASE_NAME}")
                    print(f"✅ Collection: {config.COLLECTION_NAME}")
                    return

                except Exception as e:
                    print(f"❌ Connection option {i + 1} failed: {e}")
                    continue

            # If all options failed
            self.connection_error = "All connection attempts failed"
            print("❌ All MongoDB connection attempts failed")

        except Exception as e:
            self.connection_error = f"Connection error: {str(e)}"
            print(f"❌ MongoDB connection failed: {e}")

    def get_connection_status(self):
        """Get connection status and error message"""
        if self.connected:
            return True, "Connected to MongoDB"
        else:
            return False, self.connection_error or "Not connected to MongoDB"

    def clear_all_documents(self):
        """Clear all documents from the collection"""
        if not self.connected:
            return False, "Not connected to MongoDB"

        try:
            result = self.collection.delete_many({})
            return True, f"Cleared {result.deleted_count} documents"
        except Exception as e:
            return False, f"Error clearing documents: {str(e)}"

    def get_document_count(self):
        """Get count of documents in collection"""
        if not self.connected:
            return 0
        try:
            return self.collection.count_documents({})
        except:
            return 0

    def is_connected(self):
        """Check if MongoDB is connected"""
        return self.connected


# Global database instance
db_manager = MongoDBManager()