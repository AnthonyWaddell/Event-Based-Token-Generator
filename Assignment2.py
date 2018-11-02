import sys
import os
import hashlib
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import *

# Generate the random number
randnum = os.urandom(128)
hash = str(int(hashlib.sha256(randnum).hexdigest(),16))
code = hash[:6]
 
# Make a window
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('Assignment 2')
window.resize(900, 250)
 
# Give window a text box for push button
textbox_client = QLineEdit(window)
textbox_client.move(180, 80)
textbox_client.resize(240,40)

# Give window a text box for token input
textbox_server = QLineEdit(window)
textbox_server.move(480, 80)
textbox_server.resize(240,40)

 
# Create a button to generate token
create_button = QPushButton('Generate Token', window)
create_button.move(180,20)

# Create a button to input token
input_button = QPushButton('Input Token', window)
input_button.move(480,20)
 
# Handle event to generate token
@pyqtSlot()
def on_click():
    textbox_client.setText(code)

# Create a label to dsplay results to user
window.labl=QLabel(window)
window.labl.move(300,140)
window.labl.setText("Testing") # change this later to reflect
 
# Define token generation button behavior
create_button.clicked.connect(on_click)
 
# Dispaly to user
window.show()
app.exec_()
