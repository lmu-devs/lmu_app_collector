from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from data_collector.src.roomfinder.models.floor_model import Floor


class Building(BaseModel):
    building_part_id: str = Field(alias="buildingPartCode")
    title: str
    address: str
    location: Optional[Dict] = Field(default=None)
    aliases: Optional[List[str]] = Field(default=None)
    street: str = Field(alias="streetCode")
    building_code: Optional[str] = Field(alias="buildingCode", default=None)
    lat: Optional[float] = Field(default=None)
    lng: Optional[float] = Field(default=None)
    floors: Optional[List["Floor"]] = Field(default_factory=list)

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True

    def __init__(self, **data):
        # Convert lat/lng to location if they exist
        if (
            "lat" in data
            and "lng" in data
            and data["lat"] is not None
            and data["lng"] is not None
        ):
            data["location"] = {
                "type": "Point",
                "coordinates": [data["lng"], data["lat"]],
            }
        super().__init__(**data)

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "Building":
        return cls(**data)

    @classmethod
    def from_json_list(cls, json_list: List[Dict[str, str]]) -> List["Building"]:
        return [cls.from_dict(item) for item in json_list]
