import sys
import os
import hashlib
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import *

# Generate the random number
#TODO: Do this three times
randnum = os.urandom(128)
hash = str(int(hashlib.sha256(randnum).hexdigest(),16))
code = hash[:6]
 
# Make a window
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('Assignment 2')
window.resize(600, 150)
 
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
    textbox.setText(code)
 
# Define click behavior
button.clicked.connect(on_click)
 
# Dispaly to user
window.show()
app.exec_()