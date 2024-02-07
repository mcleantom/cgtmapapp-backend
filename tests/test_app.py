from unittest import TestCase
from cgt_map_backend.config import CGTMapBackendConfig
from fastapi.testclient import TestClient
from cgt_map_backend.app import create_app
from cgt_map_backend.db_models import Company, ECompanyCategory
from cgt_map_backend.companies_router import CreateCompanyRequest, CompanyResponse
import json
from mongoengine import disconnect


class TestConfig(TestCase):

    def setUp(self):
        d = {
            "mongo": {
                "type": "MOCK"
            }
        }
        self.config = CGTMapBackendConfig.parse_obj(d)
        self.app = create_app(self.config)
        self.client = TestClient(self.app)

    def tearDown(self):
        disconnect()

    def test_create_company(self):
        request_data = CreateCompanyRequest(
            name="Test Company",
            position={"type": "Point", "coordinates": [0, 0]},
            category=ECompanyCategory.Consulting,
            description="Test Description",
            website="https://www.test.com",
            logo="https://www.test.com/logo.png"
        )
        response = self.client.post("/company", json=json.loads(request_data.json()))
        self.assertEqual(200, response.status_code)
        response_data = CompanyResponse.parse_obj(response.json())
        self.assertEqual(request_data.name, response_data.name)
        self.assertEqual(request_data.position, response_data.position)
        self.assertEqual(request_data.category, response_data.category)
        self.assertEqual(request_data.description, response_data.description)
        self.assertEqual(request_data.website, response_data.website)
        self.assertEqual(request_data.logo, response_data.logo)

    def test_get_companies(self):
        test_company = Company(
            name="Test Company",
            position=[0, 0],
            category=ECompanyCategory.Consulting,
            description="Test Description",
            website="https://www.test.com/",
            logo="https://www.test.com/logo.png"
        ).save()
        response = self.client.get("/company")
        self.assertEqual(200, response.status_code)
        response_data = [CompanyResponse.parse_obj(company) for company in response.json()]
        self.assertEqual(1, len(response_data))
        self.assertEqual(test_company.name, response_data[0].name)
        self.assertEqual(tuple(test_company.position), response_data[0].position.coordinates)
        self.assertEqual(test_company.category, response_data[0].category)
        self.assertEqual(test_company.description, response_data[0].description)
        self.assertEqual(test_company.website, str(response_data[0].website))
        self.assertEqual(test_company.logo, str(response_data[0].logo))

    def test_delete_company(self):
        test_company = Company(
            name="Test Company",
            position=[0, 0],
            category=ECompanyCategory.Consulting,
            description="Test Description",
            website="https://www.test.com/",
            logo="https://www.test.com/logo.png"
        ).save()
        response = self.client.delete(f"/company/{test_company._id}")
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, Company.objects().count())