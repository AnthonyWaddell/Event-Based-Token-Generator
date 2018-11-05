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

# List to store the full hashes to feed the next OTP
hash_list = [(OTP(Key)[0])]
# List to store each token
token_list = [(OTP(Key)[1])]
# List to track the number of collisions over time
count = []
clicks = 0

# Calcalulate 1,000,000 token generations
for i in range(1000000):
	hash_list.append(OTP(hash_list[i])[0])
	token_list.append(OTP(hash_list[i])[1])
	if i % 10000 == 0:
		count.append(len(np.unique(token_list)))

# Make a window
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('Assignment 2 Client')
window.resize(600, 250)
 
# Give window a text box
textbox = QLineEdit(window)
textbox.move(180, 80)
textbox.resize(240,40)
 
# Create a button in the window
button = QPushButton('Generate Token', window)
button.move(180,20)


# Handle event
@pyqtSlot()
def on_click():
	global clicks
	textbox.setText(token_list[clicks])
	clicks += 1

# Define click behavior
button.clicked.connect(on_click)
 
# Dispaly to user
window.show()
app.exec_()
