class InvalidConfigurationException(Exception):
    def __init__(self, message):
        self.message = message


class DbConnectionParameters:
    def __init__(self, host: str, port: int, username: str, password: str):
        self.__check_param("host", host)
        self.__check_port("port", port)
        self.__check_param("username", username)
        self.__check_param("password", password)
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def __check_param(self, name: str, value: str):
        if not value or value.isspace():
            raise InvalidConfigurationException(
                "Required connection parameter {} is missing".format(name))

    def __check_port(self, name: str, value: int):
        if value <= 0:
            raise InvalidConfigurationException(
                "Required connection parameter port is not valid or missing".format(name))


class Configuration:
    def __init__(self, left: DbConnectionParameters, right: DbConnectionParameters):
        self.left = left
        self.right = right
