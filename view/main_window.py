from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PyQt5.QtWidgets import (
    QVBoxLayout, QGridLayout, QGroupBox, QLabel, 
    QSpinBox, QDoubleSpinBox, QComboBox, QPushButton, QScrollArea
)
from PyQt5.QtWidgets import QInputDialog
import numpy as np
from controller.array_controller import ArrayController
from controller.visualization_controller import VisualizationController
from model.scenario_manager import ScenarioManager
from view.visualization_panel import VisualizationPanel
from view.array_panel import ArrayPanel
from view.scenario_panel import ScenarioPanel

class BeamformingSimulator(QMainWindow):
    """Main application window integrating all components"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("2D Beamforming Simulator")
        
        # Initialize components in correct order
        self.visualization_panel = VisualizationPanel()
        self.visualization_controller = VisualizationController()
        self.visualization_controller.main_window = self
        self.array_controller = ArrayController(self.visualization_controller)
        self.visualization_controller.array_controller = self.array_controller
        self.scenario_manager = ScenarioManager()
        
        # Initialize lists and states
        self.saved_units = []
        self.scenarios = []
        self.active_scenario = None
        self.active_scenario_id = None
        
        # Setup UI and initial state
        self._init_ui()
        self._apply_stylesheet()
        self.update_patterns_with_units([])

    def _init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        
        # Setup visualization panel
        self.visualization_panel = VisualizationPanel()
        layout.addWidget(self.visualization_panel, stretch=2)
        
        # Setup control panel
        self.control_panel = self._create_control_panel()
        layout.addWidget(self.control_panel, stretch=1)

    def _create_control_panel(self):
        control_widget = QWidget()
        control_layout = QVBoxLayout(control_widget)
        
        # Current Unit Controls
        current_unit_group = QGroupBox("Current Unit")
        current_unit_layout = QGridLayout()
        
        # Array Type
        self.array_type = self._create_array_type_selector(current_unit_layout)
        self.array_type.currentTextChanged.connect(self._toggle_curvature)
        
        # Numeric Parameters
        self.elements = self._create_parameter_spinbox("Elements", 1, 100, 16, current_unit_layout, 1)
        self.spacing = self._create_parameter_spinbox("Spacing (λ)", 0.1, 10.0, 0.5, current_unit_layout, 2)
        self.steering = self._create_parameter_spinbox("Steering (°)", -90, 90, 0, current_unit_layout, 3)
        self.curvature = self._create_parameter_spinbox("Curvature", 0.1, 10.0, 1.0, current_unit_layout, 5)
        self.frequency = self._create_parameter_spinbox("Frequency (MHz)", 1, 1000, 100, current_unit_layout, 6)
        self.x_position = self._create_parameter_spinbox("X-Position", -50, 50, 0.0, current_unit_layout, 7)
        self.y_position = self._create_parameter_spinbox("Y-Position", -50, 50, 0.0, current_unit_layout, 8)
        
         # Add custom style for disabled curvature
        self.curvature.setStyleSheet("""
            QDoubleSpinBox:disabled {
                background-color: #2D3748;
                color: #718096;
            }
        """)
    
        # Initialize curvature state
        self.curvature.setEnabled(False)
        
        # Save Unit Button
        self.save_unit_btn = QPushButton("Save Unit")
        self.save_unit_btn.clicked.connect(self._save_current_unit)
        current_unit_layout.addWidget(self.save_unit_btn, 9, 0, 1, 2)
        
        current_unit_group.setLayout(current_unit_layout)
        control_layout.addWidget(current_unit_group)
        
        # Saved Units Section
        saved_units_group = self._create_saved_units_section()
        control_layout.addWidget(saved_units_group)
        
        return control_widget

    def _toggle_curvature(self, array_type):
        self.curvature.setEnabled(array_type == "Curved")
        
    def _toggle_parameters(self, array_type):
        is_curved = array_type == "Curved"
        self.curvature.setEnabled(is_curved)
        self.spacing.setEnabled(not is_curved)
        
        # Add styling for disabled state
        disabled_style = """
            QDoubleSpinBox:disabled {
                background-color: #2D3748;
                color: #718096;
            }
        """
        self.spacing.setStyleSheet(disabled_style)
        self.curvature.setStyleSheet(disabled_style)
        
        # Update plots after parameter changes
        self.update_plots()

    def _create_array_type_selector(self, layout):
        layout.addWidget(QLabel("Array Type:"), 0, 0)
        array_type = QComboBox()
        array_type.addItems(["Linear", "Curved"])
        array_type.currentTextChanged.connect(self._toggle_parameters)
        layout.addWidget(array_type, 0, 1)
        return array_type
    
    def _create_parameter_spinbox(self, label, min_val, max_val, default_val, layout, row):
        layout.addWidget(QLabel(label), row, 0)
        spinbox = QDoubleSpinBox() if isinstance(default_val, float) else QSpinBox()
        spinbox.setRange(min_val, max_val)
        spinbox.setValue(default_val)
        spinbox.valueChanged.connect(self.update_plots)
        layout.addWidget(spinbox, row, 1)
        return spinbox
    
    def _create_saved_units_section(self):
        saved_units_group = QGroupBox("Saved Units")
        saved_units_layout = QHBoxLayout()
        
        # Units Section
        left_layout = self._create_units_section()
        
        # Scenarios Section
        right_layout = self._create_scenarios_section()
        
        saved_units_layout.addLayout(left_layout)
        saved_units_layout.addLayout(right_layout)
        saved_units_group.setLayout(saved_units_layout)
        
        return saved_units_group
    
    def _create_units_section(self):
        layout = QVBoxLayout()
        
        # Scroll Area for Units
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background-color: #1F2937;")
        scroll_content = QWidget()
        self.saved_units_layout = QVBoxLayout(scroll_content)
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        # Add Scenario Button
        self.add_scenario_btn = QPushButton("Add Scenario")
        self.add_scenario_btn.clicked.connect(self._save_scenario)
        self.add_scenario_btn.setEnabled(False)  # Initially disabled
        layout.addWidget(self.add_scenario_btn)
        
        return layout

    def _create_scenarios_section(self):
        layout = QVBoxLayout()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background-color: #1F2937;")
        scroll_content = QWidget()
        self.scenarios_layout = QVBoxLayout(scroll_content)
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        return layout

    def update_plots(self):
        if self.scenario_manager.active_scenario_id is None:
            self.update_patterns_with_units([])

    def update_patterns_with_units(self, units):
        self.visualization_panel.clear_all_plots()
        
        if units:
            params_list = self._prepare_params_list(units)
        else:
            params_dict = self._get_current_params()
            # For current unit, steering is already in degrees, no conversion needed
            params_list = [params_dict]
        
        self._update_all_plots(params_list)
        self.visualization_panel.refresh_all_canvases()
        
    def _save_current_unit(self):
        unit_data = {
            'array_type': self.array_type.currentText().lower(),  
            'elements': self.elements.value(),
            'spacing': self.spacing.value(),
            'steering': self.steering.value(),
            'phase': 0,
            'curvature': self.curvature.value(),
            'frequency': self.frequency.value(),
            'x_position': self.x_position.value(),
            'y_position': self.y_position.value()
        }
        # Remove the id calculation from here and let array_controller handle it
        self.array_controller.create_array(unit_data)
        self.update_saved_units_display()
        
        visible_arrays = [array.to_dict() for array in self.array_controller.arrays
                        if self.array_controller.selected_arrays.get(array.id, True)]
        self.visualization_panel.update_plots(visible_arrays, self.visualization_controller)
        self.visualization_panel.refresh_all_canvases()

    def _save_scenario(self):
        if self.array_controller.arrays:
            # Create a dialog to get scenario name
            name, ok = QInputDialog.getText(self, 'Save Scenario', 'Enter scenario name:')
            
            if ok and name:
                scenario_id = self.scenario_manager.add_scenario(
                    arrays=self.array_controller.arrays,
                    name=name  # Pass the name to add_scenario
                )
                self.array_controller.arrays = []
                self.update_saved_units_display()
                self.update_scenarios_display()
                self.scenario_manager.set_active_scenario(scenario_id)

    def update_saved_units_display(self):
        while self.saved_units_layout.count():
            child = self.saved_units_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        for array in self.array_controller.arrays:
            unit_widget = ArrayPanel(
                array_data=array.to_dict(),
                on_delete=self.array_controller.delete_array,  # Connect delete handler
                on_edit=self.array_controller.update_array,
                on_visibility_change=self.array_controller.toggle_array_visibility
            )
            self.saved_units_layout.addWidget(unit_widget)
        self.add_scenario_btn.setEnabled(len(self.array_controller.arrays) > 0)   
        # Force refresh of the layout
        self.saved_units_layout.update()

    def update_scenarios_display(self):
        while self.scenarios_layout.count():
            child = self.scenarios_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for scenario in self.scenario_manager.scenarios:
            scenario_widget = ScenarioPanel(
                scenario_data=scenario,
                on_delete=self._handle_scenario_delete,  # Add new handler
                on_visibility_toggle=self._handle_scenario_visibility,  # Add new handler
                is_visible=(scenario['id'] == self.scenario_manager.active_scenario_id)
            )
            self.scenarios_layout.addWidget(scenario_widget)

    # Add these new methods to handle the button actions
    def _handle_scenario_delete(self, scenario_id):
        # Delete the scenario
        self.scenario_manager.delete_scenario(scenario_id)
        self.update_scenarios_display()

        # Update plots with current unit parameters
        self.visualization_panel.clear_all_plots()
        params = {
            'elements': self.elements.value(),
            'spacing': self.spacing.value(),
            'steering': self.steering.value(),
            'array_type': self.array_type.currentText().lower(),
            'curvature': self.curvature.value(),
            'frequency': self.frequency.value(),
            'x_position': self.x_position.value(),
            'y_position': self.y_position.value(),
            'phase': 0
        }
        self.visualization_panel.update_plots([params], self.visualization_controller)
        self.visualization_panel.refresh_all_canvases()

    def _handle_scenario_visibility(self, scenario_id):
        scenario = next((s for s in self.scenario_manager.scenarios if s['id'] == scenario_id), None)
        if scenario:
            self.visualization_panel.clear_all_plots()
            visible_arrays = scenario['arrays']
            self.visualization_panel.update_plots(visible_arrays, self.visualization_controller)
            self.visualization_panel.refresh_all_canvases()
        
        self.scenario_manager.set_active_scenario(scenario_id)
        self.update_scenarios_display()

    def _prepare_params_list(self, units):
        return [{
            'elements': unit['elements'],
            'spacing': unit['spacing'],
            'steering': np.deg2rad(unit['steering']),
            'array_type': unit['type'],
            'curvature': unit['curvature'],
            'frequency': unit['frequency'],
            'x_position': unit['x_position'],
            'y_position': unit['y_position'],
            'phase': unit['phase'],
            'id': unit['id']
        } for unit in units]

    def _get_current_params(self):
        return {
            'elements': self.elements.value(),
            'spacing': self.spacing.value(),
            'steering': self.steering.value(),  # Keep in degrees, let visualization controller handle conversion
            'array_type': self.array_type.currentText().lower(),
            'curvature': self.curvature.value(),
            'frequency': self.frequency.value(),
            'x_position': self.x_position.value(),
            'y_position': self.y_position.value(),
            'phase': 0
        }

    def _update_all_plots(self, params_list):
        self.visualization_panel.update_plots(params_list, self.visualization_controller)
        
    def _apply_stylesheet(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #111827;
                font-family: 'Arial', sans-serif;
            }

            QLabel {
                color: white;
                font-size: 10pt;
            }

            QGroupBox {
                background-color: #1F2937;
                border-radius: 8px;
                padding: 3px;
                color: white;
                font-weight: bold;
            }

            QSpinBox, QDoubleSpinBox, QComboBox {
                background-color: #374151;
                color: white;
                border: 1px solid #4B5563;
                border-radius: 4px;
                padding: 8px;
                font-size: 10pt;
            }

            QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
                border: 1px solid #2563EB;
                background-color: #1F2937;
            }

            QPushButton {
                background-color: #2563EB;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 10pt;
            }

            QPushButton:hover {
                background-color: #1D4ED8;
                border-radius: 4px;
            }

            QPushButton:pressed {
                background-color: #1E40AF;
                border-radius: 4px;
            }

            QScrollArea {
                border: none;
                background-color: #111827;
            }

            QScrollBar:vertical, QScrollBar:horizontal {
                border: none;
                background-color: #374151;
                width: 4px;
                height: 4px;
            }

            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                background-color: #2563EB;
                border-radius: 4px;
            }

            QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {
                background-color: #1D4ED8;
            }

            QFrame {
                background-color: #1F2937;
                border-radius: 8px;
                padding: 5px;
                color: white;
            }

            QLineEdit {
                background-color: #374151;
                color: white;
                border: 1px solid #4B5563;
                border-radius: 4px;
                padding: 3px 5px;
            }

            QLineEdit:focus {
                border: 1px solid #2563EB;
                background-color: #1F2937;
            }

            QComboBox {
                background-color: #374151;
                color: white;
                border: 1px solid #4B5563;
                border-radius: 4px;
                padding: 4px;
            }

            QComboBox:focus {
                border: 1px solid #2563EB;
                background-color: #1F2937;
            }

            QTabWidget::pane {
                background-color: #1F2937;
                border: none;
            }

            QTabBar::tab {
                background-color: #374151;
                color: white;
                padding: 4px;
                border-radius: 4px;
            }

            QTabBar::tab:selected {
                background-color: #2563EB;
                color: white;
            }

            QTabBar::tab:hover {
                background-color: #1D4ED8;
            }

            QToolTip {
                background-color: #2563EB;
                color: white;
                border-radius: 4px;
                padding: 4px;
                font-size: 2pt;
            }
        """)

