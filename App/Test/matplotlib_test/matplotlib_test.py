import matplotlib.pyplot as plt

# error while importing
#           ImportError: DLL load failed: %1 is not a valid Win32 application.
#           from PyQt4 import QtCore, QtGui

# Looks like QtCore is a 64bit DLL and I'm running Python 3.4 in 32 bit mode.
