# Import required modules
import logging
import sys
from PySide import QtCore, QtGui

from GATools.gui.app import app

# Configure Logging
root = logging.getLogger()
root.setLevel(logging.DEBUG)


def main():
    # Exception Handling
    try:
        myApp = QtGui.QApplication(sys.argv)
        gaa   = app()
        gaa.show()
        sys.exit(myApp.exec_())
    except NameError:
        print("Name Error:", sys.exc_info()[1])
    except SystemExit:
        print("Closing Window...")
    except Exception:
        print (sys.exc_info()[1])


if __name__ == '__main__':
    main()
