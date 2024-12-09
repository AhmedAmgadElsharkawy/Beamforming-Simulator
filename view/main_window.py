from inspect import Parameter
import parameters
import sys
import numpy as np
from PyQt5.QtWidgets import (
    QMainWindow,QVBoxLayout, QGridLayout, QGroupBox, QLabel, QSpinBox, QDoubleSpinBox, 
    QComboBox, QPushButton, QScrollArea, QWidget,QHBoxLayout
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from controller.plotting_functions import (
    plot_beam_pattern,
    plot_top_xy,
    plot_interference,
    plot_bottom_xy
)
from view.saved_unit import SavedUnit
from view.saved_scenarios import SavedScenario
import matplotlib.pyplot as plt

class BeamformingSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("2D Beamforming Simulator")
        self.saved_units = []
        self.scenarios = []
        self.active_scenario = None
        self.active_scenario_id = None
        self.setup_ui()
        self.setup_connections()
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
    def setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        self.setup_visualizations(layout)
        self.setup_controls(layout)

    def setup_connections(self):
        # Connect UI components to update the parameters object
        self.array_type.currentIndexChanged.connect(
            lambda: setattr(parameters, "array_type", self.array_type.currentText())
        )
        self.elements.valueChanged.connect(
            lambda value: setattr(parameters, "elements", value)
        )
        self.spacing.valueChanged.connect(
            lambda value: setattr(parameters, "spacing", value)
        )
        self.steering.valueChanged.connect(
            lambda value: setattr(parameters, "steering", value)
        )
        self.phase.valueChanged.connect(
            lambda value: setattr(parameters, "phase", value)
        )
        self.curvature.valueChanged.connect(
            lambda value: setattr(parameters, "curvature", value)
        )
        self.frequency.valueChanged.connect(
            lambda value: setattr(parameters, "frequency", value)
        )
        self.x_position.valueChanged.connect(
            lambda value: setattr(parameters, "x_position", value)
        )
        self.y_position.valueChanged.connect(
            lambda value: setattr(parameters, "y_position", value)
        )
    def setup_visualizations(self, layout):
        left_layout = QGridLayout()
        
        # Bottom-left - X-Y graph
        self.bottom_xy_figure = plt.figure(figsize=(5, 3), facecolor='#111827')  
        self.bottom_xy_canvas = FigureCanvas(self.bottom_xy_figure)
        self.bottom_xy_ax = self.bottom_xy_figure.add_subplot(111)
        self.bottom_xy_ax.set_facecolor('#111827')
        self.bottom_xy_ax.tick_params(colors='white')
        self.bottom_xy_ax.grid(True, color='gray', linestyle='--', linewidth=0.5)
        self.bottom_xy_ax.set_xticks(np.arange(-50, 51, 10))
        self.bottom_xy_ax.set_yticks(np.arange(-50, 51, 10))
        left_layout.addWidget(self.bottom_xy_canvas, 1, 0)

        # Top-left - X-Y graph
        self.top_xy_figure = plt.figure(figsize=(5, 3), facecolor='#111827')  
        self.top_xy_canvas = FigureCanvas(self.top_xy_figure)
        self.top_xy_ax = self.top_xy_figure.add_subplot(111)
        self.top_xy_ax.set_facecolor('#111827')
        self.top_xy_ax.tick_params(colors='white')
        self.top_xy_ax.grid(True, color='gray', linestyle='--', linewidth=0.5)
        self.top_xy_ax.set_xticks(np.arange(-100, 101, 25))
        self.top_xy_ax.set_yticks(np.arange(-100, 101, 25))
        left_layout.addWidget(self.top_xy_canvas, 0, 0)

        # Top-right - Beam Pattern
        self.beam_figure = plt.figure(figsize=(5, 3), facecolor='#111827')  
        self.beam_canvas = FigureCanvas(self.beam_figure)
        self.beam_ax = self.beam_figure.add_subplot(111, projection='polar')
        self.beam_ax.set_facecolor('#111827')
        self.beam_ax.tick_params(colors='white')
        left_layout.addWidget(self.beam_canvas, 0, 1)

        # Bottom-right - Interference Pattern
        self.interference_figure = plt.figure(figsize=(5, 3), facecolor='#111827')  
        self.interference_canvas = FigureCanvas(self.interference_figure)
        self.interference_ax = self.interference_figure.add_subplot(111)
        self.interference_ax.set_facecolor('#111827')
        self.interference_ax.tick_params(colors='white')
        left_layout.addWidget(self.interference_canvas, 1, 1)
        
        layout.addLayout(left_layout, stretch=2)


    def setup_controls(self, layout):
        controls_layout = QVBoxLayout()

        # Current Unit Controls
        current_unit_group = QGroupBox("Current Unit")
        current_unit_layout = QGridLayout()

        # Array Type
        current_unit_layout.addWidget(QLabel("Array Type:"), 0, 0)
        self.array_type = QComboBox()
        self.array_type.addItems(["Linear", "Curved"])
        current_unit_layout.addWidget(self.array_type, 0, 1)

        # Elements
        current_unit_layout.addWidget(QLabel("Elements:"), 1, 0)
        self.elements = QSpinBox()
        self.elements.setRange(1, 100)
        self.elements.setValue(16)
        current_unit_layout.addWidget(self.elements, 1, 1)

        # Spacing
        current_unit_layout.addWidget(QLabel("Spacing (λ):"), 2, 0)
        self.spacing = QDoubleSpinBox()
        self.spacing.setRange(0.1, 10.0)
        self.spacing.setValue(0.5)
        self.spacing.setSingleStep(0.1)
        current_unit_layout.addWidget(self.spacing, 2, 1)

        # Steering
        current_unit_layout.addWidget(QLabel("Steering (°):"), 3, 0)
        self.steering = QDoubleSpinBox()
        self.steering.setRange(-90, 90)
        self.steering.setValue(0)
        current_unit_layout.addWidget(self.steering, 3, 1)

        # Phase
        current_unit_layout.addWidget(QLabel("Phase (°):"), 4, 0)
        self.phase = QDoubleSpinBox()
        self.phase.setRange(-360, 360)
        self.phase.setValue(0)
        current_unit_layout.addWidget(self.phase, 4, 1)

        # Curvature Factor
        current_unit_layout.addWidget(QLabel("Curvature:"), 5, 0)
        self.curvature = QDoubleSpinBox()
        self.curvature.setRange(0.1, 10.0)
        self.curvature.setValue(1.0)
        self.curvature.setSingleStep(0.1)
        current_unit_layout.addWidget(self.curvature, 5, 1)

        # Frequency
        current_unit_layout.addWidget(QLabel("Frequency (MHz):"), 6, 0)
        self.frequency = QDoubleSpinBox()
        self.frequency.setRange(1, 1000)
        self.frequency.setValue(100)
        current_unit_layout.addWidget(self.frequency, 6, 1)

        # X-Position
        current_unit_layout.addWidget(QLabel("X-Position:"), 7, 0)
        self.x_position = QDoubleSpinBox()
        self.x_position.setRange(-50, 50)
        self.x_position.setValue(0.0)
        self.x_position.setSingleStep(0.1)
        current_unit_layout.addWidget(self.x_position, 7, 1)

        # Y-Position
        current_unit_layout.addWidget(QLabel("Y-Position:"), 8, 0)
        self.y_position = QDoubleSpinBox()
        self.y_position.setRange(-50, 50)
        self.y_position.setValue(0.0)
        self.y_position.setSingleStep(0.1)
        current_unit_layout.addWidget(self.y_position, 8, 1)

        # Save Unit button
        self.save_unit_btn = QPushButton("Save Unit")
        self.save_unit_btn.clicked.connect(self.save_current_unit)
        current_unit_layout.addWidget(self.save_unit_btn, 9, 0, 1, 2)

        current_unit_group.setLayout(current_unit_layout)
        controls_layout.addWidget(current_unit_group)

        # Saved Units
        saved_units_group = QGroupBox("Saved Units")
        saved_units_layout = QHBoxLayout()

        # Left half - Units
        left_layout = QVBoxLayout()
        left_scroll = QScrollArea()
        left_scroll.setWidgetResizable(True)
        left_scroll.setStyleSheet("background-color: #1F2937;")
        left_scroll_content = QWidget()
        self.saved_units_layout = QVBoxLayout(left_scroll_content)
        left_scroll.setWidget(left_scroll_content)
        left_layout.addWidget(left_scroll)

        # Add Scenario button at the bottom of left panel
        add_scenario_btn = QPushButton("Add Scenario")
        add_scenario_btn.clicked.connect(self.save_scenario)
        add_scenario_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 8pt;
                margin-top: 4px;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
        """)
        left_layout.addWidget(add_scenario_btn)

        # Right half - Scenarios
        right_layout = QVBoxLayout()
        right_scroll = QScrollArea()
        right_scroll.setWidgetResizable(True)
        right_scroll.setStyleSheet("background-color: #1F2937;")
        right_scroll_content = QWidget()
        self.scenarios_layout = QVBoxLayout(right_scroll_content)
        right_scroll.setWidget(right_scroll_content)
        right_layout.addWidget(right_scroll)

        # Add both halves to the main saved units layout
        saved_units_layout.addLayout(left_layout)
        saved_units_layout.addLayout(right_layout)

        saved_units_group.setLayout(saved_units_layout)
        controls_layout.addWidget(saved_units_group)

        layout.addLayout(controls_layout, stretch=1)

    def save_scenario(self):
        if not self.saved_units:
            return
            
        scenario_data = {
            'id': len(self.scenarios) + 1,
            'units': self.saved_units.copy()
        }
        self.scenarios.append(scenario_data)
        self.update_scenarios_display()

    def delete_scenario(self, scenario_id):
        if self.active_scenario_id == scenario_id:
            self.active_scenario_id = None
            self.clear_patterns()
        self.scenarios = [s for s in self.scenarios if s['id'] != scenario_id]
        self.update_scenarios_display()

   

    def update_patterns_with_units(self, units):
        # Update plots with specific units

        params = parameters.get_parameters()
        plot_beam_pattern(self.beam_ax, units)
        plot_top_xy(self.top_xy_ax, units)
        plot_interference(self.interference_ax, units)
        plot_bottom_xy(self.bottom_xy_ax, units)
        
        # Refresh canvases
        self.beam_canvas.draw()
        self.top_xy_canvas.draw()
        self.interference_canvas.draw()
        self.bottom_xy_canvas.draw()

    def update_scenarios_display(self):
        # Clear existing scenarios
        while self.scenarios_layout.count():
            child = self.scenarios_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Add scenarios
        for scenario in self.scenarios:
            scenario_widget = SavedScenario(
                scenario_data=scenario,
                on_delete=self.delete_scenario,
                on_visibility_toggle=self.toggle_scenario_visibility,
                is_visible=(scenario == self.active_scenario)
            )
            self.scenarios_layout.addWidget(scenario_widget)

    def save_current_unit(self):
        unit_data = {
            'id': len(self.saved_units) + 1,
            'type': self.array_type.currentText().lower(),
            'elements': self.elements.value(),
            'spacing': self.spacing.value(),
            'steering': self.steering.value(),
            'phase': self.phase.value(),
            'curvature': self.curvature.value(),
            'frequency': self.frequency.value(),
            'x_position': self.x_position.value(),
            'y_position': self.y_position.value()
        }
        self.saved_units.append(unit_data)
        self.update_saved_units_display()

        self.clear_patterns()

    def clear_patterns(self):
        # Clear all plots
        self.beam_ax.clear()
        self.top_xy_ax.clear()
        self.interference_ax.clear()
        self.bottom_xy_ax.clear()
        
        # Reset basic plot properties
        self.top_xy_ax.grid(True, color='gray', linestyle='--', linewidth=0.5)
        self.bottom_xy_ax.grid(True, color='gray', linestyle='--', linewidth=0.5)
        
        # Refresh canvases
        self.beam_canvas.draw()
        self.top_xy_canvas.draw()
        self.interference_canvas.draw()
        self.bottom_xy_canvas.draw()

    def save_scenario(self):
        if not self.saved_units:
            return
            
        scenario_data = {
            'id': len(self.scenarios) + 1,
            'units': self.saved_units.copy(),
            'visible': False
        }
        self.scenarios.append(scenario_data)
        self.update_scenarios_display()
        # Clear saved units after creating scenario
        self.saved_units = []
        self.update_saved_units_display()

    def toggle_scenario_visibility(self, scenario_id, visible):
        # If the scenario is already active (visible), turn it off
        if self.active_scenario_id == scenario_id and visible:
            # Hide the current scenario
            for scenario in self.scenarios:
                if scenario['id'] == scenario_id:
                    scenario['visible'] = False
            
            # Clear the active scenario and patterns
            self.active_scenario_id = None
            self.clear_patterns()
        else:
            # Turn off any currently visible scenario
            for scenario in self.scenarios:
                scenario['visible'] = False
            
            # If making the new scenario visible
            if visible:
                # Set the new active scenario
                self.active_scenario_id = scenario_id
                # Find and update patterns with the selected scenario's units
                active_scenario = next((s for s in self.scenarios if s['id'] == scenario_id), None)
                if active_scenario:
                    active_scenario['visible'] = True
                    self.update_patterns_with_units(active_scenario['units'])
            else:
                # If not visible, reset the active scenario ID
                self.active_scenario_id = None
        
        # Refresh the scenarios display to reflect changes
        self.update_scenarios_display()

    def delete_scenario(self, scenario_id):
        # If the scenario to be deleted is the active one
        if self.active_scenario_id == scenario_id:
            self.active_scenario_id = None
            self.clear_patterns()
        
        # Remove the scenario
        self.scenarios = [s for s in self.scenarios if s['id'] != scenario_id]
        
        # If no scenarios left, clear patterns
        if not self.scenarios:
            self.clear_patterns()
        # If scenarios exist, display the first scenario
        elif self.scenarios:
            first_scenario = self.scenarios[0]
            self.toggle_scenario_visibility(first_scenario['id'], True)
        
        # Update the display
        self.update_scenarios_display()
    def update_saved_units_display(self):
        while self.saved_units_layout.count():
            child = self.saved_units_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
        for unit_data in self.saved_units:
            unit_widget = SavedUnit(
                unit_data=unit_data,
                on_delete=self.delete_unit
            )
            self.saved_units_layout.addWidget(unit_widget)
   
    def delete_unit(self, unit_id):
        self.saved_units = [u for u in self.saved_units if u['id'] != unit_id]
        self.update_saved_units_display()

    def delete_unit(self, unit_id):
        self.saved_units = [u for u in self.saved_units if u['id'] != unit_id]
        self.update_saved_units_display()

    def update_patterns_with_units(self, units):
        # Update plots with specific units
        plot_beam_pattern(self.beam_ax, units)
        plot_top_xy(self.top_xy_ax, units)
        plot_interference(self.interference_ax, units)
        plot_bottom_xy(self.bottom_xy_ax, units)
        
        # Refresh canvases
        self.beam_canvas.draw()
        self.top_xy_canvas.draw()
        self.interference_canvas.draw()
        self.bottom_xy_canvas.draw()