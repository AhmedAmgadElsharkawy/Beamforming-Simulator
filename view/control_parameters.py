class ControlParameters:
    def __init__(self):
        self.params_list = []
        self.add_new_array()
        
    def add_new_array(self):
        params = {
            "array_type": "Linear",
            "elements": 16,
            "spacing": 0.5,
            "steering": 0.0,
            "phase": 0.0,
            "curvature": 1.0,
            "frequency": 100.0,
            "x_position": 0.0,
            "y_position": 0.0,
            "id": len(self.params_list) + 1
        }
        self.params_list.append(params)
        
    def get_parameters(self):
        return self.params_list
        
    def update_array_parameters(self, array_id, **kwargs):
        for params in self.params_list:
            if params['id'] == array_id:
                params.update(kwargs)
                break
                
    def remove_array(self, array_id):
        self.params_list = [p for p in self.params_list if p['id'] != array_id]
