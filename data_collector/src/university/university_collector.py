from data_collector.src.core.base_collector import BaseCollector
from data_collector.src.university.services.faculty_service import FacultyService
from data_collector.src.university.services.university_service import UniversityService


class UniversityCollector(BaseCollector):
    async def _collect_data(self, db):
        service = UniversityService(db)
        faculty_service = FacultyService(db)
        service.add_universities()
        faculty_service.add_faculties()
