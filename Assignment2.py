import sys
import os
import hashlib
import numpy as np
import rsa
import matplotlib.pyplot as plt
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import *

# Initial Key value
Key = "808670FF00FF08812"

"""This function takes a key and a list as inputs and performs a hash function on the 
key and uses the first 6 digits as a one-time-password and appends this value to the list"""
def OTP(key):
    token = str(int(hashlib.sha256((key).encode("utf-8")).hexdigest(),16))[:6]
    Hash = str(int(hashlib.sha256((key).encode("utf-8")).hexdigest(),16))
    return Hash, token

def yeet(value, search_list):
	try:
		list_index = search_list.index(value)
		return list_index
	except ValueError:
		return None

# List to store the full hashes to feed the next OTP
hash_list = [(OTP(Key)[0])]
# Lists to store each token
token_list = [(OTP(Key)[1])]
# List to track the number of collisions over time
count = []
clicks = 0
soon = False

# Calcalulate 1,000,000 token generations
for i in range(1000):
	hash_list.append(OTP(hash_list[i])[0])
	token_list.append(OTP(hash_list[i])[1])
	if i % 1000 == 0:
		count.append(len(np.unique(token_list)))

# Make a window

for i in range(20):
	print(token_list[i])

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('Assignment 2 Server')
window.resize(600, 250)
 
# Give window a text box
textbox = QLineEdit(window)
textbox.move(180, 80)
textbox.resize(240,40)
 
# Create a button in the window
button = QPushButton('Enter Password', window)
button.move(180,20)
 

# Create a label to dsplay results to user
window.labl=QLabel(window)
window.labl.move(180,140)
window.labl.resize(300,60)

# Handle event
@pyqtSlot()
def on_click():
	global clicks
	global soon
	user_input = textbox.text()
	print(user_input)
	if token_list[clicks] == user_input:
		window.labl.setText("Access Granted")
		clicks += 1
		print(clicks)
	elif token_list[clicks] != user_input:
		for i in range(clicks, clicks + 10):
			if token_list[i] == user_input:
				window.labl.setText("Please try again")
				print("before: ")
				print(clicks)
				clicks += 1
				print("after: ")
				print(clicks)
				soon = True
				break
		if soon != True:
			window.labl.setText("Please generate new token")
			index = yeet(user_input, token_list)
			clicks = index
			clicks += 1
			print("yeet: ")
			print(clicks)
				

# Define click behavior
button.clicked.connect(on_click)
 
# Display to user
window.show()
app.exec_()
