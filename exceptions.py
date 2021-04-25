class SaveNotFoundError(Exception):
    def __init__(self, message="save doesn't exist"):
        super().__init__(message)

class SaveExistsError(Exception):
    def __init__(self, message="save already exists"):
        super().__init__(message)

class InvalidSettingsError(Exception):
    def __init__(self, message='BTD6 Save Directory or BTD6 Exe Directory are not set'):
        super().__init__(message)