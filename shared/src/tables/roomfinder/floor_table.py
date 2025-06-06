from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class FloorTable():
    __tablename__ = "floors"

    id = Column(String, primary_key=True)
    level = Column(String, nullable=False)
    name = Column(String, nullable=False)
    map_uri = Column(String, nullable=False)
    map_size_x = Column(Integer, nullable=False)
    map_size_y = Column(Integer, nullable=False)
    building_part_id = Column(String, ForeignKey("buildings.building_part_id"), nullable=False)

    # Relationships
    rooms = relationship("RoomTable", back_populates="floor")
    building = relationship("BuildingTable", back_populates="floors")
