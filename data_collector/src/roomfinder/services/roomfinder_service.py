import json
from collections import defaultdict
from typing import Dict, List

from data_collector.src.roomfinder.models import Building, Floor, Room, Street
from shared.src.services.directus_service import DirectusService


class RoomfinderService:
    def __init__(self):
        self.directus = DirectusService()
        self.streets = self._get_streets()
        self.buildings = self._get_buildings()
        self.floors = self._get_floors()
        self.rooms = self._get_rooms()

    def _get_streets(self) -> List[Street]:
        with open("data_collector/src/roomfinder/constants/2_street.json") as f:
            street_data = json.load(f)
            return Street.from_json_list(street_data)

    def _get_buildings(self) -> List[Building]:
        with open("data_collector/src/roomfinder/constants/3_building.json") as f:
            building_data = json.load(f)
            return Building.from_json_list(building_data)

    def _get_floors(self) -> List[Floor]:
        with open("data_collector/src/roomfinder/constants/5_floor.json") as f:
            floor_data = json.load(f)
            return Floor.from_json_list(floor_data)

    def _get_rooms(self) -> List[Room]:
        with open("data_collector/src/roomfinder/constants/6_room.json") as f:
            room_data = json.load(f)
            return Room.from_json_list(room_data)

    def _build_nested_structure(self) -> List[Street]:
        """Build the nested structure of streets -> buildings -> floors -> rooms"""

        # Create lookup dictionaries for efficient grouping
        rooms_by_floor: Dict[str, List[Room]] = defaultdict(list)
        floors_by_building: Dict[str, List[Floor]] = defaultdict(list)
        buildings_by_street: Dict[str, List[Building]] = defaultdict(list)

        # Group rooms by floor
        for room in self.rooms:
            rooms_by_floor[room.floor].append(room)

        # Assign rooms to floors and group floors by building
        for floor in self.floors:
            floor.rooms = rooms_by_floor.get(floor.id, [])
            floors_by_building[floor.building].append(floor)

        # Assign floors to buildings and group buildings by street
        for building in self.buildings:
            building.floors = floors_by_building.get(building.building_part_id, [])
            buildings_by_street[building.street].append(building)

        # Assign buildings to streets
        for street in self.streets:
            street.buildings = buildings_by_street.get(street.id, [])

        return self.streets

    def update_database(self) -> Dict:
        """Updates all roomfinder related data using GraphQL mutations"""

        # Build the nested structure
        nested_streets = self._build_nested_structure()

        # Convert to JSON format for GraphQL
        streets_data = []
        for street in nested_streets:
            street_dict = street.model_dump(by_alias=True, exclude_none=True)
            streets_data.append(street_dict)

        # Execute the GraphQL mutation
        variables = {"data": streets_data}

        try:
            result = self.directus.execute_query_file(
                "data_collector/src/roomfinder/graphql/roomfinder_mutation.graphql",
                variables,
            )
            return result
        except Exception as e:
            print(f"Error executing GraphQL mutation: {e}")
            raise

    def get_nested_data(self) -> List[Dict]:
        """Get the nested data structure as JSON for inspection"""
        nested_streets = self._build_nested_structure()
        return [
            street.model_dump(by_alias=True, exclude_none=True)
            for street in nested_streets
        ]


if __name__ == "__main__":
    service = RoomfinderService()

    # Print sample nested structure
    nested_data = service.get_nested_data()
    print("Sample nested structure:")
    print(json.dumps(nested_data[:1], indent=2))  # Print first street only for brevity

    # Uncomment to actually update the database
    # result = service.update_database()
    # print("GraphQL mutation result:", result)
