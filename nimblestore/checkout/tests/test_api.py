import os

import django
import pytest

# from checkout.models import Product
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from checkout.models import Product, Order, OrderProduct
from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nimblestore.settings")
django.setup()


@pytest.fixture
def api_client():
    return APIClient()



@pytest.fixture
def create_product():
    """Fixture to create a product."""
    def _create_product(name, price, quantity, state='Active'):
        return Product.objects.create(name=name, price=price, quantity=quantity, state=state)
    return _create_product


def dummy_test():
    assert 1 == 1


def dummy_failing():
    assert 1 == 2


@pytest.mark.django_db
def test_get_products(api_client, create_product):
    create_product(name="Test Product 1", price=10.00, quantity=100)
    create_product(name="Test Product 2", price=15.00, quantity=200)

    url = reverse("products")  # Adjust this to your actual URL name
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2



@pytest.mark.django_db
def test_post_order(api_client, create_product):
    # Create test products
    product1 = create_product(name="Test Product 1", price=10.00, quantity=100)
    product2 = create_product(name="Test Product 2", price=15.00, quantity=200)

    # Prepare data for the order
    order_data = [
        {"product": product1.name, "quantity": 2},
        {"product": product2.name, "quantity": 3}
    ]

    # Make POST request to create the order
    url = reverse("order")  # Adjust this to your actual URL name
    response = api_client.post(url, data=order_data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert 'order_id' in response.data
    assert 'total' in response.data

    # Verify that the total cost is correctly calculated
    total_cost = 2 * product1.price + 3 * product2.price
    assert Decimal(response.data['total']) == total_cost

    # Check that the products' quantities have been updated
    product1.refresh_from_db()
    product2.refresh_from_db()
    assert product1.quantity == 98  # 100 - 2
    assert product2.quantity == 197  # 200 - 3
