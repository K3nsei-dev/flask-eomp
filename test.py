import unittest
from app import app


# api route connection class for testing
class ApiRoutes(unittest.TestCase):

    def test_registration(self):  # testing registration connection
        test_reg = app.test_client()
        response = test_reg.get('/register')
        status = response.status_code
        self.assertEqual(status, 405)

    def test_user(self):  # testing get user connection
        test_user = app.test_client()
        response = test_user.get('/user-profile/<int:user_id>')
        status = response.status_code
        self.assertEqual(status, 404)

    def test_update(self):  # testing update product connection
        test_update = app.test_client()
        response = test_update.get('/update-products/<int:product_id>')
        status = response.status_code
        self.assertEqual(status, 404)

    def test_add(self):  # testing add product connection
        test_add = app.test_client()
        response = test_add.get('/add-products')
        status = response.status_code
        self.assertEqual(status, 405)

    def test_view(self):  # testing view product connection
        test_view = app.test_client()
        response = test_view.get('/view-products')
        status = response.status_code
        self.assertEqual(status, 308)

    def test_delete(self):  # testing delete product connection
        test_del = app.test_client()
        response = test_del.get('/delete-product/<int:product_id>')
        status = response.status_code
        self.assertEqual(status, 404)
