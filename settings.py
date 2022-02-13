import json
path = "/data/settings.json"
class Settings:

    def __init__(self):
        self.params = []
        self.selected_param = 0
        self.selected_option = 0
        self.param_edit = False
        self.menu_open = False

    def load_settings(self):
        with open(path, "r") as file:
            data = json.load(file)
            self.params = data["settings"]

    def save_settings(self):
        with open(path, "w") as file:
            data = json.dump(params, file)

    def increment_position(self):
        if self.menu_open:
            if self.selected_param < len(params) -1:
                selected_param += 1
        elif self.param_edit:
            if self.option < len(params[selected_param]) -1:
                selected_option += 1

    def decrement_position(self):
        if self.menu_open:
            if self.selected_param < len(params) -1:
                selected_param -= 1
        elif self.param_edit:
            if self.option < len(params[selected_param]) -1:
                selected_option -= 1

    def reset_position(self):
        self.selected_param = 0
        self.selected_option = 0


# settings = Settings()
