from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QSizePolicy
from PyQt5.QtCore import Qt

class ScenarioPanel(QFrame):
    """Panel for managing and displaying scenarios with proper icon alignment"""
    
    def __init__(self, scenario_data, on_delete=None, on_visibility_toggle=None, is_visible=False):
        super().__init__()
        self.visible = is_visible
        self.on_visibility_toggle = on_visibility_toggle
        self.scenario_data = scenario_data
        self._init_ui(on_delete)
        self._apply_styles()

    def _init_ui(self, on_delete):
        # Main horizontal layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 5, 10, 5)
        main_layout.setSpacing(8)
        self.setLayout(main_layout)
        
        # Name label with ellipsis for long text
        name = self.scenario_data.get('name', f'Scenario {self.scenario_data["id"]}')
        name_label = QLabel(name)
        name_label.setWordWrap(False)  # Prevent wrapping
        name_label.setMaximumWidth(150)  # Limit width
        name_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        name_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        # Enable eliding for long text
        name_label.setTextFormat(Qt.PlainText)
        metrics = name_label.fontMetrics()
        elidedText = metrics.elidedText(name, Qt.ElideRight, name_label.maximumWidth())
        name_label.setText(elidedText)
        
        # Add name to layout
        main_layout.addWidget(name_label)
        
        # Add stretch to push buttons to the right
        main_layout.addStretch()
        
        # Container for buttons to keep them together
        button_layout = QHBoxLayout()
        button_layout.setSpacing(4)  # Small gap between buttons
        
        # Visibility toggle button
        self.visibility_btn = QPushButton("👁" if self.visible else "🚫")
        self.visibility_btn.setFixedSize(24, 24)  # Fixed size for consistency
        self.visibility_btn.clicked.connect(self._toggle_visibility)
        button_layout.addWidget(self.visibility_btn)
        
        # Delete button
        if on_delete:
            delete_btn = QPushButton("❌")
            delete_btn.setFixedSize(24, 24)  # Fixed size for consistency
            delete_btn.clicked.connect(lambda: on_delete(self.scenario_data['id']))
            delete_btn.setProperty('delete', True)  # For styling
            button_layout.addWidget(delete_btn)
        
        # Add button layout to main layout
        main_layout.addLayout(button_layout)

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
                font-size: 9pt;
                padding: 2px;
            }
            QPushButton {
                background-color: #2563EB;
                color: white;
                font-size: 10pt;
                border-radius: 4px;
                margin: 0px;
                padding: 0px;
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