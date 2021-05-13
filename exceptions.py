class SaveNotFoundError(Exception):
    def __init__(self, message="save doesn't exist"):
        super().__init__(message)

class SaveExistsError(Exception):
    def __init__(self, message="save already exists"):
        super().__init__(message)

class InvalidSettingsError(Exception):
    def __init__(self, message='BTD6 Save Directory or BTD6 Exe Directory are not set'):
        super().__init__(message)

class IncorrectBtd6ExeDir(Exception):
    def __init__(self, message='BTD6 Exe Directory is incorrect'):
        super().__init__(message)

class IncorrectBtd6SaveDir(Exception):
    def __init__(self, message='BTD6 Save Directory is incorrect'):
        super().__init__(message)

class InvalidHotkeys(Exception):
    def __init__(self, message='Hotkeys are Invalid Try Setting Them Again in Settings'):
        super().__init__(message)

class SaveMissingData(Exception):
    def __init__(self, message='the save you are loading is missing data, it is missing either Profile.Save or Profile.bak file'):
        super().__init__(message)
