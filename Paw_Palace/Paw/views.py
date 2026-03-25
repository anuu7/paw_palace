from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
from .models import *
from django.contrib import messages
import datetime
import razorpay


# Create your views here.
def index(re):
    data_count = Petuser.objects.all().count()
    data_count2 = Petshop.objects.all().count()
    data_count3 = Product.objects.all().count()
    data = Reviews.objects.order_by('-id').first()
    return render(re, 'index.html', {'data_count': data_count,'data_count2': data_count2,'data_count3': data_count3, 'data': data})

def shopregister(re):
    data_count = Petuser.objects.all().count()
    data_count2 = Petshop.objects.all().count()
    data_count3 = Product.objects.all().count()
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
        return render(re, 'Shop Register.html', {'data_count': data_count,'data_count2': data_count2,'data_count3': data_count3})
    else:
        return render(re, 'Shop Register.html', {'data_count': data_count,'data_count2': data_count2,'data_count3': data_count3})

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
        return render(re,'User Register.html', {'data': Reviews.objects.order_by('-id').first()})
    else:
        return render(re,'User Register.html', {'data': Reviews.objects.order_by('-id').first()})

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
        notifications = UserNotification.objects.filter(user=user, seen=False)
        unread_count = notifications.count()
        latest_reviews = Reviews.objects.order_by('-id')[:6]
        # Sum all quantities in cart for correct item count
        cart_items = Cart.objects.filter(user=user)
        cart_count = sum(item.quantity for item in cart_items)
        return render(re, 'userhome.html', {
            'notifications': notifications,
            'unread_count': unread_count,
            'feedback': latest_reviews,
            'user': user,
            'cartcount': cart_count
        })
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
        # Real-time counts
        customer_count = Petuser.objects.all().count()
        product_count = Product.objects.filter(shop=shop).count()
        shop_count = Petshop.objects.all().count()
        # Notifications for this shop
        notifications = Notification.objects.filter(shop=shop).order_by('-date')[:10]
        unread_count = UserNotification.objects.filter(notification__shop=shop, seen=False).count()
        return render(re,'shophome.html',{
            'feedback': latest_reviews,
            'shop': shop,
            'customer_count': customer_count,
            'product_count': product_count,
            'shop_count': shop_count,
            'notifications': notifications,
            'unread_count': unread_count,
        })
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
    data=Reviews.objects.order_by('-id').first()
    return render(re,'about.html',{'data_count': data_count,'data_count2': data_count2,'data_count3': data_count3,'data':data})

def shopabout(re):
    customer_count = Petuser.objects.all().count()
    shop_count = Petshop.objects.all().count()
    product_count = Product.objects.all().count()
    feedback = Reviews.objects.order_by('-id')[:4]
    return render(re,'shopabout.html',{
        'customer_count': customer_count,
        'shop_count': shop_count,
        'product_count': product_count,
        'feedback': feedback,
    })

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

def markallseen(re):
    """AJAX endpoint: marks all unread notifications as seen and returns JSON."""
    if 'id' in re.session:
        user = Petuser.objects.get(username=re.session['id'])
        updated = UserNotification.objects.filter(user=user, seen=False).update(seen=True)
        return JsonResponse({'success': True, 'message': f'{updated} notification(s) marked as read'})
    if 'id1' in re.session:
        shop = Petshop.objects.get(username=re.session['id1'])
        updated = UserNotification.objects.filter(notification__shop=shop, seen=False).update(seen=True)
        return JsonResponse({'success': True, 'message': f'{updated} notification(s) marked as read'})
    return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=401)

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
        # Get all active (non-suspended) shops
        shops = Petshop.objects.filter(suspense=False)
        # Add product and service counts to each shop
        for shop in shops:
            shop.product_count = Product.objects.filter(shop=shop).count()
            shop.service_count = Services.objects.filter(shop=shop).count()
        cart_product_ids = Cart.objects.filter(user=user).values_list('product__id', flat=True)
        data2 = Cart.objects.filter(user=user).count()
        return render(re, 'shop.html', {'shops': shops, 'cart_product_ids': cart_product_ids,'data2':data2})
    else:
        return redirect(log)

def shopdetail(re, id):
    if 'id' in re.session:
        user = Petuser.objects.get(username=re.session['id'])
        shop = get_object_or_404(Petshop, pk=id)
        products = Product.objects.filter(shop=shop)
        services = Services.objects.filter(shop=shop)
        cart_product_ids = Cart.objects.filter(user=user).values_list('product__id', flat=True)
        return render(re, 'shopdetail.html', {
            'shop': shop,
            'products': products,
            'services': services,
            'cart_product_ids': cart_product_ids,
        })
    else:
        return redirect(log)

def book_service(re):
    if 'id' not in re.session:
        return JsonResponse({'success': False, 'error': 'Not logged in'}, status=401)

    if re.method == 'POST':
        user = Petuser.objects.get(username=re.session['id'])
        service_id = re.POST.get('service_id')
        booking_date = re.POST.get('booking_date')
        booking_slot = re.POST.get('booking_slot')
        pet_name = re.POST.get('pet_name')
        pet_type = re.POST.get('pet_type')
        notes = re.POST.get('notes', '')

        service = get_object_or_404(Services, pk=service_id)

        # Prevent double-booking (case-insensitive)
        if ServiceBooking.objects.filter(service=service, booking_date=booking_date, booking_slot__iexact=booking_slot).exists():
            return JsonResponse({'success': False, 'error': 'This slot is already booked. Please choose another.'})

        # Create the booking
        booking = ServiceBooking.objects.create(
            user=user,
            service=service,
            pet_name=pet_name,
            pet_type=pet_type,
            booking_date=booking_date,
            booking_slot=booking_slot,
            notes=notes,
            status='confirmed'
        )

        # Create notification for shop owner
        notification = Notification.objects.create(
            shop=service.shop,
            message=f"New booking for {service.servicename} by {user.name} for {pet_name} on {booking_date} at {booking_slot}"
        )
        UserNotification.objects.create(user=user, notification=notification, seen=False)

        return JsonResponse({'success': True, 'message': 'Service booked successfully!'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

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
            prodname = re.POST.get('prodname', '')
            price = re.POST.get('price', 0)
            category = re.POST.get('category', 'Other')
            quantity = re.POST.get('qty', 0)
            image = re.FILES.get('image')
            pettype = re.POST.get('pettype', 'All Pets')
            desc = re.POST.get('desc', '')
            if prodname and price and image:
                Product.objects.create(shop=petshop, prodname=prodname, price=price, category=category, qty=quantity, image=image, pettype=pettype, description=desc)
                messages.success(re, 'Product Added Successfully!')
            else:
                messages.error(re, 'Please fill all required fields.')
            return redirect('shopproducts')
        else:
            return render(re,'products.html')
    else:
        return redirect(log)

def shopproducts(re):
    page = int(re.GET.get('page', 1))
    if 'id1' in re.session:
        shop = Petshop.objects.get(username=re.session['id1'])
        products = Product.objects.filter(shop=shop).order_by('-id')
        # Filters
        search = re.GET.get('search', '')
        cat_filter = re.GET.get('category', '')
        if search:
            products = products.filter(prodname__icontains=search)
        if cat_filter:
            products = products.filter(category=cat_filter)
        # Pagination
        paginator = Paginator(products, 10)
        try:
            products_page = paginator.page(page)
        except:
            products_page = paginator.page(1)
        categories = ['Food', 'Toys', 'Accessories', 'Healthcare', 'Grooming', 'Bedding', 'Other']
        return render(re, 'shopproducts.html', {
            'data1': products_page,
            'categories': categories,
            'search': search,
            'cat_filter': cat_filter,
        })
    return redirect(log)

def all_products(re):
    if 'id' in re.session:
        user = Petuser.objects.get(username=re.session['id'])
        products = Product.objects.all()
        cart_product_ids = Cart.objects.filter(user=user).values_list('product__id', flat=True)
        return render(re, 'allproducts.html', {'products': products, 'cart_product_ids': cart_product_ids})
    else:
        return redirect(log)

def shopservices(re):
    page = int(re.GET.get('page', 1))
    if 'id1' in re.session:
        shop = Petshop.objects.get(username=re.session['id1'])
        services = Services.objects.filter(shop=shop).order_by('-id')
        # Filters
        search = re.GET.get('search', '')
        if search:
            services = services.filter(servicename__icontains=search)
        # Pagination
        paginator = Paginator(services, 10)
        try:
            services_page = paginator.page(page)
        except:
            services_page = paginator.page(1)
        return render(re, 'shopservices.html', {
            'data1': services_page,
            'search': search,
        })
    return redirect(log)

def all_services(re):
    if 'id' in re.session:
        user = Petuser.objects.get(username=re.session['id'])
        services = Services.objects.all()
        today = datetime.date.today()
        return render(re, 'allservices.html', {'services': services})
    else:
        return redirect(log)

def editproducts(re,id):
    if 'id1' in re.session:
        return redirect(shopproducts)
    else:
        return redirect(log)


def editserv(re,id):
    if 'id1' in re.session:
        return redirect(shopservices)
    else:
        return redirect(log)

def updateproduct(re,id):
    if 'id1' in re.session:
        if re.method=='POST':
            price = re.POST.get('g2') or re.POST.get('price', '')
            quantity = re.POST.get('g3') or re.POST.get('qty', '')
            pettype = re.POST.get('pettype', 'All Pets')
            description = re.POST.get('description', '')
            Product.objects.filter(pk=id).update(price=price, qty=quantity, pettype=pettype, description=description)
            messages.success(re,'Product Updated Successfully!')
            return redirect(shopproducts)
        else:
            return redirect(shopproducts)
    else:
        return redirect(log)

def updateserv(re,id):
    if 'id1' in re.session:
        if re.method=='POST':
            price = re.POST.get('g2') or re.POST.get('price', '')
            desc = re.POST.get('g3') or re.POST.get('desc', '')
            duration = re.POST.get('duration', '')
            Services.objects.filter(pk=id).update(price=price, desc=desc, duration=duration)
            messages.success(re,'Service Updated Successfully!')
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
            servicename = re.POST.get('servicename', '')
            price = re.POST.get('price', 0)
            desc = re.POST.get('desc', '')
            duration = re.POST.get('duration', '')
            image = re.FILES.get('image')
            if servicename and price and image:
                Services.objects.create(shop=petshop, servicename=servicename, price=price, desc=desc, image=image, duration=duration)
                messages.success(re, 'Service Added Successfully!')
            else:
                messages.error(re, 'Please fill all required fields.')
            return redirect('shopservices')
        return redirect('shopservices')
    else:
        return render(log)

def addtocart(re,id):
    if 'id' in re.session:
        user = Petuser.objects.get(username=re.session['id'])
        product = Product.objects.get(pk=id)
        # Check if product already in cart — increment quantity instead of adding new row
        existing = Cart.objects.filter(user=user, product=product).first()
        if existing:
            existing.quantity += 1
            existing.total_price = existing.quantity * existing.product.price
            existing.save()
            messages.success(re, f'Updated {product.name} quantity to {existing.quantity} in cart')
        else:
            Cart.objects.create(user=user, product=product, quantity=1, total_price=product.price)
            messages.success(re, 'Item Added to Cart')
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

        return render(re, 'booking_multiple.html', {
            'items': items,
            'total': total,
            'amount': amount,
            'user': user,
            'cartcount': sum(i.quantity for i in items),
            'unread_count': UserNotification.objects.filter(user=user, seen=False).count(),
            'notifications': UserNotification.objects.filter(user=user, seen=False)
        })

    else:
        return redirect(log)


def success(re):
    if 'id' in re.session:
        user=Petuser.objects.get(username=re.session['id'])
        items=Cart.objects.filter(user=user)
        a=datetime.datetime.now().strftime("%Y-%m-%d")
        delivery_address = re.POST.get('delivery_address', '')

        for i in items:
            item=Product.objects.get(pk=i.product.pk)
            data=Bookings.objects.create(user_details=user,item_details=item,quantity=i.quantity,total_price=i.total_price,date=a,delivery_address=delivery_address)
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
        product_orders = Bookings.objects.filter(user_details=user).order_by('-id')
        service_bookings = ServiceBooking.objects.filter(user=user).order_by('-id')
        # Active = not delivered and not cancelled
        active_count = (
            product_orders.exclude(status__in=['delivered', 'cancelled']).count() +
            service_bookings.exclude(status__in=['completed', 'cancelled']).count()
        )
        return render(re, 'userorders.html', {
            'product_orders': product_orders,
            'service_bookings': service_bookings,
            'active_count': active_count,
        })
    else:
        return redirect(log)


def shoporders(re, id):
    if 'id1' in re.session:
        products = Product.objects.get(pk=id)
        bookings = Bookings.objects.filter(item_details=products)
        return render(re, 'shoporders.html', {'bookings': bookings})
    else:
        return redirect(log)

def shopallorders(re):
    """All orders (product + service) for the logged-in shop owner"""
    page = int(re.GET.get('page', 1))
    if 'id1' in re.session:
        shop = Petshop.objects.get(username=re.session['id1'])
        # Filters
        status_filter = re.GET.get('status', '')
        order_type = re.GET.get('type', 'all')
        # Product bookings
        product_bookings = Bookings.objects.filter(item_details__shop=shop).select_related('user_details', 'item_details').order_by('-date')
        if status_filter:
            product_bookings = product_bookings.filter(status=status_filter)
        # Service bookings
        service_bookings = ServiceBooking.objects.filter(service__shop=shop).select_related('user', 'service').order_by('-created_at')
        if status_filter:
            service_bookings = service_bookings.filter(status=status_filter)
        # Paginate product bookings
        paginator = Paginator(product_bookings, 10)
        try:
            bookings_page = paginator.page(page)
        except:
            bookings_page = paginator.page(1)
        statuses = ['pending', 'confirmed', 'dispatched', 'shipped', 'out_for_delivery', 'delivered', 'cancelled']
        service_statuses = ['pending', 'confirmed', 'completed', 'cancelled']
        return render(re, 'shoporders.html', {
            'bookings': bookings_page,
            'service_bookings': service_bookings,
            'status_filter': status_filter,
            'order_type': order_type,
            'statuses': statuses,
            'service_statuses': service_statuses,
        })
    return redirect(log)

def update_order_status(re, booking_id):
    """Update order status - for shop owners"""
    if 'id1' not in re.session:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=401)
    shop = Petshop.objects.get(username=re.session['id1'])
    new_status = re.POST.get('status', '')
    if new_status:
        # Try product booking
        booking = Bookings.objects.filter(pk=booking_id, item_details__shop=shop).first()
        if booking:
            booking.status = new_status
            booking.save()
            return JsonResponse({'success': True, 'status': new_status})
        # Try service booking
        service_booking = ServiceBooking.objects.filter(pk=booking_id, service__shop=shop).first()
        if service_booking:
            service_booking.status = new_status
            service_booking.save()
            return JsonResponse({'success': True, 'status': new_status})
    return JsonResponse({'success': False, 'error': 'Not found'}, status=404)

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
        return render(re, 'single_checkout.html', {'product': product, 'total': total, 'user': user})
    else:
        return redirect(log)

def confirm_single_order(re):
    if 'id' in re.session:
        user=Petuser.objects.get(username=re.session['id'])
        product_id = re.POST.get('product_id')
        delivery_address = re.POST.get('delivery_address', '')

        product=Product.objects.get(pk=product_id)
        total=product.price
        a=datetime.datetime.now().strftime("%Y-%m-%d")
        data=Bookings.objects.create(user_details=user,item_details=product,quantity=1,total_price=total,date=a,delivery_address=delivery_address)
        data.save()
        product.qty=product.qty-1
        product.save()
        messages.success(re,'Successfully Ordered')
        return redirect(shopping)
    else:
        return redirect(log)

def bookservice(re, id):
    if 'id' in re.session:
        data = Services.objects.get(pk=id)
        # Default to today; use selected date if provided
        selected_date = re.GET.get('booking_date', datetime.date.today().isoformat())
        booked = list(
            ServiceBooking.objects
            .filter(service=data, booking_date=selected_date)
            .values_list('booking_slot', flat=True)
        )
        return render(re, 'servicebooking.html', {
            'data': data,
            'booked_slots': booked,
            'booked_slots_json': json.dumps(booked),
            'selected_date': selected_date,
            'today': datetime.date.today().isoformat(),
        })
    else:
        return redirect(log)

def get_booked_slots(re, id):
    """JSON API: returns booked slots for a given service and date."""
    if 'id' not in re.session:
        return JsonResponse({'error': 'Not logged in'}, status=401)
    try:
        service = Services.objects.get(pk=id)
    except Services.DoesNotExist:
        return JsonResponse({'error': 'Service not found'}, status=404)
    date = re.GET.get('date', datetime.date.today().isoformat())
    booked = list(
        ServiceBooking.objects
        .filter(service=service, booking_date=date)
        .values_list('booking_slot', flat=True)
    )
    return JsonResponse({'booked_slots': booked})
