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
    
#This function finds the index of a user inputted token value
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
server_clicks = 0
client_clicks = 0
duplicate = 0
soon = False

# Calcalulate 1,000,000 token generations
for i in range(1000):
	hash_list.append(OTP(hash_list[i])[0])
	token_list.append(OTP(hash_list[i])[1])
	if i % 10 == 0:
		count.append(len(token_list) - len(np.unique(token_list)))

# Determine count of consecutive tokens
for i in range(1, len(token_list)):
	if token_list[i-1] == token_list[i]:
		duplicate += 1
print("Duplicate consecutive tokens: ", end = "")
print(duplicate)

# Make a server window
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('Assignment 2 Server')
window.resize(700, 250)

# Create a client window
client = QWidget()
client.setWindowTitle('Assignment 2 Client')
client.resize(700, 250)

# Give the client window a textbox
client_textbox = QLineEdit(client)
client_textbox.move(180, 80)
client_textbox.resize(240,40)
 
# Give the server window a text box
textbox = QLineEdit(window)
textbox.move(180, 80)
textbox.resize(240,40)
 
 # Create a button in the client window
client_button = QPushButton('Generate Token', client)
client_button.move(180,20)

# Create a button in the server window
server_button = QPushButton('Enter Password', window)
server_button.move(180,20)

# Create a label to display results to user
window.labl=QLabel(window)
window.labl.move(180,140)
window.labl.resize(400,60)

# Handle client event
@pyqtSlot()
def on_client_click():
	global client_clicks
	client_textbox.setText(token_list[client_clicks])
	client_clicks += 1

# Define click behavior
client_button.clicked.connect(on_client_click)

# Handle server event
@pyqtSlot()
def on_server_click():
	global server_clicks
	global client_clicks
	global soon
	# Get user inputted  toke
	user_input = textbox.text()
	if user_input == None:
		print(server_clicks)
		user_input = ""
	# Is this the correct token
	if token_list[server_clicks] == user_input:
		window.labl.setText("Access Granted")
		server_clicks += 1
	# Is it an incorect token?
	elif token_list[server_clicks] != user_input:
		# Is at least gonna be correct soon?
		for i in range(server_clicks, server_clicks + 10):
			if token_list[i] == user_input:
				window.labl.setText("Please try again")
				server_clicks += 1
				soon = True
				break
		# Or do we need to synchronize with the client?
		if soon != True:
			window.labl.setText("Please generate new token")
			index = yeet(user_input, token_list)
			server_clicks = index
			server_clicks += 1
			client_clicks = index
			client_clicks += 1

# Plot the number of collisions
plt.plot(count)
plt.ylabel("Number of Collisions")
plt.xlabel(" Iterations in 10,000's")
plt.title("Collisions Properties Evolutions as the number of OTP's Increase")
plt.savefig("Graph", dpi = 400)

# Define click behavior
server_button.clicked.connect(on_server_click)
 
# Display to user
window.show()
client.show()
app.exec_()