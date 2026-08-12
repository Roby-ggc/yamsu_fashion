from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



from django.db import models


class Product(models.Model):

    name = models.CharField(
        max_length=200
    )


    category = models.CharField(
        max_length=100
    )


    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )


    description = models.TextField()


    image = models.ImageField(
        upload_to='products/'
    )


    # Exemple :
    # Chaussures : 40,41,42,43,44,45
    # Vêtements : S,M,L,XL,XXL
    # Enfants : 2 ans,3 ans,4 ans
    sizes = models.CharField(
        max_length=200,
        blank=True,
        help_text="Séparer les tailles par des virgules. Exemple: S,M,L,XL ou 40,41,42"
    )


    stock = models.PositiveIntegerField(
        default=0
    )


    available = models.BooleanField(
        default=True
    )


    def get_sizes_list(self):
        if self.sizes:
            return [size.strip() for size in self.sizes.split(",")]
        return []


    def __str__(self):

        return self.name





class CustomerProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )


    phone = models.CharField(
        max_length=20,
        blank=True
    )


    address = models.TextField(
        blank=True
    )


    def __str__(self):

        return self.user.username





@receiver(post_save, sender=User)
def create_customer_profile(sender, instance, created, **kwargs):

    if created:

        CustomerProfile.objects.create(
            user=instance
        )





class Order(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )


    full_name = models.CharField(
        max_length=100
    )


    phone = models.CharField(
        max_length=30
    )


    address = models.TextField()
    

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )


    STATUS_CHOICES = [

        ('En attente', 'En attente'),

        ('Confirmée', 'Confirmée'),

        ('En préparation', 'En préparation'),

        ('Livrée', 'Livrée'),

    ]


    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='En attente'
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):

        return f"Commande de {self.user.username}"





class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )


    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )


    quantity = models.PositiveIntegerField(
        default=1
    )


    size = models.CharField(
        max_length=50,
        blank=True
    )


    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )


    def __str__(self):

        return f"{self.product.name} x {self.quantity}"