class TitanFileError(Exception):
    pass

class TitanFileAuthError(TitanFileError):
    pass

class TitanFileAPIError(TitanFileError):
    pass
