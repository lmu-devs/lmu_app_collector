from sqlalchemy import Column, Time
from sqlalchemy.ext.declarative import declared_attr


class TimeRange():
    """
    Abstract base class for time range.
    Declares a time range column.
    """

    __abstract__ = True

    @declared_attr
    def start_time(cls):
        return Column(Time, nullable=False)

    @declared_attr
    def end_time(cls):
        return Column(Time, nullable=False)
