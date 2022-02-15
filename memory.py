class Memory:

    def __init__(self):
        self.mode = None
        self.patch = []
        self.bank = {}
        self.active_patch = None
        self.active_bank = None
        self.selected_bank = None
        self.selected_patch = None
        self.write_location = None
        self.debug = True

    def change_mode(self, newMode):
        self.mode = newMode

    def get_mode(self):
        return self.mode

    def clear_all(self):
        self.patch.clear()

    def load_one(self, instruction):
        if self.patch.count(instruction) == 0:
            self.patch.append(instruction)
        elif self.patch.count(instruction) == 1:
            self.patch.remove(instruction)

    def set_active_bank(self):
        self.active_bank = self.selected_bank
        self.active_patch = self.selected_patch

    def get_active_bank(self):
        return self.active_bank

    def get_patch(self):
        return self.patch

    def load_patch(self, patch_address):
        self.patch = self.bank[str(patch_address)]

    def load_selected_patch(self):
        self.patch = self.bank[str(self.selected_patch)]

    def get_active_patch(self):
        return self.active_patch

    def load_bank(self, bank):
        self.bank = bank

    def get_write_location(self):
        return self.write_location

    def set_write_location(self, newAdd):
        self.write_location = newAdd

    def copy_write_location(self):
        self.selected_patch = self.write_location

    def reset_write_location(self):
        self.write_location = None

    def get_selected_patch(self):
        return self.selected_patch

    def set_selected_patch(self, new):
        self.selected_patch = new

    def get_selected_bank(self):
        return self.selected_bank

    def set_selected_bank(self, new):
        self.selected_bank = new

    def increment_bank(self):
        if self.selected_bank < 5:
            self.selected_bank += 1

    def decrement_bank(self):
        if self.selected_bank > 1:
            self.selected_bank -= 1

    def enable_debug(self):
        self.debug = True
