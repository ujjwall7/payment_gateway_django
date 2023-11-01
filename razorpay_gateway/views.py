from django.shortcuts import render
import razorpay
from . models import *
from django.views.decorators.csrf import csrf_exempt



def index(request):
    if request.method=="POST":
        name = request.POST.get('name')
        amount = int(request.POST.get('amount')) * 100
        client = razorpay.Client(auth=("rzp_test_SjQuoGgh17Ps5G" , "BmNrvpc0S7W7aqGkFn8oknrw"))
        # client = razorpay.Client(auth=("PUBLIC KEY" , "SECRET KEY"))

        #Payment capture = 1 for automatic , 0 for manual
        payment = client.order.create({'amount':amount , 'currency':'INR' , 'payment_capture':'1'})
        print('Payment : ',payment)
        coffee = Coffee.objects.create(name = name,
                                       amount = amount,
                                       order_id = payment['id'])
        return render(request, 'razorpay/razorpay.html' ,{'payment':payment})
    return render(request, "razorpay/razorpay.html")

@csrf_exempt
def success(request):
    if request.method == "POST":
        a =  (request.POST)    #jo bhi razor pay ne bheja hoga post karke vo a ke andar store kar lenge
        print(a)
        order_id = ""

        for key , value in a.items():
            if key=="razorpay_order_id":
                order_id = value
                break
        user = Coffee.objects.filter(order_id=order_id).last()
        user.paid=True
        user.save()
    return render(request, "razorpay/success.html")


"""
Example

a = {'apple': 1, 'banana': 2, 'cherry': 3}
target_key = 'banana'

for key, item in a.items():
    if key == target_key:
        print(f"Key: {key}, Value: {item}")
        break
else:
    print(f"{target_key} not found in the dictionary.")


a = {'apple': 1, 'banana': 2, 'cherry': 3}
target_key = 'banana'

for key, item in a.items():
    if key == target_key:
        print(f"Key: {key}, Value: {item}")
        break
else:
    print(f"{target_key} not found in the dictionary.")
"""

