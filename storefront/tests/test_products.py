# from rest_framework.test import APIClient
# from rest_framework import status
# import pytest

# @pytest.mark.django_db
# class TestCreateProduct:
#     def test_if_user_is_anonymous_return_401(self):
#         client = APIClient()
#         response = client.post('/store/products/', {"title" : "a", "price": 2, "collection" : 7})

#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
# test_app.py
import pytest

def add(a, b):
    return a + b

# Define a fixture
@pytest.fixture
def numbers():
    return (1, 2)

# Use the fixture in a test
def test_add(numbers):
    print(numbers)
    a, b = numbers
    result = add(a, b)
    assert result == 3
