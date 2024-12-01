from django.http.response import JsonResponse
from django.views import generic
from rest_framework import viewsets,status
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from .models import Product, Order, OrderProduct
from .serializers import ProductSerializer,OrderSerializer,OrderProductSerializer
from django.shortcuts import get_object_or_404
from decimal import Decimal
from rest_framework.response import Response
from django.db import transaction

class IndexView(generic.TemplateView):
    template_name = "index.html"


class ProductListView(viewsets.ModelViewSet):
    """
    API endpoint to list products filtered by active state.

    This view provides an API for listing all products that are in an active state. 
    Each product in the response includes its name, price, and available quantity.

    Attributes:
        queryset (QuerySet): The queryset to retrieve products from the database.
        serializer_class (ProductSerializer): The serializer to convert product instances to JSON format.
    """
    queryset = Product.objects.filter(state='Active')
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        """Override get_queryset to add filtering by active state and optional name filter.

        Filters products based on the active state and an optional name parameter.
        
        Returns:
            QuerySet: A queryset of products filtered by active state and name (if provided).
        """
        name = self.request.query_params.get('name', None)
        
        if name:
            queryset = self.queryset.filter(name__icontains=name)
            return queryset
        
        return self.queryset


class OrderView(APIView):
    parser_classes = (JSONParser,)
    authentication_classes = []

    def post(self, request):
        """
        API endpoint to create an order with products and calculate the total cost.

        This view processes a list of products and quantities, checks product availability 
        in the inventory, and creates an order if the products are available. It also 
        calculates the total cost of the order.

        Args:
            request (Request): The HTTP request object containing the products and quantities.

        Returns:
            Response: A JSON response containing either the details of the order or an error message.
        """

        # Get the products and quantities from the request body
        order_data = request.data
        products = order_data

        # Check if products are provided
        if not products:
            return Response(
                {"detail": "At least one product must be included in the order."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verify product availability and quantity before creating the order
        valid_products = []
        for item in products:
            product_name = item.get("product")
            quantity = float(item.get("quantity"))

            # Validation for required fields
            if not product_name or not quantity:
                return Response(
                    {
                        "detail": "Product name and quantity are required.",
                        "total": 0
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                # Find the product in the active inventory
                product = Product.objects.get(name=product_name, state='Active')
            except Product.DoesNotExist:
                return Response(
                    {
                        "detail": f"Product '{product_name}' not found or is inactive.",
                        "total": 0
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            print(product,product.quantity,quantity)
            # Check if there is enough inventory
            if product.quantity < quantity:
                product.refresh_from_db()
                print('pre validacion')
                return Response(
                    {
                        "detail": f"Not enough inventory for product '{product_name}'. Requested: {quantity}, Available: {product.quantity}.",
                        "total": 0
                     },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # If the product is valid, add it to the list of valid products
            valid_products.append((product, quantity))

        # Now that all products are valid, create the order
        try:
            with transaction.atomic():
                # Initially create the empty order
                order = Order.objects.create()

                # Add valid products to the order and update inventory
                for product, quantity in valid_products:
                    # Verify the product again within the transaction
                    product.refresh_from_db()  # Obtener los datos actualizados de la base de datos

                    # Re-check inventory as it may have been modified in other operations
                    if product.quantity < quantity:
                        print('post validacion')
                        return Response(
                            {
                                "detail": f"Not enough inventory for product '{product.name}'. Requested: {quantity}, Available: {product.quantity}.",
                                "total": 0
                            },
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    # Deduct the product quantity from the database
                    product.quantity -= quantity
                    product.save()

                    # Add the product to the order
                    OrderProduct.objects.create(order=order, product=product, quantity=quantity)

                
                # Refresh the products after the transaction has been confirmed
                for product, quantity in valid_products:
                    product.refresh_from_db()  

                # Recalculate the total after adding the products
                order.total_cost = order.validate_and_calculate_total_cost()
                order.save()

                # Return the response with order details
                return Response(
                    {"order_id": order.id, "total": str(order.total_cost)},
                    status=status.HTTP_201_CREATED,
                )

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            # If any error occurs, rollback the transaction
            return Response(
                {
                    "detail": f"An error occurred: {str(e)}",
                    "total": 0
                    },
                status=status.HTTP_400_BAD_REQUEST
            )