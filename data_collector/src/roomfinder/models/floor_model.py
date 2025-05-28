from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from data_collector.src.roomfinder.models.room_model import Room


class Floor(BaseModel):
    id: str = Field(alias="code")
    level: str
    title: str = Field(alias="name")
    map_uri: str = Field(alias="mapUri")
    building: str = Field(alias="buildingPartCode")
    map_size_x: Optional[int] = Field(alias="mapSizeX", default=None)
    map_size_y: Optional[int] = Field(alias="mapSizeY", default=None)
    rooms: Optional[List["Room"]] = Field(default_factory=list)

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "Floor":
        return cls(**data)

    @classmethod
    def from_json_list(cls, json_list: List[Dict[str, str]]) -> List["Floor"]:
        return [cls.from_dict(item) for item in json_list]

