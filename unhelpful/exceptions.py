class UnhelpfulException(Exception):
    """parent exception for project"""


class RobinhoodException(UnhelpfulException):
    """parent exception for all robinhood connections"""


class RobinhoodNoLogin(RobinhoodException):
    """Lacking login credentials, must be called as part of the context-manager scope"""


class TickerNotFound(RobinhoodException):
    """Unable to find instrument/ticker for a requested company symbol"""
