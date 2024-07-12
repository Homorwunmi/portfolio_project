""" This module sends messages to a Telegram chat using the Telegram Bot API.
"""

import requests
import os
import json
import genai
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()
telegram_token = os.getenv('TELEGRAM_TOKEN')

# Set base URL for the Telegram Bot API
base_url = "https://api.telegram.org/bot"

# Dictionary to store user statistics
user_stats = {}

# Function to send a quiz to a Telegram chat
def send_quiz(quiz, chat_id):
    """ This function is responsible for sending a quiz to Telegram

    Args:
        quiz (_type_): dict
                        The quiz from the genai module
        chat_id (_type_): int
                        The chat ID to send the quiz to
    """
    
    # Extract quiz details
    question = quiz['question']
    options = json.dumps(quiz['options'])
    correct_option_id = quiz['correct_option_id']
    explanation = quiz['explanation']

    # Construct parameters for the quiz
    parameters = {
        "chat_id" : chat_id,
        "question": f"🤔💻 *Brain Teaser:* 🤔💻 \n\n{question}",
        "options": options,
        "correct_option_id": correct_option_id,
        "explanation": explanation,
        "is_anonymous": True,
        "type" : "quiz"
    }

    # URL to send the quiz
    url = f"{base_url}{telegram_token}/sendPoll"

    try:
        # Send the quiz to Telegram
        response = requests.post(url, data=parameters)
        response.raise_for_status()  # Raise an exception for HTTP errors
        print(f"Quiz sent to Telegram chat {chat_id}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending quiz: {e}")
    return None

# Function to send a message to a Telegram chat
def send_message(chat_id, text):
    # URL to send the message
    url = f"{base_url}{telegram_token}/sendMessage"
    params = {'chat_id': chat_id, 'text': text}

    try:
        # Send the message to Telegram
        response = requests.post(url, json=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        print(f"Message sent to Telegram chat {chat_id}")
        return response.json()  # Return the JSON response
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")
    return None

# Function to process incoming commands from Telegram
def process_command(update):
    message = update.get('message')
    if message:
        text = message.get('text')
        chat_id = message['chat']['id']
        user_id = message['from']['id']

        if text == '/start':
            send_message(chat_id, "Hi! I'm a Programming Quiz bot")
        elif text == '/help':
            send_message(chat_id, "Hi! I'm a Programming Quiz bot. \nUse commands: /start, /help, /quiz, /stats to interact with me.")
        elif text == '/quiz':
            quiz = genai.prompt_model()
            send_quiz(quiz, chat_id)
        
            # Update user statistics
            if user_id not in user_stats:
                user_stats[user_id] = {'quizzes_taken': 0, 'correct_answers': 0, 'incorrect_answers': 0}
            user_stats[user_id]['quizzes_taken'] += 1

            # Check if user answered correctly
            for option in update['poll']['options']:
                if option['voter_count'] > 0:
                    user_answer = option['voter_count']
            if quiz['correct_option_id'] == user_answer:
                user_stats[user_id]['correct_answers'] += 1
            else:
                user_stats[user_id]['incorrect_answers'] += 1
        
        elif text == '/stats':
            if user_id in user_stats:
                stats = user_stats[user_id]
                send_message(chat_id, f"You have taken {stats['quizzes_taken']} quizzes.\n"
                                      f"Correct answers: {stats['correct_answers']}\n"
                                      f"Incorrect answers: {stats['incorrect_answers']}")
            else:
                send_message(chat_id, "You haven't taken any quizzes yet.")
        else:
            # Update user statistics
            if user_id not in user_stats:
                user_stats[user_id] = {'quizzes_taken': 0, 'correct_answers': 0, 'incorrect_answers': 0}

            # Send message to Telegram chat
            send_message(chat_id, 'Sorry, I do not understand that command. Please type /help for a list of commands.')

# Function to get updates from Telegram
def get_updates(offset=None):
    # URL to get updates
    url = f"{base_url}{telegram_token}/getUpdates"
    params = {'offset': offset}

    try:
        # Get updates from Telegram
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()  # Return the JSON response
    except requests.exceptions.RequestException as e:
        print(f"Error getting updates: {e}")

# Main function to continuously get updates and process commands
def main():
    offset = None
    while True:
        updates = get_updates(offset)
        for update in updates['result']:
            process_command(update)
            offset = update['update_id'] + 1

# Run the main function if this script is executed
if __name__ == '__main__':
    main()