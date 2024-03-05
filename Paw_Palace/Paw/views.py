from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from .models import *
from django.contrib import messages
import datetime
import razorpay


# Create your views here.
def index(re):
    data_count = Petuser.objects.all().count()
    data_count2 = Petshop.objects.all().count()
    data_count3 = Product.objects.all().count()
    return render(re, 'index.html', {'data_count': data_count,'data_count2': data_count2,'data_count3': data_count3})

def shopregister(re):
    if re.method == 'POST':
        petshopname = re.POST['pts1']
        ownername = re.POST['pts2']
        adress = re.POST['pts3']
        phone = re.POST['pts4']
        email = re.POST['pts5']
        username = re.POST['pts6']
        password = re.POST['pts7']
        data = Petshop.objects.create(shopname=petshopname, ownername=ownername, adress=adress, phone=phone, email=email, username=username, password=password)
        data.save()
        messages.success(re, 'Registered Sucessfully')
        return render(re, 'Shop Register.html')
    else:
        return render(re, 'Shop Register.html')

def userreg(re):
    if re.method == 'POST':
        name = re.POST['us1']
        phone = re.POST['us2']
        email= re.POST['us3']
        username = re.POST['us4']
        password = re.POST['us5']
        data = Petuser.objects.create(name=name, phone=phone, email=email, username=username, password=password)
        data.save()
        messages.success(re, 'Registered Sucessfully')
        return render(re,'User Register.html')
    else:
        return render(re,'User Register.html')

def log(re):
    if re.method=='POST':
        usname=re.POST['un']
        password=re.POST['ps']
        try:
            data = Petuser.objects.get(username=usname)
            if data.password==password:
                re.session['id'] = usname
                return redirect(userhome)
            else:
                messages.error(re,'Username or Password incorrect')
                return redirect(log)
        except Exception:
            try:
                data1 = Petshop.objects.get(username=usname)
                if data1.password==password and data1.suspense==False:
                    re.session['id1'] = usname
                    return redirect(shophome)
                else:
                    messages.info(re, 'Username or Password incorrect or shop is suspended by admin')
                    return redirect(log)
            except Exception:
                if usname=='admin' and password=='admin':
                    re.session['id2']=usname
                    return redirect(adminhome)
                else:
                    messages.info(re, 'Username Incorrect')
                    return redirect(log)
    else:
        return render(re,'index.html')

def userhome(re):
    if 'id' in re.session:
        user = Petuser.objects.get(username=re.session['id'])
        notifications = UserNotification.objects.filter(user=user,seen=False)
        unread_count = notifications.filter(seen=False).count()
        latest_reviews = Reviews.objects.order_by('-id')[:6]
        cartitems = Cart.objects.filter(user=user).count()
        return render(re, 'userhome.html', {'notifications':notifications ,'unread_count': unread_count, 'feedback': latest_reviews,'user':user,'cartcount':cartitems})
    else:
        return redirect(log)

def userlogout(re):
    if 'id' in re.session:
        re.session.flush()
        return redirect(log)

def shophome(re):
    if 'id1' in re.session:
        shop = Petshop.objects.get(username=re.session['id1'])
        latest_reviews = Reviews.objects.order_by('-id')[:4]
        return render(re,'shophome.html',{'feedback': latest_reviews,'shop':shop})
    else:
        return redirect(log)

def unsuspense(re,id):
    if 'id2' in re.session:
        suspense = Petshop.objects.filter(pk=id)
        for shop in suspense:
            shop.suspense = False
            shop.save()

        return redirect(petshopdetails)
    return redirect(log)

def suspense(re,id):
    if 'id2' in re.session:
        suspense = Petshop.objects.filter(pk=id)
        for shop in suspense:
            shop.suspense = True
            shop.save()

        return redirect(petshopdetails)
    return redirect(log)

def shoplogout(re):
    if 'id1' in re.session:
        re.session.flush()
        return redirect(log)

def adminhome(re):
    if 'id2' in re.session:
        latest_reviews = Reviews.objects.order_by('-id')[:4]
        return render(re,'admin.html',{'feedback': latest_reviews})
    else:
        return redirect(log)

def adminlogout(re):
    if 'id2' in re.session:
        re.session.flush()
        return redirect(log)

def about(re):
    data_count = Petuser.objects.all().count()
    data_count2 = Petshop.objects.all().count()
    data_count3 = Product.objects.all().count()
    data=Reviews.objects.all()
    return render(re,'about.html',{'data_count': data_count,'data_count2': data_count2,'data_count3': data_count3,'data':data})

def shopabout(re):
    data_count = Petuser.objects.all().count()
    data_count2 = Petshop.objects.all().count()
    data_count3 = Product.objects.all().count()
    data=Reviews.objects.all()
    return render(re,'shopabout.html',{'data_count': data_count,'data_count2': data_count2,'data_count3': data_count3,'data':data})

def userabout(re):
    data_count = Petuser.objects.all().count()
    data_count2 = Petshop.objects.all().count()
    data_count3 = Product.objects.all().count()
    data=Reviews.objects.all()
    return render(re,'userabout.html',{'data_count': data_count,'data_count2': data_count2,'data_count3': data_count3,'data':data})
def addnotfication(re):
    if 'id1' in re.session:
        shop = Petshop.objects.get(username=re.session['id1'])
        if re.method == 'POST':
            message = re.POST['nty']
            notification = Notification.objects.create(shop=shop,message=message)

            # Attach the notification to all users
            users = Petuser.objects.all()
            for user in users:
                UserNotification.objects.create(user=user, notification=notification, seen=False)

            messages.success(re, 'Notification posted successfully')
            return redirect(addnotfication)

        return render(re, 'addnotification.html')
    else:
        return redirect(log)

def userdetails(re):
    if 'id2' in re.session:
        data=Petuser.objects.all()
        return render(re,'users.html',{'data':data})
    else:
        return (log)

def petshopdetails(re):
    if 'id2' in re.session:
        data=Petshop.objects.all()
        return render(re,'shops.html',{'data':data})
    else:
        return (log)
def gallery(re):
    if 'id' in re.session:
        data=Gallery.objects.filter(accept=True)
        return render(re,'gallery.html',{'data':data})
    else:
        return redirect(log)

def shopgallery(re):
    if 'id1' in re.session:
        data=Gallery.objects.filter(accept=True)
        return render(re,'shopgallery.html',{'data':data})
    else:
        return redirect(log)

def admingallery(re):
    if 'id2' in re.session:
        data=Gallery.objects.filter(accept=True)
        return render(re,'admingallery.html',{'data':data})
    else:
        return redirect(log)

def markasseen(re,id):
    if 'id' in re.session:
        user = Petuser.objects.get(username=re.session['id'])
        unseen_notifications = UserNotification.objects.filter(user=user, seen=False,notification_id=id)
        for notification in unseen_notifications:
            notification.seen = True
            notification.save()

        return redirect(userhome)
    return redirect(log)

def addphotos(re):
    if 'id' in re.session or 'id1' in re.session:
        if re.method=='POST':
            category=re.POST['g1']
            breed=re.POST['g2']
            image = re.FILES['image']
            data = Gallery.objects.create(category=category, breed=breed, image=image)
            data.save()
            messages.info(re, 'once admin accept your photo it will show on gallery')
            return redirect(gallery)
        else:
            return redirect(addphotos)
    else:
        return redirect(log)

def photoreq(re):
    if 'id2' in re.session:
        data=Gallery.objects.filter(accept=False)
        return render(re,'photoreq.html',{'data':data})
    else:
        return redirect(log)
def acceptphoto(re,id):
    if 'id2' in re.session:
        accepted = Gallery.objects.filter(pk=id)
        for photos in accepted:
            photos.accept = True
            photos.save()

        return redirect(photoreq)
    return redirect(log)

def deletePhoto(re,id):
    if 'id2' in re.session:
        deleted=Gallery.objects.filter(pk=id)
        for photos in deleted:
            photos.delete()

        return redirect(photoreq)
    return redirect(log)

def addreviews(re):
    if 'id' in re.session:
        if re.method=='POST':
            review = re.POST['feedback']
            user = Petuser.objects.get(username=re.session['id'])
            feedback=Reviews.objects.create(user=user,review=review)
            feedback.save()
            messages.success(re,'Review Added Successfully')
            return redirect(userhome)
        else:
            return render(userhome)
    else:
        return render(log)


def editprofile(re):
    if 'id' in re.session:
        data=Petuser.objects.get(username=re.session['id'])
        return render(re,'editprofile.html',{'data':data})
    else:
        return redirect(log)

def editshopprofile(re):
    if 'id1' in re.session:
        data=Petshop.objects.get(username=re.session['id1'])
        return render(re,'editshopprofile.html',{'data':data})
    else:
        return redirect(log)

def updateuspf(re):
    if 'id' in re.session:
        uname = re.session['id']
        if re.method=='POST':
            name = re.POST['us1']
            phone = re.POST['us2']
            email = re.POST['us3']
            username = re.POST['us4']
            password = re.POST['us5']
            data1 = Petuser.objects.filter(username=uname).update(name=name, phone=phone, email=email, username=username, password=password)
            messages.success(re,'Profile Updated')
            return redirect(editprofile)
        else:
            return render(re,'editprofile.html')
    else:
        return redirect(log)

def updatesppf(re):
    if 'id1' in re.session:
        uname = re.session['id1']
        if re.method=='POST':
            petshopname = re.POST['pts1']
            ownername = re.POST['pts2']
            adress = re.POST['pts3']
            phone = re.POST['pts4']
            email = re.POST['pts5']
            username = re.POST['pts6']
            password = re.POST['pts7']
            data1 = Petshop.objects.filter(username=uname).update(shopname=petshopname,ownername=ownername,adress=adress, phone=phone, email=email, username=username, password=password)
            messages.success(re,'Profile Updated')
            return redirect(editshopprofile)
        else:
            return render(re,'editshopprofile.html')
    else:
        return redirect(log)

def shopping(re):
    if 'id' in re.session:
        user = Petuser.objects.get(username=re.session['id'])
        data = Product.objects.all()
        data1 = Product.objects.filter(category="Medicines")
        data3 = Product.objects.filter(category="Food")
        data4= Product.objects.filter(category="Accessories")
        cart_product_ids = Cart.objects.filter(user=user).values_list('product__id', flat=True)
        data2 = Cart.objects.filter(user=user).count()
        return render(re, 'shop.html', {'data': data, 'data1': data1, 'cart_product_ids': cart_product_ids,'data2':data2, 'data3': data3, 'data4': data4})
    else:
        return redirect(log)

def services(re):
    if 'id' in re.session:
        data=Services.objects.all()
        return render(re, 'servicesdetail.html', {'data': data})
    else:
        return redirect(log)

def addproducts(re):
    if 'id1' in re.session:
        petshop =Petshop.objects.get(username=re.session['id1'])
        if re.method=='POST':
            prodname = re.POST['g1']
            price = re.POST['g2']
            category = re.POST['g4']
            quantity = re.POST['g3']
            image = re.FILES['image']
            data=Product.objects.create(shop=petshop,prodname=prodname,price=price,category=category,qty=quantity,image=image)
            data.save()
            messages.success(re,'Product Added Succesfully')
            return render(re,'products.html')
        else:
            return render(re,'products.html')
    else:
        return render(log)

def shopproducts(re):
    if 'id1' in re.session:
        data = Petshop.objects.get(username=re.session['id1'])
        data1 = Product.objects.filter(shop=data)
        return render(re, 'shopproducts.html', { 'data1': data1})
    else:
        return redirect(log)

def shopservices(re):
    if 'id1' in re.session:
        data = Petshop.objects.get(username=re.session['id1'])
        data1 = Services.objects.filter(shop=data)
        return render(re, 'shopservices.html', { 'data1': data1})
    else:
        return redirect(log)

def editproducts(re,id):
    if 'id1' in re.session:
        data=Product.objects.get(pk=id)
        return render(re,'editproduct.html',{'data':data})
    else:
        return redirect(log)


def editserv(re,id):
    if 'id1' in re.session:
        data=Services.objects.get(pk=id)
        return render(re,'editservices.html',{'data':data})
    else:
        return redirect(log)

def updateproduct(re,id):
    if 'id1' in re.session:
        if re.method=='POST':
            prodname = re.POST['g1']
            price = re.POST['g2']
            quantity = re.POST['g3']
            data1 = Product.objects.filter(pk=id).update(prodname=prodname,price=price, qty=quantity)
            messages.info(re,'Product Updated')
            return redirect(shopproducts)
        else:
            return redirect(shopproducts)
    else:
        return redirect(log)

def updateserv(re,id):
    if 'id1' in re.session:
        if re.method=='POST':
            price = re.POST['g2']
            desc = re.POST['g3']
            data1 = Services.objects.filter(pk=id).update(price=price,desc=desc)
            messages.info(re,'Service Updated')
            return redirect(shopservices)
        else:
            return redirect(shopservices)
    else:
        return redirect(log)

def deleteprod(re,id):
    if 'id1' in re.session:
        deleted = Product.objects.filter(pk=id)
        for prod in deleted:
            prod.delete()

        messages.success(re,'Sucessfully Deleted')
        return redirect(shopproducts)
    return redirect(log)

def deleteserv(re,id):
    if 'id1' in re.session:
        deleted = Services.objects.filter(pk=id)
        for serv in deleted:
            serv.delete()

        messages.success(re,'Sucessfully Deleted')
        return redirect(shopservices)
    return redirect(log)


def addservices(re):
    if 'id1' in re.session:
        petshop =Petshop.objects.get(username=re.session['id1'])
        if re.method=='POST':
            servicename = re.POST['g1']
            price = re.POST['g2']
            desc = re.POST['g3']
            image = re.FILES['image']
            data=Services.objects.create(shop=petshop,servicename=servicename,price=price,desc=desc,image=image)
            data.save()
            messages.info(re,'Service Added Successfully')
            return render(re,'services.html')
        else:
            return render(re,'services.html')
    else:
        return render(log)

def addtocart(re,id):
    if 'id' in re.session:
        user = Petuser.objects.get(username=re.session['id'])
        product = Product.objects.get(pk=id)
        data=Cart.objects.create(user=user, product=product,quantity=1,total_price=product.price)
        data.save()
        messages.success(re,'Item Added to Cart')
        return redirect(shopping)
    else:
        return redirect(log)

def cart(re):
    if 'id' in re.session:
        user = Petuser.objects.get(username=re.session['id'])
        data=Cart.objects.filter(user=user)
        data1 = Cart.objects.filter(user=user).count()
        total=0
        for i in data:
            total+=i.product.price*i.quantity
        return render(re,'cart.html',{'data':data, 'data1':data1, 'total':total})
    else:
        return redirect(log)


def increment_quantity(re,id):
    if 'id' in re.session:
        cart_item = Cart.objects.get(pk=id)
        if cart_item.product.qty > 1:
            cart_item.quantity =cart_item.quantity + 1
            cart_item.total_price = cart_item.quantity * cart_item.product.price
            cart_item.save()
        return redirect(cart)
    else:
        return redirect(log)


def decrement_quantity(re, id):
    if 'id' in re.session:
        cart_item = Cart.objects.get(pk=id)
        if cart_item.product.qty > 1:
            cart_item.quantity = cart_item.quantity - 1
            cart_item.total_price = cart_item.quantity * cart_item.product.price
            cart_item.save()
        return redirect(cart)
    else:
        return redirect(log)

def dltcartitm(re,id):
    if 'id' in re.session:
        deleted=Cart.objects.filter(pk=id)
        for item in deleted:
            item.delete()

        messages.info(re,'item removed')
        return redirect(cart)
    return redirect(log)


def placeorder(re):
    if 'id' in re.session:
        user = Petuser.objects.get(username=re.session['id'])
        items = Cart.objects.filter(user=user)
        total = 0
        for i in items:
            total += i.product.price * i.quantity

        for cart_item in items:
            if cart_item.quantity > cart_item.product.qty:
                messages.info(re, f'Stock Limit Exceeded for {cart_item.product.prodname}')
                return redirect(cart)
        amount = total * 100
        order_currency = 'INR'
        client = razorpay.Client(
            auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))

        return render(re, 'booking_multiple.html', {'items': items,'total':total,'amount':amount})

    else:
        return redirect(log)


def success(re):
    if 'id' in re.session:
        user=Petuser.objects.get(username=re.session['id'])
        items=Cart.objects.filter(user=user)
        a=datetime.datetime.now().strftime("%Y-%m-%d")
        for i in items:
            item=Product.objects.get(pk=i.product.pk)
            data=Bookings.objects.create(user_details=user,item_details=item,quantity=i.quantity,total_price=i.total_price,date=a)
            data.save()
            item.qty=item.qty-i.quantity
            item.save()
        Cart.objects.all().delete()
        messages.success(re,'All cart items are booked')
        return redirect(shopping)
    else:
        return redirect(log)

def userorders(re):
    if 'id' in re.session:
        user = Petuser.objects.get(username=re.session['id'])
        data = Bookings.objects.filter(user_details=user)
        return render(re,'userorders.html',{'data':data})
    else:
        return redirect(log)


def shoporders(re, id):
    if 'id1' in re.session:
        products = Product.objects.get(pk=id)
        bookings = Bookings.objects.filter(item_details=products)
        return render(re, 'shoporders.html', {'bookings': bookings})
    else:
        return redirect(log)

def review(re):
    if 'id2' in re.session:
        data=Reviews.objects.all()
        return render(re,'review.html',{'data':data})
    else:
        return redirect(log)

def allorders(re):
    if 'id2' in re.session:
        data=Bookings.objects.all()
        return render(re,'orders.html',{'data':data})
    else:
        return redirect(log)

def singleplaceorder(re,id):
    if 'id' in re.session:
        user = Petuser.objects.get(username=re.session['id'])
        items = Product.objects.filter(pk=id)


        for item in items:
            if item.qty == 0:
                messages.info(re, f'Stock Limit Exceeded for {item.prodname}')
                return redirect(shopping)
        order_currency = 'INR'
        client = razorpay.Client(
            auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))

        return render(re, 'shop.html', )

    else:
        return redirect(log)

def singlesuccess(re,id):
    if 'id' in re.session:
        user=Petuser.objects.get(username=re.session['id'])
        product=Product.objects.get(pk=id)
        total=product.price
        a=datetime.datetime.now().strftime("%Y-%m-%d")
        data=Bookings.objects.create(user_details=user,item_details=product,quantity=1,total_price=total,date=a)
        data.save()
        product.qty=product.qty-1
        product.save()
        messages.success(re,'Successfully Ordered')
        return redirect(shopping)
    else:
        return redirect(log)

def bookservice(re,id):
    if 'id' in re.session:
        data=Services.objects.get(pk=id)
        return render(re,'servicebooking.html',{'data':data})
    else:
        return redirect(log)
