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

        self.customer_payload = {
            "first_name": "TestBob",
            "last_name": "TestBarker",
            "email": "bob@bob.com",
            "password": "bob",
            "phone": "555-555-5555",
            "address": "555 Bob St",
        }

        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.commit()

        self.token = encode_token(1, "admin")
        self.client = self.app.test_client()

    # def tearDown(self):
    #     with self.app.app_context():
    #         db.session.remove()
    #         db.drop_all()
    #         db.engine.dispose()
    # db.session.close()

    # create customer test
    def test_create_customer(self):
        response = self.client.post(
            "/customer",
            json=self.customer_payload,
            headers={"Authorization": f"Bearer {self.token}"},
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["first_name"], "TestBob")
        self.assertEqual(response.json["last_name"], "TestBarker")
        self.assertIn("id", response.json)
        self.assertEqual(response.json["password"], "********")

    def test_create_customer_no_token(self):
        response = self.client.post(
            "/customer",
            json=self.customer_payload,
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json["error"], "token missing from authorization headers"
        )
        self.assertNotIn("id", response.json)

    def test_create_customer_invalid_token(self):
        customer_token = encode_token(1, "user")

        response = self.client.post(
            "/customer",
            json=self.customer_payload,
            headers={"Authorization": f"Bearer {customer_token}"},
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json["message"], "admin access required")
        self.assertNotIn("id", response.json)
        self.assertNotIn("first_name", response.json)

    def test_customer_login(self):
        payload = {"email": "test@test.com", "password": "password"}
        response = self.client.post("/customer/login", json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json)
        self.assertEqual(response.json["message"], "Welcome Firstname")
        self.assertIsInstance(response.json["token"], str)

    def test_update_customer(self):
        payload = {
            "phone": "999-999-9999",
            "first_name": "billy",
            "password": "newpassword",
        }

        response = self.client.put(
            "customer",
            json=payload,
            headers={"Authorization": f"Bearer {self.token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["phone"], "999-999-9999")
        self.assertEqual(response.json["first_name"], "billy")
        self.assertEqual(response.json["password"], "********")
        self.assertIn("phone", response.json)
        self.assertIn("id", response.json)
