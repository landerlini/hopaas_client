class HopaasError (RuntimeError):
    pass

class HopaasServerError(HopaasError):
    pass

class HopaasConsistencyError(HopaasError):
    pass
