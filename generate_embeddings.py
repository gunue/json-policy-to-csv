from openai import OpenAI
import pymongo
import os
import json
from dotenv import load_dotenv

# Load environment variables (for OpenAI API credentials)
load_dotenv()
openai = OpenAI()
openai.api_key = os.getenv("OPENAI_API_KEY")

# MongoDB configuration
mongo_url = "mongodb://embed:PolicyMaiker19191919@localhost:27017/?authSource=admin"
client = pymongo.MongoClient(mongo_url)
db = client["vector_database"]
collection = db["embeddings_collection"]

# Function to generate embedding for each description
def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    response = openai.embeddings.create(input=text, model=model)
    
    # Check the response structure
    #print("Embedding response structure:", response)
    
    # Access the embedding directly from the structured response
    embedding = response.data[0].embedding
    
    return embedding

# Load and process each policy, embedding its description and storing in MongoDB
with open('security_policies.json', 'r') as f:
    policies = json.load(f)["policies"]
    for policy in policies:
        description = policy['description']
        embedding = get_embedding(description)
        policy["description_embedding"] = embedding  # Add embedding to policy data
        
        # Insert document with embedding and all other fields in MongoDB
        collection.insert_one(policy)
print("Policies with embeddings have been successfully added to MongoDB.")