from app import create_app
from app.models import Tech, db
import unittest
from werkzeug.security import check_password_hash, generate_password_hash
from app.util.auth import encode_token


class TestTech(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.tech = Tech(
            first_name="Firstname",
            last_name="Lastname",
            password=generate_password_hash("password"),
            phone="123-456-7890",
            position="tech",
        )

        self.tech_payload = {
            "first_name": "TestBob",
            "last_name": "TestBarker",
            "password": "bob",
            "phone": "555-555-5555",
            "position": "tech",
        }

        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.tech)
            db.session.commit()

        self.token = encode_token(1, "tech")
        self.client = self.app.test_client()

    # def tearDown(self):
    #     with self.app.app_context():
    #         db.session.remove()
    #         db.drop_all()
    #         db.engine.dispose()
    # db.session.close()
    #
    def test_tech_login(self):
        payload = {"last_name": "Lastname", "password": "password"}
        response = self.client.post("/tech/login", json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json)
        self.assertEqual(response.json["message"], "Welcome Firstname")
        self.assertIsInstance(response.json["token"], str)

    def test_create_tech(self):
        admin_token = encode_token(1, "admin")
        response = self.client.post(
            "/tech",
            json=self.tech_payload,
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["first_name"], "TestBob")
        self.assertEqual(response.json["last_name"], "TestBarker")
        self.assertEqual(response.json["phone"], "555-555-5555")
        self.assertIn("id", response.json)
        self.assertIn("password", response.json)
        self.assertEqual(response.json["password"], "********")

    def test_update_tech(self):
        payload = {
            "phone": "999-999-9999",
            "first_name": "billy",
            "password": "newpassword",
        }

        response = self.client.put(
            "tech", json=payload, headers={"Authorization": f"Bearer {self.token}"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["phone"], "999-999-9999")
        self.assertEqual(response.json["first_name"], "billy")
        self.assertIn("phone", response.json)
        self.assertIn("password", response.json)
        self.assertEqual(response.json["password"], "********")
        self.assertIn("id", response.json)

    def test_get_tech_by_id(self):
        response = self.client.get(
            "/tech/1", headers={"Authorization": f"Bearer {self.token}"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["first_name"], "Firstname")
        self.assertEqual(response.json["last_name"], "Lastname")
        self.assertIn("id", response.json)
        self.assertNotIn("password", response.json)

    def test_get_tech_by_id_no_token(self):
        response = self.client.get(
            "/tech/1",
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json["error"], "token missing from authorization headers"
        )
