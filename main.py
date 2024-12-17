import sys
from PyQt5.QtWidgets import QApplication
from view.main_window import BeamformingSimulator

def main():
    app = QApplication(sys.argv)
    window = BeamformingSimulator()
    window.setGeometry(100, 100, 1280, 720)  # Set initial window size
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
