from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, CustomerProfile, Order, OrderItem
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import urllib.parse
from django.urls import reverse



# =========================
# COMPTEUR PANIER
# =========================

def get_cart_count(request):

    cart = request.session.get(
        'cart',
        {}
    )

    return sum(cart.values())



# =========================
# ACCUEIL
# =========================

def home(request):

    query = request.GET.get('search')


    if query:

        products = Product.objects.filter(
            name__icontains=query
        )

    else:

        products = Product.objects.all()


    return render(
        request,
        'shop/home.html',
        {
            'products': products,
            'cart_count': get_cart_count(request)
        }
    )



# =========================
# DETAIL PRODUIT
# =========================

def product_detail(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )


    nom = product.name.lower()
    description = product.description.lower()


    if (
        "chaussure" in nom
        or "sneaker" in nom
        or "basket" in nom
        or "talon" in nom
        or "pointure" in description
    ):

        sizes = [
            "36","37","38","39","40",
            "41","42","43","44","45"
        ]


    elif product.category in [
        "Hommes",
        "Femmes"
    ]:

        sizes = [
            "S",
            "M",
            "L",
            "XL",
            "XXL"
        ]


    elif product.category == "Enfants":

        sizes = [
            "2 ans",
            "3 ans",
            "4 ans",
            "5 ans",
            "6 ans",
            "8 ans",
            "10 ans",
            "12 ans"
        ]


    else:

        sizes = [
            "Standard"
        ]



    return render(
        request,
        'shop/product_detail.html',
        {
            'product': product,
            'sizes': sizes,
            'cart_count': get_cart_count(request)
        }
    )



# =========================
# AJOUTER AU PANIER
# =========================

def add_to_cart(request, id):

    cart = request.session.get(
        'cart',
        {}
    )


    size = request.POST.get(
        'size',
        'Standard'
    )


    key = f"{id}_{size}"


    cart[key] = cart.get(
        key,
        0
    ) + 1


    request.session['cart'] = cart


    return redirect(
        'cart'
    )



# =========================
# DIMINUER QUANTITE
# =========================

def decrease_cart(request, key):

    cart = request.session.get(
        'cart',
        {}
    )


    if key in cart:

        if cart[key] > 1:

            cart[key] -= 1

        else:

            del cart[key]


    request.session['cart'] = cart


    return redirect(
        'cart'
    )



# =========================
# SUPPRIMER PANIER
# =========================

def remove_from_cart(request, key):

    cart = request.session.get(
        'cart',
        {}
    )


    if key in cart:

        del cart[key]


    request.session['cart'] = cart


    return redirect(
        'cart'
    )



# =========================
# PANIER
# =========================

def cart(request):

    cart = request.session.get(
        'cart',
        {}
    )


    cart_items = []

    total = 0



    for item_key, quantity in cart.items():


        if "_" in item_key:

            product_id, size = item_key.split(
                "_",
                1
            )

        else:

            product_id = item_key
            size = "Standard"



        product = get_object_or_404(
            Product,
            id=product_id
        )


        item_total = product.price * quantity


        total += item_total



        cart_items.append(
            {
                'product': product,
                'quantity': quantity,
                'size': size,
                'key': item_key,
                'item_total': item_total
            }
        )



    # =========================
    # MESSAGE WHATSAPP
    # =========================


    message = (
        "Bonjour Yamsu Chance Fashion 👋\n\n"
        "Je souhaite commander les articles suivants :\n\n"
    )



    for item in cart_items:


        message += (
            "🛍️ Article : "
            + item['product'].name
            + "\n"
            
            "📂 Catégorie : "
            + item['product'].category
            + "\n"
            
            "📏 Taille : "
            + item['size']
            + "\n"
            
            "🔢 Quantité : "
            + str(item['quantity'])
            + "\n"
            
            "💰 Prix unitaire : "
            + str(item['product'].price)
            + " FCFA\n"
            
            "💵 Sous-total : "
            + str(item['item_total'])
            + " FCFA\n\n"
            
            "----------------------\n\n"
        )



    message += (
        "💵 TOTAL : "
        + str(total)
        + " FCFA\n\n"
        
        "Merci 🙏"
    )



    print("MESSAGE WHATSAPP :")
    print(message)



    return render(
        request,
        'shop/cart.html',
        {
            'cart_items': cart_items,
            'total': total,
            'cart_count': get_cart_count(request),
            'whatsapp_message': urllib.parse.quote(message)
        }
    )
# =========================
# CATEGORIES
# =========================

def hommes(request):

    products = Product.objects.filter(
        category="Hommes"
    )

    return render(
        request,
        'shop/home.html',
        {
            'products': products,
            'cart_count': get_cart_count(request)
        }
    )



def femmes(request):

    products = Product.objects.filter(
        category="Femmes"
    )

    return render(
        request,
        'shop/home.html',
        {
            'products': products,
            'cart_count': get_cart_count(request)
        }
    )



def enfants(request):

    products = Product.objects.filter(
        category="Enfants"
    )

    return render(
        request,
        'shop/home.html',
        {
            'products': products,
            'cart_count': get_cart_count(request)
        }
    )



def electromenager(request):

    products = Product.objects.filter(
        category="Électroménager"
    )

    return render(
        request,
        'shop/home.html',
        {
            'products': products,
            'cart_count': get_cart_count(request)
        }
    )



def autres(request):

    products = Product.objects.exclude(
        category__in=[
            "Hommes",
            "Femmes",
            "Enfants",
            "Électroménager"
        ]
    )

    return render(
        request,
        'shop/home.html',
        {
            'products': products,
            'cart_count': get_cart_count(request)
        }
    )





# =========================
# CHECKOUT
# =========================

def checkout(request):

    cart = request.session.get(
        'cart',
        {}
    )


    total = 0

    products_in_cart = []


    for item_key, quantity in cart.items():


        if "_" in item_key:

            product_id, size = item_key.split(
                "_",
                1
            )

        else:

            product_id = item_key
            size = "Standard"



        product = get_object_or_404(
            Product,
            id=product_id
        )



        item_total = product.price * quantity


        total += item_total



        products_in_cart.append(
            {
                'product': product,
                'quantity': quantity,
                'size': size,
                'item_total': item_total
            }
        )




    if request.method == "POST":


        order = Order.objects.create(

            user=request.user,

            full_name=request.POST.get(
                'full_name'
            ),

            phone=request.POST.get(
                'phone'
            ),

            address=request.POST.get(
                'address'
            ),

            total=total

        )




        for item in products_in_cart:


            OrderItem.objects.create(

                order=order,

                product=item['product'],

                quantity=item['quantity'],

                price=item['product'].price,

                size=item['size']

            )





        # =========================
        # MESSAGE WHATSAPP COMPLET
        # =========================


        message = f"""
🛒 NOUVELLE COMMANDE

🏪 Yamsu Chance Fashion


👤 Client :
{order.full_name}


📞 Téléphone :
{order.phone}


📍 Adresse :
{order.address}



📦 PRODUITS COMMANDÉS :
"""



        for item in products_in_cart:


            message += f"""

🛍️ Article :
{item['product'].name}


📂 Catégorie :
{item['product'].category}


📏 Taille :
{item['size']}


🔢 Quantité :
{item['quantity']}


💰 Prix unitaire :
{item['product'].price} FCFA


💵 Sous-total :
{item['item_total']} FCFA


-------------------------
"""



        message += f"""

💵 TOTAL COMMANDE :
{order.total} FCFA


🙏 Merci pour votre confiance.
"""



        whatsapp_url = (

            "https://wa.me/2349165391998"

            "?text="

            + urllib.parse.quote(message)

        )



        # vider le panier après commande

        request.session['cart'] = {}




        return render(

            request,

            'shop/order_success.html',

            {

                'order': order,

                'whatsapp_url': whatsapp_url

            }

        )






    return render(

        request,

        'shop/checkout.html',

        {

            'total': total,

            'products_in_cart': products_in_cart

        }

    )





# =========================
# INSCRIPTION
# =========================

def register(request):

    if request.method == "POST":

        username = request.POST.get(
            'username'
        )

        password = request.POST.get(
            'password'
        )


        user = User.objects.create_user(
            username=username,
            password=password
        )


        CustomerProfile.objects.create(
            user=user
        )


        login(
            request,
            user
        )


        return redirect(
            'home'
        )



    return render(
        request,
        'shop/register.html'
    )





# =========================
# CONNEXION
# =========================

def login_user(request):

    if request.method == "POST":


        user = authenticate(

            request,

            username=request.POST.get(
                'username'
            ),

            password=request.POST.get(
                'password'
            )

        )


        if user:

            login(
                request,
                user
            )


            return redirect(
                'home'
            )



    return render(
        request,
        'shop/login.html'
    )





# =========================
# DECONNEXION
# =========================

def logout_user(request):

    logout(request)


    return redirect(
        'home'
    )





# =========================
# PROFIL CLIENT
# =========================

def profile(request):

    profile, created = CustomerProfile.objects.get_or_create(
        user=request.user
    )


    orders = Order.objects.filter(
        user=request.user
    ).order_by(
        '-created_at'
    )


    return render(
        request,
        'shop/profile.html',
        {
            'profile': profile,
            'orders': orders
        }
    )





# =========================
# MODIFIER PROFIL
# =========================

def edit_profile(request):

    profile, created = CustomerProfile.objects.get_or_create(
        user=request.user
    )


    if request.method == "POST":

        profile.phone = request.POST.get(
            'phone'
        )

        profile.address = request.POST.get(
            'address'
        )


        profile.save()


        return redirect(
            'profile'
        )


    return render(
        request,
        'shop/edit_profile.html',
        {
            'profile': profile
        }
    )





# =========================
# PDF COMMANDE
# =========================

def download_order_pdf(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )


    response = HttpResponse(
        content_type="application/pdf"
    )


    response["Content-Disposition"] = (
        f'attachment; filename="commande_{order.id}.pdf"'
    )


    pdf = canvas.Canvas(
        response,
        pagesize=A4
    )


    width, height = A4


    # TITRE
    pdf.setFont(
        "Helvetica-Bold",
        20
    )

    pdf.drawString(
        50,
        height - 50,
        "Yamsu Chance Fashion"
    )


    pdf.setFont(
        "Helvetica",
        12
    )


    y = height - 90


    pdf.drawString(
        50,
        y,
        f"Commande N° {order.id}"
    )

    y -= 25


    pdf.drawString(
        50,
        y,
        f"Client : {order.full_name}"
    )

    y -= 20


    pdf.drawString(
        50,
        y,
        f"Téléphone : {order.phone}"
    )

    y -= 20


    pdf.drawString(
        50,
        y,
        f"Adresse : {order.address}"
    )


    y -= 40


    pdf.setFont(
        "Helvetica-Bold",
        13
    )


    pdf.drawString(
        50,
        y,
        "Produits :"
    )


    y -= 25


    pdf.setFont(
        "Helvetica",
        11
    )


    for item in order.items.all():

        texte = (
            f"{item.product.name} - "
            f"Taille: {item.size} - "
            f"Qté: {item.quantity} - "
            f"{item.price} FCFA"
        )


        pdf.drawString(
            50,
            y,
            texte
        )


        y -= 20



    y -= 20


    pdf.setFont(
        "Helvetica-Bold",
        14
    )


    pdf.drawString(
        50,
        y,
        f"TOTAL : {order.total} FCFA"
    )


    pdf.save()


    return response