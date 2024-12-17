import uuid

class ScenarioManager:
    """Manages array scenarios and their states"""
    def __init__(self):
        self.scenarios = []
        self.active_scenario_id = None
        self.visible_scenarios = {}

    def add_scenario(self, arrays, name=""):
        scenario_id = str(uuid.uuid4())
        scenario = {
            'id': scenario_id,
            'name': name,
            'arrays': [array.to_dict() for array in arrays],
            'visible': True
        }
        self.scenarios.append(scenario)
        self.visible_scenarios[scenario_id] = True
        return scenario_id

    def get_scenario(self, scenario_id):
        return next((s for s in self.scenarios if s['id'] == scenario_id), None)

    def delete_scenario(self, scenario_id):
        self.scenarios = [s for s in self.scenarios if s['id'] != scenario_id]
        if scenario_id in self.visible_scenarios:
            del self.visible_scenarios[scenario_id]
        if self.active_scenario_id == scenario_id:
            self.active_scenario_id = None

    def toggle_scenario_visibility(self, scenario_id):
        scenario = self.get_scenario(scenario_id)
        if scenario:
            scenario['visible'] = not scenario['visible']
            self.visible_scenarios[scenario_id] = scenario['visible']
            return scenario['visible']
        return False

    def get_visible_scenarios(self):
        return [s for s in self.scenarios if s['visible']]

    def set_active_scenario(self, scenario_id):
        # Set all scenarios to not visible first
        for scenario in self.scenarios:
            scenario['visible'] = False
        
        # Make the selected scenario visible
        selected_scenario = self.get_scenario(scenario_id)
        if selected_scenario:
            selected_scenario['visible'] = True
            self.active_scenario_id = scenario_id

    def get_active_scenario(self):
        return self.get_scenario(self.active_scenario_id)
