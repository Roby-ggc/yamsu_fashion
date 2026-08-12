from django.urls import path
from . import views


urlpatterns = [

    # =========================
    # ACCUEIL
    # =========================

    path(
        '',
        views.home,
        name='home'
    ),



    # =========================
    # PRODUITS
    # =========================

    path(
        'product/<int:id>/',
        views.product_detail,
        name='product_detail'
    ),



    # =========================
    # CATEGORIES
    # =========================

    path(
        'hommes/',
        views.hommes,
        name='hommes'
    ),


    path(
        'femmes/',
        views.femmes,
        name='femmes'
    ),


    path(
        'enfants/',
        views.enfants,
        name='enfants'
    ),


    path(
        'electromenager/',
        views.electromenager,
        name='electromenager'
    ),


    path(
        'autres/',
        views.autres,
        name='autres'
    ),





    # =========================
    # PANIER
    # =========================

    path(
        'cart/',
        views.cart,
        name='cart'
    ),


    path(
        'add-cart/<int:id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),


    path(
        'decrease-cart/<str:key>/',
        views.decrease_cart,
        name='decrease_cart'
    ),


    path(
        'remove-cart/<str:key>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),





    # =========================
    # COMMANDE
    # =========================

    path(
        'checkout/',
        views.checkout,
        name='checkout'
    ),


    path(
        'order-pdf/<int:order_id>/',
        views.download_order_pdf,
        name='download_order_pdf'
    ),





    # =========================
    # COMPTE CLIENT
    # =========================

    path(
        'register/',
        views.register,
        name='register'
    ),


    path(
        'login/',
        views.login_user,
        name='login'
    ),


    path(
        'logout/',
        views.logout_user,
        name='logout'
    ),





    # =========================
    # PROFIL
    # =========================

    path(
        'profile/',
        views.profile,
        name='profile'
    ),


    path(
        'edit-profile/',
        views.edit_profile,
        name='edit_profile'
    ),

]