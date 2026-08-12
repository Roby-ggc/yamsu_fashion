from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.conf import settings
import os


def generate_order_pdf(order):

    folder = os.path.join(
        settings.MEDIA_ROOT,
        "orders"
    )

    os.makedirs(
        folder,
        exist_ok=True
    )


    filename = f"commande_{order.id}.pdf"


    filepath = os.path.join(
        folder,
        filename
    )


    pdf = canvas.Canvas(
        filepath,
        pagesize=A4
    )


    width, height = A4


    y = height - 50


    pdf.setFont(
        "Helvetica-Bold",
        18
    )


    pdf.drawString(
        50,
        y,
        "Yamsu Chance Fashion"
    )


    y -= 40


    pdf.setFont(
        "Helvetica",
        12
    )


    pdf.drawString(
        50,
        y,
        f"Commande #{order.id}"
    )


    y -= 25

    pdf.drawString(
        50,
        y,
        f"Client : {order.full_name}"
    )


    y -= 25

    pdf.drawString(
        50,
        y,
        f"Telephone : {order.phone}"
    )


    y -= 25

    pdf.drawString(
        50,
        y,
        f"Adresse : {order.address}"
    )


    y -= 40


    pdf.drawString(
        50,
        y,
        "Produits :"
    )


    y -= 25


    for item in order.items.all():

        pdf.drawString(
            50,
            y,
            f"{item.product.name} x{item.quantity} - {item.price} FCFA"
        )

        y -= 20


    y -= 20


    pdf.drawString(
        50,
        y,
        f"TOTAL : {order.total} FCFA"
    )


    pdf.save()


    return f"orders/{filename}"