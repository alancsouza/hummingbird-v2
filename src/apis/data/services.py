from models import City
from models import CasesLocation
from sqlalchemy.sql import or_


class ReportService:

    def search_on_location_by_term(self, query):
        cases = City.query.filter(
            or_(City.city.like(query), City.state.like(query))
        ).all()

        result = []

        for case in cases:
            current_case = {
                'city': case.city,
                'state': case.state,
                'cases': case.totalcases
            }
            result.append(current_case)

        return result

    def get_all_city_cases(self):
        all_cases = City.query.all()
        return compile_cases(all_cases)

    def search_city_cases_by_state(self, state_code):
        city_situation = City.query.filter_by(
            state=state_code).all()
        return compile_cases(city_situation)

    def get_cases_near_location(self, latitude, longitude):
        # FIX: Why those variables has not been used?
        all_cases = CasesLocation.query.all()
        return compile_cases_near_location(all_cases)


def compile_cases(data):
    totalcases = sum(
        [city.totalcases
         for city in data]) or 0

    return {
        'totalCases': totalcases
    }


def compile_cases_near_location(data):
    for case in data:
        return {
            'status': case.status,
            'location': {
                'latitude': case.longitude,
                'longitude': case.latitude
            }
        }
