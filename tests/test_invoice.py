from app import create_app
from app.models import Invoice, Tech, Customer, db
import unittest
from werkzeug.security import check_password_hash, generate_password_hash
from app.util.auth import encode_token
from datetime import date


class TestInvoice(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.invoice = Invoice(
            date=date(2025, 12, 7),
            status="Test status",
            total_cost=float(100.00),
            vehicle="Test Vehicle",
            customer_id=int(1),
        )

        # self.customer = Customer(
        #     first_name="Firstname",
        #     last_name="Lastname",
        #     email="test@test.com",
        #     password=generate_password_hash("password"),
        #     phone="123-456-7890",
        #     address="123 Test St",
        # )
        # self.tech = Tech(
        #     first_name="Firstname",
        #     last_name="Lastname",
        #     password=generate_password_hash("password"),
        #     phone="123-456-7890",
        #     position="tech",
        # )

        self.invoice_payload = {
            "date": date(2025, 12, 8),
            "status": "Brake Job: In progress.",
            "total_cost": float(250.00),
            "vehicle": "1999 Ford Exploder",
            "customer_id": int(1),
            # "customer_id": self.customer.id,
        }

        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.invoice)
            # db.session.add(self.customer)
            # db.session.add(self.tech)
            db.session.commit()

        self.admin_token = encode_token(1, "admin")
        self.tech_token = encode_token(1, "tech")
        self.client = self.app.test_client()

    # def tearDown(self):
    #     with self.app.app_context():
    #         db.session.remove()
    #         db.drop_all()
    #         db.engine.dispose()
    # db.session.close()

    # def test_get_invoices_admin_token(self):

    def test_get_invoice_admin_token(self):
        response = self.client.get(
            "/invoice/1",
            headers={"Authorization": f"Bearer {self.admin_token}"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "Test status")
        self.assertEqual(response.json["total_cost"], 100.0)
        self.assertEqual(response.json["vehicle"], "Test Vehicle")
        self.assertEqual(response.json["customer_id"], 1)
        self.assertIn("id", response.json)

    def test_get_invoice_tech_token(self):
        response = self.client.get(
            # f"/invoice/{self.invoice.id}",
            "/invoice/1",
            headers={"Authorization": f"Bearer {self.tech_token}"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "Test status")
        self.assertEqual(response.json["total_cost"], 100.0)
        self.assertEqual(response.json["vehicle"], "Test Vehicle")
        self.assertEqual(response.json["customer_id"], 1)
        self.assertIn("id", response.json)

    def test_get_invoice_no_token(self):
        response = self.client.get(
            "/invoice/1",
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json["error"], "token missing from authorization headers"
        )

    # def test_create_invoice_admin_token(self):
    #     response = self.client.post(
    #         "/invoice",
    #         json=self.invoice_payload,
    #         headers={"Authorization": f"Bearer {self.admin_token}"},
    #     )
    #
    #     self.assertEqual(response.status_code, 201)
    #     self.assertEqual(response.json["status"], "Brake Job: In progress.")
    #     self.assertEqual(response.json["total_cost"], 250.0)
    #     self.assertEqual(response.json["vehicle"], "1999 Ford Exploder")
    #     self.assertIn("id", response.json)
