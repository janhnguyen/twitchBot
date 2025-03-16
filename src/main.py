import re
from time import sleep
import cv2
import pyautogui
import numpy as np
from pytesseract import pytesseract
import atexit

def goodbye_message():
    for name, msgs in messages.items() :

        for msg in msgs:
            words = msg.split()

            # Iterate through each word in the message
            for word in words:
                word = word.lower()

                # Update the word count in the dictionary
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1

    sorted_word_count = sorted(word_count.items(), key=lambda item: item[1], reverse=True)

    print("-----------------------------------------------------------------------------------")
    print("Word frequencies in decreasing order:")
    for word, count in sorted_word_count:
        print(f"{word}: {count}")

allowedChars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789:?!" '
messages = {}
word_count = {}
counter = 1

# Register the function to run when the script exits
atexit.register(goodbye_message)

while True :

    try :

        image = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
        image = image[365:1575, 2375:2880]

        text = pytesseract.image_to_string(image)
        text = text.replace('\n', ' ')
        text = ''.join([char for char in text if char in allowedChars]) #filter chars

        # Use regex to split the text while keeping the username in the output
        matches = re.findall(r'(\S+:\s)', text)  # Find all usernames

        # Splitting the text using regex that ensures we split *before* each username
        split_text = re.split(r'(\S+:\s)', text)

        # Reconstruct the messages while preserving structure
        output = []
        for i in range(1, len(split_text), 2):  # Iterate over usernames and messages
            username = split_text[i].strip()
            message = split_text[i + 1].strip()
            try :
                if message not in messages[username]:  # Check for duplicates
                    messages[username].append(message)
            except :
                messages[username] = [message]

        sleep(5)
        print(f'{counter} Updating...')
        counter += 1

    except KeyboardInterrupt :
        print('Stopping script...')
        break