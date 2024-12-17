from model.array_parameters import ArrayParameters
from datetime import datetime

class ArrayController:
    def __init__(self, visualization_controller):
        self.visualization_controller = visualization_controller
        self.arrays = []
        self.selected_arrays = {}
        self.id_counter = 1

    def create_array(self, params_dict):
        array = ArrayParameters()
        array.id = self.id_counter
        self.id_counter += 1  # Always increment, never reuse
        array.from_dict(params_dict)
        self.arrays.append(array)
        self.selected_arrays[array.id] = True
        
        visible_arrays = [array.to_dict() for array in self.arrays 
                        if self.selected_arrays.get(array.id, True)]
        self.visualization_controller.update_plots(visible_arrays)
        return array.id

    def update_array(self, array_id, params_dict):
        array = self.get_array(array_id)
        if array:
            array.from_dict(params_dict)
            # Get visualization panel from main window
            main_window = self.visualization_controller.main_window
            # Get only visible arrays
            params_list = [a.to_dict() for a in self.arrays 
                        if self.selected_arrays.get(a.id, True)]
            main_window.visualization_panel.update_plots(params_list, self.visualization_controller)
            return True
        return False

    def delete_array(self, array_id):
        # Remove array from arrays list
        self.arrays = [array for array in self.arrays if array.id != array_id]
        self.selected_arrays.pop(array_id, None)
        
        # Get remaining visible arrays
        visible_arrays = [array.to_dict() for array in self.arrays 
                        if self.selected_arrays.get(array.id, True)]
        
        # Update plots with remaining arrays
        self.visualization_controller.update_plots(visible_arrays)
        main_window = self.visualization_controller.main_window
        main_window.visualization_panel.refresh_all_canvases()
        self.visualization_controller.main_window.update_saved_units_display()

    def get_array(self, array_id):
        return next((a for a in self.arrays if a.id == array_id), None)

    def toggle_array_visibility(self, array_id, is_visible):
        self.selected_arrays[array_id] = is_visible
        
        # Get only the visible arrays for calculations
        visible_arrays = [array.to_dict() for array in self.arrays 
                        if self.selected_arrays.get(array.id, True)]
        
        # Update all plots with only visible arrays
        self.visualization_controller.update_plots(visible_arrays)
        
        # Force refresh of visualization panel
        main_window = self.visualization_controller.main_window
        main_window.visualization_panel.refresh_all_canvases()


