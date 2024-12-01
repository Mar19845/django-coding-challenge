from django.db import models
from django.utils.timezone import now
from decimal import Decimal

# Create your models here.
class Product(models.Model):
    """Represents a product in the inventory.

    Attributes:
        name (str): The name of the product (max 100 characters).
        price (Decimal): The price of the product. Defaults to 0.00.
        quantity (int): The quantity of the product in stock. Defaults to 0.
        state (str): The state of the product, either 'Active' or 'Inactive'. Defaults to 'Active'.
    """
    # Add properties name, price and quantity
    STATE_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    
    name = models.CharField(max_length=100,default='')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity = models.PositiveIntegerField(default=0)
    state = models.CharField(max_length=8, choices=STATE_CHOICES, default='Active')
    def __str__(self):
        """Returns a string representation of the product.

        Returns:
            str: The name of the product.
        """
        return self.name


class Order(models.Model):
    """Represents an order containing multiple products.

    Attributes:
        products (ManyToManyField): A relationship with the Product model.
        total_cost (Decimal): The total cost of the order, calculated dynamically.
        state (str): The current state of the order: 'Created', 'Paid', or 'Delivered'.
        created_at (datetime): The timestamp when the order was created.
        paid_at (datetime): The timestamp when the order was paid.
        delivered_at (datetime): The timestamp when the order was delivered.
    """
    STATE_CHOICES = [
        ('Created', 'Created'),
        ('Paid', 'Paid'),
        ('Delivered', 'Delivered'),
    ]

    products = models.ManyToManyField('Product', through='OrderProduct')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default='Created')
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    def validate_and_calculate_total_cost(self):
        """
        Validates if the order can be created and calculates its total cost.
        Raises:
            ValueError: If there is insufficient inventory for any product.
        Returns:
            Decimal: The total cost of the order.
        """
        total = Decimal('0.00')
        for order_product in self.orderproduct_set.all():
            product = order_product.product
            if product.quantity < order_product.quantity:
                raise ValueError(f"Not enough inventory for product '{product.name}'. Requested: {order_product.quantity}, Available: {product.quantity}.")
            total += product.price * order_product.quantity
        return total
    
    def save(self, *args, **kwargs):
        """
        Overrides the save method to validate and calculate total cost before saving.
        """
        if self.pk is None and not self.total_cost:  # Allow order creation without total cost
            self.total_cost = Decimal('0.00')  # Initialize with a default value
        super().save(*args, **kwargs)

    def add_product(self, product, quantity):
        """
        Adds a product to the order and recalculates the total cost.
        """
        # Check if there is enough stock for the product
        if product.quantity < quantity:
            raise ValueError(f"Not enough inventory for product '{product.name}'. Requested: {quantity}, Available: {product.quantity}.")
        
        # Add the product to the order
        OrderProduct.objects.create(order=self, product=product, quantity=quantity)

        # Recalculate the total cost after adding the product
        self.total_cost = self.validate_and_calculate_total_cost()
        self.save()
    
class OrderProduct(models.Model):
    """Intermediate model to represent products in an order with quantities.

    Attributes:
        order (ForeignKey): The order to which the product belongs.
        product (ForeignKey): The product included in the order.
        quantity (int): The quantity of the product in the order.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        """Returns a string representation of the OrderProduct.

        Returns:
            str: A string showing the product name, order ID, and quantity.
        """
        return f"{self.product.name} (Order #{self.order.id}) - Quantity: {self.quantity}"