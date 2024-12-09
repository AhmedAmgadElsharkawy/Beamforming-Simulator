from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class SavedScenario(QFrame):
    def __init__(self, parent=None, scenario_data=None, on_delete=None, on_visibility_toggle=None, is_visible=False):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #1F2937;
                border-radius: 4px;
                padding: 4px;
                margin: 2px;
            }
        """)
        
        self.visible = is_visible
        self.on_visibility_toggle = on_visibility_toggle
        self.scenario_data = scenario_data
        
        # Main layout
        layout = QHBoxLayout(self)
        layout.setSpacing(4)
        layout.setContentsMargins(4, 4, 4, 4)
        
        # Scenario name
        name_label = QLabel(f"Scenario {scenario_data['id']}")
        name_label.setStyleSheet("""
            font-weight: bold;
            color: white;
            font-size: 8pt;
            padding: 2px;
        """)
        layout.addWidget(name_label)
        
        # Visibility toggle button
        self.visibility_btn = QPushButton("👁‍🗨" if self.visible else "🚫")
        self.visibility_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                font-size: 8pt;
                padding: 2px 4px;
                min-width: 20px;
                max-width: 20px;
                height: 16px;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
        """)
        self.visibility_btn.clicked.connect(self.toggle_visibility)  # Corrected method name
        layout.addWidget(self.visibility_btn)
        
        # Delete button
        delete_btn = QPushButton("❌")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #DC2626;
                color: white;
                font-size: 8pt;
                padding: 2px 4px;
                min-width: 20px;
                max-width: 20px;
                height: 16px;
            }
            QPushButton:hover {
                background-color: #B91C1C;
            }
        """)
        delete_btn.clicked.connect(lambda: on_delete(self.scenario_data['id']))
        layout.addWidget(delete_btn)
        
        layout.addStretch()

    def toggle_visibility(self):
        if self.on_visibility_toggle:
            self.on_visibility_toggle(self.scenario_data['id'], not self.visible)