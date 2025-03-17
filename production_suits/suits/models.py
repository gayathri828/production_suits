from django.db import models
from django.contrib.auth.models import User


# Model to store customer information
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile',default=1)  # Replace 1 with a valid user ID
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


# Model to store the customization preferences of a suit order
class SuitCustomization(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customizations')
    fireproof = models.BooleanField(default=False)
    waterproof = models.BooleanField(default=False)
    gas_resistance = models.BooleanField(default=False)
    chemical_resistance = models.BooleanField(default=False)
    germ_resistance = models.BooleanField(default=False)
    bulletproof = models.BooleanField(default=False)

    suit_name = models.CharField(max_length=15, blank=True, null=True)  # The predicted suit name

    def __str__(self):
        return f'{self.suit_name} for {self.customer.first_name}'

    def calculate_price(self):
        base_price = 100  # Example base price

        # Add features cost
        if self.fireproof:
            base_price += 50
        if self.waterproof:
            base_price += 40
        if self.gas_resistance:
            base_price += 60
        if self.chemical_resistance:
            base_price += 70
        if self.germ_resistance:
            base_price += 30
        if self.bulletproof:
            base_price += 100

        return base_price


# Model to store the order details
class SuitOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    suit_customization = models.ForeignKey(SuitCustomization, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Example: Store the total price
    order_status = models.CharField(max_length=10, default='Pending')  # Status could be 'Pending', 'In Progress', 'Shipped', etc.

    def __str__(self):
        return f'Order {self.id} for {self.customer.first_name}'


# Model to store product details for the suits
class Suit(models.Model):
    name = models.CharField(max_length=10)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
