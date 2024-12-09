from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QWidget

class SavedUnit(QFrame):
    def __init__(self, parent=None, unit_data=None, on_delete=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #1F2937;
                border-radius: 4px;
                padding: 4px;
                margin: 2px;
            }
        """)
        
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(4, 4, 4, 4)
        
        left_container = QWidget()
        left_layout = QHBoxLayout(left_container)
        left_layout.setSpacing(4)
        left_layout.setContentsMargins(4, 0, 4, 0)
        
        name_label = QLabel(f"Unit {unit_data['id']}")
        name_label.setStyleSheet("""
            font-weight: bold;
            color: white;
            font-size: 8pt;
            padding: 2px;
        """)
        left_layout.addWidget(name_label)
        
        delete_btn = QPushButton("Delete")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #DC2626;
                color: white;
                font-size: 8pt;
                padding: 2px 4px;
                min-width: 40px;
                max-width: 40px;
                height: 16px;
            }
            QPushButton:hover {
                background-color: #B91C1C;
            }
        """)
        delete_btn.clicked.connect(lambda: on_delete(unit_data['id']))
        left_layout.addWidget(delete_btn)
        
        main_layout.addWidget(left_container)
        
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setStyleSheet("""
            QFrame {
                background-color: #374151;
                width: 6px;
            }
        """)
        main_layout.addWidget(separator)
        
        right_container = QWidget()
        right_layout = QHBoxLayout(right_container)
        right_layout.setContentsMargins(4, 0, 4, 0)
        main_layout.addWidget(right_container)
        
        main_layout.setStretchFactor(left_container, 0)
        main_layout.setStretchFactor(right_container, 1)