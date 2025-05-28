from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class StreetTable():
    __tablename__ = "streets"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)

    # Relationships
    buildings = relationship("BuildingTable", back_populates="street")
