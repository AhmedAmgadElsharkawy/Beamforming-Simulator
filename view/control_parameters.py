class ControlParameters:
    def __init__(self):
        self.array_type = "Linear"
        self.elements = 16
        self.spacing = 0.5
        self.steering = 0.0
        self.phase = 0.0
        self.curvature = 1.0
        self.frequency = 100.0
        self.x_position = 0.0
        self.y_position = 0.0

    def get_parameters(self):
        return {
            "array_type": self.array_type,
            "elements": self.elements,
            "spacing": self.spacing,
            "steering": self.steering,
            "phase": self.phase,
            "curvature": self.curvature,
            "frequency": self.frequency,
            "x_position": self.x_position,
            "y_position": self.y_position,
        }