from rest_framework import serializers
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    """Serializer for the Product model.

    Converts Product model instances into JSON format and validates input data
    for creating or updating Product instances.

    Attributes:
        Meta (class): Defines the model to be serialized and the fields to include.
    """
    class Meta:
        """Meta class for ProductSerializer.

        Attributes:
            model (Product): The model to be serialized.
            fields (list): The list of fields to include in the serialized output.
        """
        model = Product
        fields = ['name', 'price', 'quantity']
        

class OrderProductSerializer(serializers.ModelSerializer):
    """Serializer for OrderProduct model.

    This serializer converts OrderProduct model instances to and from JSON.

    Attributes:
        order (int): The ID of the order the product belongs to.
        product (ProductSerializer): The details of the product.
        quantity (int): The quantity of the product in the order.
    """

    product = ProductSerializer(read_only=True)

    class Meta:
        """Meta class for OrderProductSerializer.

        Attributes:
            model (OrderProduct): The model to be serialized.
            fields (list): The list of fields to include in the serialized output.
        """
        model = OrderProduct
        fields = ['order', 'product', 'quantity']
    
    
class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order model.

    This serializer converts Order model instances to and from JSON, and
    validates if an order can be created based on product availability.

    Attributes:
        id (int): The unique identifier for the order.
        total_cost (Decimal): The total cost of the order.
        state (str): The state of the order, either 'Created', 'Paid', or 'Delivered'.
        created_at (datetime): The timestamp when the order was created.
        paid_at (datetime): The timestamp when the order was paid.
        delivered_at (datetime): The timestamp when the order was delivered.
        products (list[OrderProductSerializer]): The products included in the order, with quantities.
    """

    products = OrderProductSerializer(many=True)
    total_cost = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'total_cost', 'state', 'created_at', 'paid_at', 'delivered_at', 'products']
