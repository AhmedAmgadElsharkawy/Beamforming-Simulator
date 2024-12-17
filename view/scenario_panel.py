from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton

class ScenarioPanel(QFrame):
    """Panel for managing and displaying scenarios"""
    
    def __init__(self, scenario_data, on_delete=None, on_visibility_toggle=None, is_visible=False):
        super().__init__()
        self.visible = is_visible
        self.on_visibility_toggle = on_visibility_toggle
        self.scenario_data = scenario_data
        self._init_ui(on_delete)
        self._apply_styles()

    def _init_ui(self, on_delete):
        # Use single layout
        self.setLayout(QHBoxLayout())
        layout = self.layout()
        layout.setSpacing(4)
        layout.setContentsMargins(4, 4, 4, 4)
        
        # Display meaningful scenario name
        name = self.scenario_data.get('name', f'Scenario {self.scenario_data["id"]}')
        name_label = QLabel(name)
        layout.addWidget(name_label)
        
        # Visibility toggle button with proper callback
        self.visibility_btn = QPushButton("👁" if self.visible else "🚫")
        self.visibility_btn.clicked.connect(self._toggle_visibility)
        layout.addWidget(self.visibility_btn)
        
        # Delete button with proper callback
        if on_delete:
            delete_btn = QPushButton("❌")
            delete_btn.clicked.connect(lambda: on_delete(self.scenario_data['id']))
            layout.addWidget(delete_btn)
        
        layout.addStretch()

    def _toggle_visibility(self):
        if self.on_visibility_toggle:
            self.visible = not self.visible
            self.visibility_btn.setText("👁" if self.visible else "🚫")
            self.on_visibility_toggle(self.scenario_data['id'])
            
    def _apply_styles(self):
        self.setStyleSheet("""
            QFrame {
                background-color: #1F2937;
                border-radius: 4px;
                padding: 4px;
                margin: 2px;
            }
            QLabel {
                font-weight: bold;
                color: white;
                font-size: 8pt;
                padding: 2px;
            }
            QPushButton {
                background-color: #2563EB;
                color: white;
                font-size: 8pt;
                padding: 2px 4px;
                min-width: 20px;
                max-width: 20px;
                height: 16px;
            }
            QPushButton[delete=true] {
                background-color: #DC2626;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
            QPushButton[delete=true]:hover {
                background-color: #B91C1C;
            }
        """)
