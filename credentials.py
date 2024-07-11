import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

def load_credentials():
    """This function is responsible for extracting user data"""
    
    # Initialize an empty list to store credentials
    credentials = []

    # Iterate over all environment variables
    for key, value in os.environ.items():
        # Check if the environment variable key starts with 'TELEGRAM_CHAT_ID'
        if key.startswith('TELEGRAM_CHAT_ID'):
            user_id = value

            # If the user ID is not empty, add it to the credentials list
            if user_id:
                credentials.append({'chat_id': int(user_id)})
    
    # Print the collected credentials
    print(credentials)

# Call the function to load credentials
load_credentials()