from app import create_app
from app.models import Customer, db
import unittest
from werkzeug.security import check_password_hash, generate_password_hash
from app.util.auth import encode_token


class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.customer = Customer(
            first_name="Firstname",
            last_name="Lastname",
            email="test@test.com",
            password=generate_password_hash("password"),
            phone="123-456-7890",
            address="123 Test St",
        )

        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.commit()

        self.token = encode_token(1, "admin")
        self.client = self.app.test_client()

    # create customer test
    def test_create_customer(self):
        customer_payload = {
            "first_name": "TestBob",
            "last_name": "TestBarker",
            "email": "bob@bob.com",
            "password": "bob",
            "phone": "555-555-5555",
            "address": "555 Bob St",
        }

        response = self.client.post(
            "/customer",
            json=customer_payload,
            headers={"Authorization": f"Bearer {self.token}"},
        )
        self.assertEqual(response.status_code, 201)
