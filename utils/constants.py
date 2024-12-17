# Application Constants
DEFAULT_ARRAY_PARAMS = {
    "ELEMENTS": 16,
    "SPACING": 0.5,
    "STEERING": 0.0,
    "PHASE": 0.0,
    "CURVATURE": 1.0,
    "FREQUENCY": 100.0,
    "X_POSITION": 0.0,
    "Y_POSITION": 0.0
}

# Plot Configuration
PLOT_CONFIG = {
    "BACKGROUND_COLOR": "#111827",
    "GRID_COLOR": "gray",
    "GRID_STYLE": "--",
    "GRID_WIDTH": 0.5
}

# UI Style Constants
UI_COLORS = {
    "BACKGROUND": "#111827",
    "SECONDARY_BG": "#1F2937",
    "PRIMARY": "#2563EB",
    "PRIMARY_HOVER": "#1D4ED8",
    "DANGER": "#EF4444",
    "DANGER_HOVER": "#DC2626",
    "TEXT": "white"
}

# Array Types
ARRAY_TYPES = ["Linear", "Curved"]

# Parameter Ranges
PARAM_RANGES = {
    "ELEMENTS": (1, 100),
    "SPACING": (0.1, 10.0),
    "STEERING": (-90, 90),
    "PHASE": (-360, 360),
    "CURVATURE": (0.1, 10.0),
    "FREQUENCY": (1, 1000),
    "POSITION": (-50, 50)
}
