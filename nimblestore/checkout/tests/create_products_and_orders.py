from decimal import Decimal
from random import randint, choice
from checkout.models import Product, Order, OrderProduct

# Crear productos básicos de supermercado
product_names = [
    "Pan", "Leche", "Huevos", "Arroz", "Frijoles", 
    "Azúcar", "Sal", "Aceite", "Cereal", "Jugo"
]

products = []

for name in product_names:
    product = Product.objects.create(
        name=name,
        price=Decimal(randint(10, 100)),  # Precio entre 10 y 100
        quantity=100,  # Cantidad fija
        state="Active"
    )
    products.append(product)

print("Productos creados con éxito!")

# Crear órdenes
for i in range(10):
    order = Order.objects.create()  # Crear una nueva orden
    num_products = randint(1, 5)  # Cada orden tiene entre 1 y 5 productos
    # Seleccionar productos aleatoriamente para la orden
    selected_products = [choice(products) for _ in range(num_products)]
    for product in selected_products:
        quantity = randint(1, 5)  # Cantidad entre 1 y 5 por producto
        # Validar si hay suficiente inventario
        if product.quantity >= quantity:
            # Reducir el inventario del producto
            product.quantity -= quantity
            product.save()
            # Añadir el producto a la orden
            OrderProduct.objects.create(
                order=order,
                product=product,
                quantity=quantity
            )
    # Recalcular y guardar el total de la orden
    order.total_cost = order.validate_and_calculate_total_cost()
    order.save()

print("Órdenes creadas con éxito!")
