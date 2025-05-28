from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from data_collector.src.roomfinder.models.building_model import Building


class Street(BaseModel):
    id: str = Field(alias="code")
    title: str = Field(alias="name")
    buildings: Optional[List["Building"]] = Field(default_factory=list)

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "Street":
        return cls(**data)

    @classmethod
    def from_json_list(cls, json_list: List[Dict[str, str]]) -> List["Street"]:
        return [cls.from_dict(item) for item in json_list]
