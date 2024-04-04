import unittest
from app import app, db
from app.models import Client, Item

class TestApp(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.client = app.test_client()
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_add_client(self):
        response = self.client.post('/client', json={'name': 'Test'})
        self.assertEqual(response.status_code, 200)

    def test_get_client(self):
        client = Client(name='Test')
        db.session.add(client)
        db.session.commit()

        response = self.client.get('/client/1')
        self.assertEqual(response.status_code, 200)

    def test_add_item(self):
        client = Client(name='Test')
        db.session.add(client)
        db.session.commit()

        response = self.client.post('/item', json={'name': 'Test Item', 'client_id': 1})
        self.assertEqual(response.status_code, 200)

    def test_get_item(self):
        client = Client(name='Test')
        db.session.add(client)

        item = Item(name='Test Item', client_id=1)
        db.session.add(item)
        db.session.commit()

        response = self.client.get('/item/1')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()