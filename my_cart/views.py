from django.shortcuts import render
from rest_framework import generics
from main.models import Exhibitions
from .models import Cart, CartLine
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework import status
from main.permissions import UserOnly, StaffOrAdminOrUser, StaffOrAdmin
from .serializer import CartSerializer
import json
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase import ttfonts
from reportlab.lib.pagesizes import letter
from users.models import NewUser
from users.serialize import UsersPostSerializer
from django.core.mail import EmailMessage
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing


class CartView(APIView):
    permission_classes = [StaffOrAdminOrUser]

    def put(self, request, pk, quantity):
        exhibition = Exhibitions.objects.get(id=pk)
        user = request.user
        order_item = CartLine.create(exhibition, quantity,
                                     quantity*exhibition.price)
        order_item.save()
        order, status_tmp = Cart.objects.get_or_create(account=user, is_ordered=False)
        order.items.add(order_item)
        order.amount = Cart.get_cart_amount(order)
        order.save()

        return HttpResponse(request.data, status=status.HTTP_200_OK)

    def delete(self, request, item_id):
        user = request.user
        order = Cart.objects.get(account=user, is_ordered=False)

        item_to_delete = order.items.get(id=item_id)
        item_to_delete.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    def get(self, request):
        user = request.user
        get_data = request.query_params.get('is_ordered')
        if not get_data:
            is_ordered = 0
        else:
            is_ordered = get_data
        orders = Cart.objects.filter(account=user, is_ordered=is_ordered)
        serializer = CartSerializer(orders, many=True, context={'request': request})

        return HttpResponse(json.dumps(serializer.data), status=status.HTTP_200_OK)


class CartPaymentView(APIView):
    permission_classes = [StaffOrAdminOrUser]

    def generate_pdf(self, exh_name, user_name, price, quantity, amount, address, date, time):
        buffer = io.BytesIO()
        cnv = canvas.Canvas(buffer, pagesize=letter)
        cnv.setLineWidth(.4)
        arial_font = ttfonts.TTFont('Arial', '9041.ttf')
        arial_bold_font = ttfonts.TTFont('Arial-Bold', 'arial_bold.ttf')
        pdfmetrics.registerFont(arial_font)
        pdfmetrics.registerFont(arial_bold_font)
        cnv.setFont('Arial-Bold', 14)
        cnv.drawString(30, 750, exh_name)
        cnv.setFont('Arial', 14)
        cnv.drawString(30, 725, date)
        cnv.drawString(150, 725, str(time))
        cnv.drawString(30, 700, address)
        cnv.drawString(30, 675, "Цена")
        cnv.drawString(150, 675, 'Количество')
        cnv.drawString(300, 675, "Стоимость")
        cnv.drawString(30, 650, price + " руб")
        cnv.drawString(150, 650, str(quantity))
        cnv.drawString(300, 650, amount + " руб")
        cnv.drawString(30, 625, "Покупатель: ")
        cnv.drawString(150, 625, user_name)
        cnv.line(0, 600, 620, 600)

        # qr_code = qr.QrCodeWidget('hello')
        #
        # bounds = qr_code.getBounds()
        # width = bounds[2] - bounds[0]
        # height = bounds[3] - bounds[1]
        # c = Drawing(45, 45, transform=[60. / width, 0, 0, 60. / height, 0, 0])
        # c.add(qr_code)
        #
        # cnv.drawImage(c, 30, 575, 50, 50)

        cnv.save()
        pdf = buffer.getvalue()

        # buffer.seek(0)
        return pdf

    def put(self, request):
        user = request.user
        try:
            order = Cart.objects.get(account=user, is_ordered=False)
        except:
            return HttpResponse(request.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        order.is_ordered = True
        order.save()

        letter_str = 'Во вложении данного письма файл, являющийся билетом на мероприятие. ' \
                     'Просим вас распечатать данный билет перед посещением спектакля. ' \
                     'Спасибо за покупку! Ждем Вас снова на нашем сайте.'

        cart_serial = CartSerializer(order)
        account_id = cart_serial.data['account']
        account = NewUser.objects.get(pk=account_id)
        acc_serial = UsersPostSerializer(account)
        if acc_serial.data['first_name'] and acc_serial.data['last_name']:
            acc_name = acc_serial.data['first_name'] + acc_serial.data['last_name']
        else:
            acc_name = acc_serial.data['email']

        msg = EmailMessage("Galartus", letter_str, to=[acc_serial.data['email']])

        for item in cart_serial.data['items']:
            quantity = item['quantity']
            total = item['total']
            exh_name = item['exhibition']['name']
            exh_address = item['exhibition']['address']
            exh_date = item['exhibition']['date']
            exh_time = item['exhibition']['time']
            exh_price = item['exhibition']['price']

            pdf = self.generate_pdf(exh_name, acc_name, exh_price, quantity,
                                       total, exh_address, exh_date, exh_time)

            # return FileResponse(pdf, as_attachment=True, filename='hello.pdf')

            msg.attach(exh_name + '.pdf', pdf, 'application/pdf')

        msg.send()
        return HttpResponse(request.data, status=status.HTTP_200_OK)
