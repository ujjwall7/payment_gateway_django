from django.shortcuts import render
import razorpay
from . models import *
from django.views.decorators.csrf import csrf_exempt

#email files
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def index(request):
    if request.method=="POST":
        name = request.POST.get('name')
        amount = int(request.POST.get('amount')) * 100
        email = request.POST.get('email')
        client = razorpay.Client(auth=("rzp_test_SjQuoGgh17Ps5G" , "BmNrvpc0S7W7aqGkFn8oknrw"))
        # client = razorpay.Client(auth=("PUBLIC KEY" , "SECRET KEY"))

        #Payment capture = 1 for automatic , 0 for manual
        payment = client.order.create({'amount':amount , 'currency':'INR' , 'payment_capture':'1'})
        # print('Payment : ',payment)
        coffee = Coffee.objects.create(name = name,
                                       amount = amount,
                                       order_id = payment['id'],
                                       email = email)
        return render(request, 'razorpay/razorpay.html' ,{'payment':payment})
    return render(request, "razorpay/razorpay.html")

@csrf_exempt
def success(request):
    if request.method == "POST":
        a =  (request.POST)    #jo bhi razor pay ne bheja hoga post karke vo a ke andar store kar lenge
        # print(a)
        order_id = ""

        data = {}
        for key , value in a.items():
            if key=="razorpay_order_id":
                data['razorpay_order_id'] = value

                order_id = value

            elif key=="razorpay_payment_id":
                data['razorpay_payment_id'] = value

            elif key=="razorpay_signature":
                data['razorpay_signature'] = value

        user = Coffee.objects.filter(order_id=order_id).last()
        user.paid=True
        user.save()

        client = razorpay.Client(auth=("rzp_test_SjQuoGgh17Ps5G" , "BmNrvpc0S7W7aqGkFn8oknrw"))
        check = client.utility.verify_payment_signature(data)
        print(check)

        if check is True:
            msg_plain = render_to_string('razorpay/email.txt')
            msg_html = render_to_string('razorpay/email.html')

            send_mail("Your Order Was Confirm! Thanku" , msg_plain , settings.EMAIL_HOST_USER , 
                      [user.email] , html_message = msg_html)
        else:
            return render(request, "razorpay/error.html")
        
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
























