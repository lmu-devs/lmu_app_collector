from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class Room(BaseModel):
    id: str = Field(alias="code")
    title: str = Field(alias="name")
    floor: str = Field(alias="floorCode")
    pos_x: Optional[int] = Field(alias="posX", default=None)
    pos_y: Optional[int] = Field(alias="posY", default=None)

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "Room":
        return cls(**data)

    @classmethod
    def from_json_list(cls, json_list: List[Dict[str, str]]) -> List["Room"]:
        return [cls.from_dict(item) for item in json_list]
