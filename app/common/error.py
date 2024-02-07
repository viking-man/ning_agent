class ParameterException(Exception):
    def __init__(self, parameter_name, message="Invalid parameter."):
        self.parameter_name = parameter_name
        self.message = message
        super().__init__(self.message)