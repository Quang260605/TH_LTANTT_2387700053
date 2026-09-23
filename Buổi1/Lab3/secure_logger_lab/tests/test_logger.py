import os
import json
import unittest
from app import app
from securelogger import get_secure_logger
from securelogger.logger import mask_pii, hash_line, LOG_FILE, SIGNATURE_FILE

class TestSecureLogger(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_mask_pii_email(self):
        text = "Contact me at user@example.com for info"
        masked = mask_pii(text)
        self.assertNotIn("user@example.com", masked)
        self.assertIn("<email_masked>", masked)

    def test_mask_pii_token(self):
        text = "Authorization token='secret123456'"
        masked = mask_pii(text)
        self.assertNotIn("secret123456", masked)
        self.assertIn("<token_masked>", masked)

    def test_validate_api_endpoint(self):
        payload = {
            "email": "phuoc@example.com",
            "url": "https://secure.com",
            "filename": "report.pdf",
            "sql": "' OR 1=1 --",
            "html": "<script>alert(1)</script>"
        }
        response = self.app.post('/validate', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data["email"])
        self.assertTrue(data["url"])
        self.assertTrue(data["filename"])
        self.assertEqual(data["sql"], "1=1")
        self.assertEqual(data["html"], "&lt;script&gt;alert(1)&lt;/script&gt;")

        # Verify log file and signature file were written
        self.assertTrue(os.path.exists(LOG_FILE))
        self.assertTrue(os.path.exists(SIGNATURE_FILE))

        with open(LOG_FILE, "r", encoding="utf-8") as f:
            logs = f.readlines()
            last_log = json.loads(logs[-1])
            self.assertIn("<email_masked>", str(last_log))

if __name__ == "__main__":
    unittest.main()
