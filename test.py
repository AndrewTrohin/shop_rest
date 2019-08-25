import unittest
import json
from rest_api import app
import time
import timeit

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config["DEBUG"] = True
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()

    def post(self, data):
        resp = self.client.post(path='/imports', data=json.dumps(data), content_type='application/json')
        return resp

    def test_posting_not_valid_data(self):
        import json
        count = 800
        citizens = []
        for i in range(1, count + 1):
            next = {
                "citizen_id": i,
                "town": "Moscow",
                "street": "Putin",
                "building": "1",
                "apartment": 777,
                "name": "Putin " + str(i),
                "birth_date": "07.05.1952",
                "gender": "male",
                "relatives": [j for j in range(1, count + 1) if j != i]
            }
            citizens.append(next)
        for i in range(1200+1, 10000+1):
            next = {
                "citizen_id": i,
                "town": "Moscow",
                "street": "Putin",
                "building": "1",
                "apartment": 777,
                "name": "Putin " + str(i),
                "birth_date": "07.05.1952",
                "gender": "male",
                "relatives": []
            }
            citizens.append(next)

        md = {"citizens": citizens}
        start_time = timeit.default_timer()
        resp = self.post(md)
        print(timeit.default_timer() - start_time)
        self.assertEqual(resp.status_code, 201)

    # def test_get(self):
    #     resp = self.client.get(path='/imports/41/citizens', content_type='application/json')
    #     #self.assertEqual(resp.status_code, 200)
    #     if not resp:
    #         print('There is no resp')
    #     print(type(resp))
    #     print(resp.json)
    #     #self.assertEqual(response.status_code, 200)
    # def tearDown(self):
    #     self.app_context.pop()


if __name__ == "__main__":
    unittest.main()