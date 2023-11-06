from django.shortcuts import render
from . models import *
from instamojo_wrapper import Instamojo
from django . conf import settings
from django.http import HttpResponse


api = Instamojo(api_key=settings.API_KEY,
                auth_token=settings.AUTH_TOKEN,
                endpoint='https://test.instamojo.com/api/1.1/')




def home(request):
    products=Product.objects.all()
    return render(request,"instamojo/home.html",{'products':products})

def order(request, product_id):
    try:
        product_obj =   Product.objects.get(uid=product_id)
        order_obj , _ = Order.objects.get_or_create(
            product=product_obj,
            is_paid=False,
            user = request.user
        )
        response=api.payment_request_create(
            amount=order_obj.product.prduct_price,
            purpose='Order Process',
            buyer_name='ujjwal sharma',
            email="ujjwal@gmail.com",
            redirect_url="http://24.144.88.78/instamojo/order-success/"
        )
        print(response)
        order_obj.order_id=response['payment_request']['id']
        order_obj.instamojo_response=response
        order_obj.save()
        return render(request,"instamojo/order.html",context={
            'payment_url':response['payment_request']['longurl']
        })

    except Exception as e:
        print(e)
        return render(request,"instamojo/order.html")


def order_success(request):
    payment_request_id=request.GET.get('payment_request_id')
    order_obj=Order.objects.get(order_id=payment_request_id)
    order_obj.is_paid=True
    order_obj.save()
    return HttpResponse("payment successful")





