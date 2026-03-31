from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
from django.contrib import messages as django_messages
from .models import *
from django.contrib import messages
from .decorators import user_required, shop_required, admin_required, user_or_shop_required
import datetime
import razorpay


# Public views (no auth required)
def index(re):
    data_count = Petuser.objects.filter(isDeleted=False).count()
    data_count2 = Petshop.objects.filter(isDeleted=False).count()
    data_count3 = Product.objects.filter(isDeleted=False).count()
    data = Reviews.objects.filter(isDeleted=False).order_by('-id').first()
    return render(re, 'index.html', {'data_count': data_count, 'data_count2': data_count2, 'data_count3': data_count3, 'data': data})

def shopregister(re):
    data_count = Petuser.objects.filter(isDeleted=False).count()
    data_count2 = Petshop.objects.filter(isDeleted=False).count()
    data_count3 = Product.objects.filter(isDeleted=False).count()
    if re.method == 'POST':
        petshopname = re.POST['pts1']
        ownername = re.POST['pts2']
        adress = re.POST['pts3']
        phone = re.POST['pts4']
        email = re.POST['pts5']
        username = re.POST['pts6']
        password = re.POST['pts7']
        data = Petshop(shopname=petshopname, ownername=ownername, adress=adress, phone=phone, email=email, username=username, password=password)
        data.set_password(password)
        data.save()
        messages.success(re, 'Registered Sucessfully')
        return render(re, 'Shop Register.html', {'data_count': data_count, 'data_count2': data_count2, 'data_count3': data_count3})
    return render(re, 'Shop Register.html', {'data_count': data_count, 'data_count2': data_count2, 'data_count3': data_count3})

def userreg(re):
    if re.method == 'POST':
        name = re.POST['us1']
        phone = re.POST['us2']
        email = re.POST['us3']
        username = re.POST['us4']
        password = re.POST['us5']
        data = Petuser(name=name, phone=phone, email=email, username=username, password=password)
        data.set_password(password)
        data.save()
        messages.success(re, 'Registered Sucessfully')
        return render(re, 'User Register.html', {'data': Reviews.objects.filter(isDeleted=False).order_by('-id').first()})
    return render(re, 'User Register.html', {'data': Reviews.objects.filter(isDeleted=False).order_by('-id').first()})

def about(re):
    data_count = Petuser.objects.filter(isDeleted=False).count()
    data_count2 = Petshop.objects.filter(isDeleted=False).count()
    data_count3 = Product.objects.filter(isDeleted=False).count()
    data = Reviews.objects.filter(isDeleted=False).order_by('-id').first()
    return render(re, 'about.html', {'data_count': data_count, 'data_count2': data_count2, 'data_count3': data_count3, 'data': data})

def shopabout(re):
    customer_count = Petuser.objects.filter(isDeleted=False).count()
    shop_count = Petshop.objects.filter(isDeleted=False).count()
    product_count = Product.objects.filter(isDeleted=False).count()
    feedback = Reviews.objects.filter(isDeleted=False).order_by('-id')[:4]
    return render(re, 'shopabout.html', {
        'customer_count': customer_count,
        'shop_count': shop_count,
        'product_count': product_count,
        'feedback': feedback,
    })

def userabout(re):
    data_count = Petuser.objects.filter(isDeleted=False).count()
    data_count2 = Petshop.objects.filter(isDeleted=False).count()
    data_count3 = Product.objects.filter(isDeleted=False).count()
    data = Reviews.objects.filter(isDeleted=False).all()
    return render(re, 'userabout.html', {'data_count': data_count, 'data_count2': data_count2, 'data_count3': data_count3, 'data': data})


# Authentication views
def log(re):
    if re.method == 'POST':
        usname = re.POST['un']
        password = re.POST['ps']
        try:
            data = Petuser.objects.get(username=usname, isDeleted=False)
            if data.check_password(password):
                re.session['id'] = usname
                return redirect(userhome)
            messages.error(re, 'Username or Password incorrect')
            return redirect(log)
        except Petuser.DoesNotExist:
            try:
                data1 = Petshop.objects.get(username=usname, isDeleted=False)
                if data1.check_password(password):
                    if data1.suspense:
                        messages.info(re, 'Your shop account is suspended by the admin')
                        return redirect(log)
                    re.session['id1'] = usname
                    return redirect(shophome)
                messages.info(re, 'Username or Password incorrect')
                return redirect(log)
            except Petshop.DoesNotExist:
                if usname == 'admin' and password == 'admin':
                    re.session['id2'] = usname
                    return redirect(adminhome)
                messages.info(re, 'Username Incorrect')
                return redirect(log)
    return render(re, 'index.html')


# User views
@user_required
def userhome(re):
    user = Petuser.objects.get(username=re.session['id'], isDeleted=False)
    notifications = UserNotification.objects.filter(user=user, seen=False, isDeleted=False)
    unread_count = notifications.count()
    latest_reviews = Reviews.objects.filter(isDeleted=False).order_by('-id')[:6]
    cart_items = Cart.objects.filter(user=user, isDeleted=False)
    cart_count = sum(item.quantity for item in cart_items)
    return render(re, 'userhome.html', {
        'notifications': notifications,
        'unread_count': unread_count,
        'feedback': latest_reviews,
        'user': user,
        'cartcount': cart_count
    })

@user_required
def userlogout(re):
    re.session.flush()
    return redirect(log)


# Shop owner views
@shop_required
def shophome(re):
    shop = Petshop.objects.get(username=re.session['id1'], isDeleted=False)
    latest_reviews = Reviews.objects.filter(isDeleted=False).order_by('-id')[:4]
    customer_count = Petuser.objects.filter(isDeleted=False).count()
    product_count = Product.objects.filter(shop=shop, isDeleted=False).count()
    shop_count = Petshop.objects.filter(isDeleted=False).count()
    notifications = ShopNotification.objects.filter(shop=shop, seen=False, isDeleted=False).order_by('-notification__date')[:10]
    unread_count = notifications.count()
    return render(re, 'shophome.html', {
        'feedback': latest_reviews,
        'shop': shop,
        'customer_count': customer_count,
        'product_count': product_count,
        'shop_count': shop_count,
        'notifications': notifications,
        'unread_count': unread_count,
    })

@shop_required
def shoplogout(re):
    re.session.flush()
    return redirect(log)


# Admin views
@admin_required
def adminhome(re):
    latest_reviews = Reviews.objects.filter(isDeleted=False).order_by('-id')[:4]
    return render(re, 'admin.html', {
        'feedback': latest_reviews,
        'user_count': Petuser.objects.filter(isDeleted=False).count(),
        'shop_count': Petshop.objects.filter(isDeleted=False).count(),
        'order_count': Bookings.objects.filter(isDeleted=False).count(),
        'review_count': Reviews.objects.filter(isDeleted=False).count(),
    })

@admin_required
def adminlogout(re):
    re.session.flush()
    return redirect(log)

@admin_required
def unsuspense(re, id):
    Petshop.objects.filter(pk=id).update(suspense=False)
    return redirect(petshopdetails)

@admin_required
def suspense(re, id):
    Petshop.objects.filter(pk=id).update(suspense=True)
    return redirect(petshopdetails)


# Mixed permission views
def addnotfication(re):
    msg_list = [{'message': str(m), 'type': m.tags or 'success'} for m in django_messages.get_messages(re)]
    messages_json = json.dumps(msg_list)
    if 'id1' in re.session:
        shop = Petshop.objects.get(username=re.session['id1'], isDeleted=False)
        if re.method == 'POST':
            message = re.POST['nty']
            notification = Notification.objects.create(shop=shop, message=message, sender_name=shop.shopname)
            for user in Petuser.objects.filter(isDeleted=False):
                UserNotification.objects.get_or_create(user=user, notification=notification)
            django_messages.success(re, 'Notification posted successfully')
            return redirect(addnotfication)
        return render(re, 'addnotification.html', {'messages_json': messages_json})
    elif 'id2' in re.session:
        if re.method == 'POST':
            message = re.POST['nty']
            shop = Petshop.objects.filter(isDeleted=False).first()
            if not shop:
                django_messages.warning(re, 'No shops registered yet. Notification not sent.')
                return redirect(addnotfication)
            notification = Notification.objects.create(shop=shop, message=message, sender_name='Admin')
            for user in Petuser.objects.filter(isDeleted=False):
                UserNotification.objects.get_or_create(user=user, notification=notification)
            for s in Petshop.objects.filter(isDeleted=False):
                ShopNotification.objects.get_or_create(shop=s, notification=notification)
            django_messages.success(re, 'Notification sent to all users')
            return redirect(addnotfication)
        return render(re, 'addnotification.html', {'messages_json': messages_json})
    return redirect(log)

@shop_required
def shopnotification(re):
    msg_list = [{'message': str(m), 'type': m.tags or 'success'} for m in django_messages.get_messages(re)]
    messages_json = json.dumps(msg_list)
    if re.method == 'POST':
        message = re.POST['nty']
        shop = Petshop.objects.get(username=re.session['id1'], isDeleted=False)
        notification = Notification.objects.create(shop=shop, message=message, sender_name=shop.shopname)
        for user in Petuser.objects.filter(isDeleted=False):
            UserNotification.objects.get_or_create(user=user, notification=notification)
        django_messages.success(re, 'Notification posted successfully')
        return redirect(shopnotification)
    return render(re, 'shopnotification.html', {'messages_json': messages_json})


# User management views
@admin_required
def userdetails(re):
    search_query = re.GET.get('search', '').strip()
    data = Petuser.objects.filter(isDeleted=False)
    if search_query:
        data = data.filter(name__icontains=search_query)
    paginator = Paginator(data, 8)
    page_number = re.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(re, 'users.html', {'data': page_obj, 'total_count': data.count(), 'search_query': search_query})

@admin_required
def petshopdetails(re):
    search_query = re.GET.get('search', '').strip()
    data = Petshop.objects.filter(isDeleted=False)
    if search_query:
        data = data.filter(shopname__icontains=search_query)
    paginator = Paginator(data, 8)
    page_number = re.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(re, 'shops.html', {
        'data': page_obj,
        'total_count': data.count(),
        'active_shops': Petshop.objects.filter(isDeleted=False, suspense=False).count(),
        'suspended_shops': Petshop.objects.filter(isDeleted=False, suspense=True).count(),
        'search_query': search_query,
    })


# Gallery views
@user_required
def gallery(re):
    data = Gallery.objects.filter(accept=True, isDeleted=False)
    return render(re, 'gallery.html', {'data': data})

@shop_required
def shopgallery(re):
    data = Gallery.objects.filter(accept=True, isDeleted=False)
    return render(re, 'shopgallery.html', {'data': data})

@admin_required
def admingallery(re):
    data = Gallery.objects.filter(accept=True, isDeleted=False)
    return render(re, 'admingallery.html', {'data': data})


# Notification views
@user_required
def markasseen(re, id):
    user = Petuser.objects.get(username=re.session['id'], isDeleted=False)
    unseen_notifications = UserNotification.objects.filter(user=user, seen=False, notification_id=id, isDeleted=False)
    for notification in unseen_notifications:
        notification.seen = True
        notification.save()
    return redirect(userhome)

def markallseen(re):
    if 'id' in re.session:
        user = Petuser.objects.get(username=re.session['id'], isDeleted=False)
        updated = UserNotification.objects.filter(user=user, seen=False, isDeleted=False).update(seen=True)
        return JsonResponse({'success': True, 'message': f'{updated} notification(s) marked as read'})
    if 'id1' in re.session:
        shop = Petshop.objects.get(username=re.session['id1'], isDeleted=False)
        updated = ShopNotification.objects.filter(shop=shop, seen=False, isDeleted=False).update(seen=True)
        return JsonResponse({'success': True, 'message': f'{updated} notification(s) marked as read'})
    return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=401)


# Photo management
@user_or_shop_required
def addphotos(re):
    if re.method == 'POST':
        category = re.POST['g1']
        breed = re.POST['g2']
        image = re.FILES['image']
        Gallery.objects.create(category=category, breed=breed, image=image)
        messages.info(re, 'Once admin accepts your photo it will show on gallery')
        return redirect(gallery)
    return redirect(addphotos)

@admin_required
def photoreq(re):
    data = Gallery.objects.filter(accept=False, isDeleted=False)
    return render(re, 'photoreq.html', {'data': data})

@admin_required
def acceptphoto(re, id):
    Gallery.objects.filter(pk=id).update(accept=True)
    return redirect(photoreq)

@admin_required
def deletePhoto(re, id):
    Gallery.objects.filter(pk=id).update(isDeleted=True)
    return redirect(photoreq)


# Reviews
@user_required
def addreviews(re):
    if re.method == 'POST':
        review = re.POST['feedback']
        user = Petuser.objects.get(username=re.session['id'], isDeleted=False)
        Reviews.objects.create(user=user, review=review)
        messages.success(re, 'Review Added Successfully')
        return redirect(userhome)
    return render(re, 'index.html')

@admin_required
def review(re):
    data = Reviews.objects.filter(isDeleted=False).all()
    return render(re, 'review.html', {'data': data})


# Profile management
@user_required
def editprofile(re):
    data = Petuser.objects.get(username=re.session['id'], isDeleted=False)
    return render(re, 'editprofile.html', {'data': data})

@shop_required
def editshopprofile(re):
    data = Petshop.objects.get(username=re.session['id1'], isDeleted=False)
    return render(re, 'editshopprofile.html', {'data': data})

@user_required
def updateuspf(re):
    if re.method == 'POST':
        uname = re.session['id']
        name = re.POST['us1']
        phone = re.POST['us2']
        email = re.POST['us3']
        username = re.POST['us4']
        password = re.POST['us5']
        user = Petuser.objects.get(username=uname)
        user.name = name
        user.phone = phone
        user.email = email
        user.username = username
        if password:
            user.set_password(password)
        user.save()
        re.session['id'] = username
        re.session.modified = True
        messages.success(re, 'Profile Updated')
        return redirect(editprofile)
    return render(re, 'editprofile.html')

@shop_required
def updatesppf(re):
    if re.method == 'POST':
        uname = re.session['id1']
        petshopname = re.POST['pts1']
        ownername = re.POST['pts2']
        adress = re.POST['pts3']
        phone = re.POST['pts4']
        email = re.POST['pts5']
        username = re.POST['pts6']
        password = re.POST['pts7']
        shop = Petshop.objects.get(username=uname)
        shop.shopname = petshopname
        shop.ownername = ownername
        shop.adress = adress
        shop.phone = phone
        shop.email = email
        shop.username = username
        if password:
            shop.set_password(password)
        shop.save()
        re.session['id1'] = username
        re.session.modified = True
        messages.success(re, 'Profile Updated')
        return redirect(editshopprofile)
    return render(re, 'editshopprofile.html')


# Shopping views
@user_required
def shopping(re):
    user = Petuser.objects.get(username=re.session['id'], isDeleted=False)
    shops = Petshop.objects.filter(suspense=False, isDeleted=False)
    for shop in shops:
        shop.product_count = Product.objects.filter(shop=shop, isDeleted=False).count()
        shop.service_count = Services.objects.filter(shop=shop, isDeleted=False).count()
    cart_product_ids = Cart.objects.filter(user=user, isDeleted=False).values_list('product__id', flat=True)
    data2 = Cart.objects.filter(user=user, isDeleted=False).count()
    return render(re, 'shop.html', {'shops': shops, 'cart_product_ids': cart_product_ids, 'data2': data2})

@user_required
def shopdetail(re, id):
    user = Petuser.objects.get(username=re.session['id'], isDeleted=False)
    shop = get_object_or_404(Petshop, pk=id)
    products = Product.objects.filter(shop=shop, isDeleted=False)
    services = Services.objects.filter(shop=shop, isDeleted=False)
    cart_product_ids = Cart.objects.filter(user=user, isDeleted=False).values_list('product__id', flat=True)
    return render(re, 'shopdetail.html', {
        'shop': shop,
        'products': products,
        'services': services,
        'cart_product_ids': cart_product_ids,
    })

@user_required
def book_service(re):
    if re.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)
    user = Petuser.objects.get(username=re.session['id'], isDeleted=False)
    service_id = re.POST.get('service_id')
    booking_date = re.POST.get('booking_date')
    booking_slot = re.POST.get('booking_slot')
    pet_name = re.POST.get('pet_name')
    pet_type = re.POST.get('pet_type')
    notes = re.POST.get('notes', '')
    service = get_object_or_404(Services, pk=service_id)
    if ServiceBooking.objects.filter(service=service, booking_date=booking_date, booking_slot__iexact=booking_slot, isDeleted=False).exists():
        return JsonResponse({'success': False, 'error': 'This slot is already booked. Please choose another.'})
    booking = ServiceBooking.objects.create(
        user=user, service=service, pet_name=pet_name, pet_type=pet_type,
        booking_date=booking_date, booking_slot=booking_slot, notes=notes, status='confirmed'
    )
    notification = Notification.objects.create(
        shop=service.shop,
        message=f"New booking for {service.servicename} by {user.name} for {pet_name} on {booking_date} at {booking_slot}",
        sender_name=user.name
    )
    ShopNotification.objects.get_or_create(shop=service.shop, notification=notification)
    return JsonResponse({'success': True, 'message': 'Service booked successfully!'})

@user_required
def services(re):
    data = Services.objects.filter(isDeleted=False).all()
    return render(re, 'servicesdetail.html', {'data': data})

@user_required
def all_products(re):
    user = Petuser.objects.get(username=re.session['id'], isDeleted=False)
    products = Product.objects.filter(isDeleted=False)
    cart_product_ids = Cart.objects.filter(user=user, isDeleted=False).values_list('product__id', flat=True)
    return render(re, 'allproducts.html', {'products': products, 'cart_product_ids': cart_product_ids})

@user_required
def all_services(re):
    user = Petuser.objects.get(username=re.session['id'], isDeleted=False)
    services = Services.objects.filter(isDeleted=False).all()
    return render(re, 'allservices.html', {'services': services})

@user_required
def bookservice(re, id):
    data = Services.objects.get(pk=id)
    selected_date = re.GET.get('booking_date', datetime.date.today().isoformat())
    booked = list(
        ServiceBooking.objects
        .filter(service=data, booking_date=selected_date, isDeleted=False)
        .values_list('booking_slot', flat=True)
    )
    return render(re, 'servicebooking.html', {
        'data': data,
        'booked_slots': booked,
        'booked_slots_json': json.dumps(booked),
        'selected_date': selected_date,
        'today': datetime.date.today().isoformat(),
    })

@user_required
def get_booked_slots(re, id):
    service = get_object_or_404(Services, pk=id)
    date = re.GET.get('date', datetime.date.today().isoformat())
    booked = list(
        ServiceBooking.objects
        .filter(service=service, booking_date=date, isDeleted=False)
        .values_list('booking_slot', flat=True)
    )
    return JsonResponse({'booked_slots': booked})


# Shop product/service management
@shop_required
def addproducts(re):
    petshop = Petshop.objects.get(username=re.session['id1'], isDeleted=False)
    if re.method == 'POST':
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
    return render(re, 'products.html')

@shop_required
def shopproducts(re):
    page = int(re.GET.get('page', 1))
    shop = Petshop.objects.get(username=re.session['id1'], isDeleted=False)
    products = Product.objects.filter(shop=shop, isDeleted=False).order_by('-id')
    search = re.GET.get('search', '')
    cat_filter = re.GET.get('category', '')
    if search:
        products = products.filter(prodname__icontains=search)
    if cat_filter:
        products = products.filter(category=cat_filter)
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

@shop_required
def addservices(re):
    petshop = Petshop.objects.get(username=re.session['id1'], isDeleted=False)
    if re.method == 'POST':
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

@shop_required
def shopservices(re):
    page = int(re.GET.get('page', 1))
    shop = Petshop.objects.get(username=re.session['id1'], isDeleted=False)
    services = Services.objects.filter(shop=shop, isDeleted=False).order_by('-id')
    search = re.GET.get('search', '')
    if search:
        services = services.filter(servicename__icontains=search)
    paginator = Paginator(services, 10)
    try:
        services_page = paginator.page(page)
    except:
        services_page = paginator.page(1)
    return render(re, 'shopservices.html', {'data1': services_page, 'search': search})

@shop_required
def editproducts(re, id):
    return redirect(shopproducts)

@shop_required
def editserv(re, id):
    return redirect(shopservices)

@shop_required
def updateproduct(re, id):
    if re.method == 'POST':
        price = re.POST.get('g2') or re.POST.get('price', '')
        quantity = re.POST.get('g3') or re.POST.get('qty', '')
        pettype = re.POST.get('pettype', 'All Pets')
        description = re.POST.get('description', '')
        Product.objects.filter(pk=id).update(price=price, qty=quantity, pettype=pettype, description=description)
        messages.success(re, 'Product Updated Successfully!')
        return redirect(shopproducts)
    return redirect(shopproducts)

@shop_required
def updateserv(re, id):
    if re.method == 'POST':
        price = re.POST.get('g2') or re.POST.get('price', '')
        desc = re.POST.get('g3') or re.POST.get('desc', '')
        duration = re.POST.get('duration', '')
        Services.objects.filter(pk=id).update(price=price, desc=desc, duration=duration)
        messages.success(re, 'Service Updated Successfully!')
        return redirect(shopservices)
    return redirect(shopservices)

@shop_required
def deleteprod(re, id):
    Product.objects.filter(pk=id).update(isDeleted=True)
    messages.success(re, 'Successfully Deleted')
    return redirect(shopproducts)

@shop_required
def deleteserv(re, id):
    Services.objects.filter(pk=id).update(isDeleted=True)
    messages.success(re, 'Successfully Deleted')
    return redirect(shopservices)


# Cart views
@user_required
def addtocart(re, id):
    user = Petuser.objects.get(username=re.session['id'], isDeleted=False)
    product = Product.objects.get(pk=id)
    existing = Cart.objects.filter(user=user, product=product, isDeleted=False).first()
    if existing:
        existing.quantity += 1
        existing.total_price = existing.quantity * existing.product.price
        existing.save()
        messages.success(re, f'Updated {product.prodname} quantity to {existing.quantity} in cart')
    else:
        Cart.objects.create(user=user, product=product, quantity=1, total_price=product.price)
        messages.success(re, 'Item Added to Cart')
    return redirect(shopping)

@user_required
def cart(re):
    user = Petuser.objects.get(username=re.session['id'], isDeleted=False)
    data = Cart.objects.filter(user=user, isDeleted=False)
    data1 = data.count()
    total = sum(i.product.price * i.quantity for i in data)
    return render(re, 'cart.html', {'data': data, 'data1': data1, 'total': total})

@user_required
def increment_quantity(re, id):
    cart_item = Cart.objects.get(pk=id)
    if cart_item.product.qty > 1:
        cart_item.quantity += 1
        cart_item.total_price = cart_item.quantity * cart_item.product.price
        cart_item.save()
    return redirect(cart)

@user_required
def decrement_quantity(re, id):
    cart_item = Cart.objects.get(pk=id)
    if cart_item.product.qty > 1:
        cart_item.quantity -= 1
        cart_item.total_price = cart_item.quantity * cart_item.product.price
        cart_item.save()
    return redirect(cart)

@user_required
def dltcartitm(re, id):
    Cart.objects.filter(pk=id).update(isDeleted=True)
    messages.info(re, 'Item removed')
    return redirect(cart)


# Order views
@user_required
def placeorder(re):
    user = Petuser.objects.get(username=re.session['id'], isDeleted=False)
    items = Cart.objects.filter(user=user, isDeleted=False)
    total = sum(i.product.price * i.quantity for i in items)
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
        'unread_count': UserNotification.objects.filter(user=user, seen=False, isDeleted=False).count(),
        'notifications': UserNotification.objects.filter(user=user, seen=False, isDeleted=False)
    })

@user_required
def success(re):
    user = Petuser.objects.get(username=re.session['id'], isDeleted=False)
    items = Cart.objects.filter(user=user, isDeleted=False)
    a = datetime.datetime.now().strftime("%Y-%m-%d")
    delivery_address = re.POST.get('delivery_address', '')
    for i in items:
        item = Product.objects.get(pk=i.product.pk)
        Bookings.objects.create(user_details=user, item_details=item, quantity=i.quantity, total_price=i.total_price, date=a, delivery_address=delivery_address)
        item.qty = item.qty - i.quantity
        item.save()
    Cart.objects.filter(user=user, isDeleted=False).update(isDeleted=True)
    messages.success(re, 'All cart items are booked')
    return redirect(shopping)

@user_required
def userorders(re):
    user = Petuser.objects.get(username=re.session['id'], isDeleted=False)
    product_orders = Bookings.objects.filter(user_details=user, isDeleted=False).order_by('-id')
    service_bookings = ServiceBooking.objects.filter(user=user, isDeleted=False).order_by('-id')
    active_count = (
        product_orders.exclude(status__in=['delivered', 'cancelled']).count() +
        service_bookings.exclude(status__in=['completed', 'cancelled']).count()
    )
    return render(re, 'userorders.html', {
        'product_orders': product_orders,
        'service_bookings': service_bookings,
        'active_count': active_count,
    })

@shop_required
def shoporders(re, id):
    products = Product.objects.get(pk=id)
    bookings = Bookings.objects.filter(item_details=products, isDeleted=False)
    return render(re, 'shoporders.html', {'bookings': bookings})

@shop_required
def shopallorders(re):
    page = int(re.GET.get('page', 1))
    shop = Petshop.objects.get(username=re.session['id1'], isDeleted=False)
    status_filter = re.GET.get('status', '')
    product_bookings = Bookings.objects.filter(item_details__shop=shop, isDeleted=False).select_related('user_details', 'item_details').order_by('-date')
    if status_filter:
        product_bookings = product_bookings.filter(status=status_filter)
    service_bookings = ServiceBooking.objects.filter(service__shop=shop, isDeleted=False).select_related('user', 'service').order_by('-created_at')
    if status_filter:
        service_bookings = service_bookings.filter(status=status_filter)
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
        'statuses': statuses,
        'service_statuses': service_statuses,
    })

@shop_required
def update_order_status(re, booking_id):
    shop = Petshop.objects.get(username=re.session['id1'], isDeleted=False)
    new_status = re.POST.get('status', '')
    if not new_status:
        return JsonResponse({'success': False, 'error': 'Status required'}, status=400)
    booking = Bookings.objects.filter(pk=booking_id, item_details__shop=shop, isDeleted=False).first()
    if booking:
        booking.status = new_status
        booking.save()
        return JsonResponse({'success': True, 'status': new_status})
    service_booking = ServiceBooking.objects.filter(pk=booking_id, service__shop=shop, isDeleted=False).first()
    if service_booking:
        service_booking.status = new_status
        service_booking.save()
        return JsonResponse({'success': True, 'status': new_status})
    return JsonResponse({'success': False, 'error': 'Not found'}, status=404)

@admin_required
def allorders(re):
    data = Bookings.objects.filter(isDeleted=False).order_by('-date')
    from_date = re.GET.get('from_date', '')
    to_date = re.GET.get('to_date', '')
    shop_search = re.GET.get('shop_search', '').strip()
    if from_date:
        data = data.filter(date__gte=from_date)
    if to_date:
        data = data.filter(date__lte=to_date)
    if shop_search:
        data = data.filter(item_details__shop__shopname__icontains=shop_search)
    paginator = Paginator(data, 8)
    page_number = re.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(re, 'orders.html', {
        'data': page_obj,
        'total_count': data.count(),
        'pending_count': Bookings.objects.filter(isDeleted=False, status='pending').count(),
        'shipped_count': Bookings.objects.filter(isDeleted=False, status__in=['dispatched', 'shipped', 'out_for_delivery']).count(),
        'delivered_count': Bookings.objects.filter(isDeleted=False, status='delivered').count(),
        'from_date': from_date,
        'to_date': to_date,
        'shop_search': shop_search,
    })

@user_required
def singleplaceorder(re, id):
    user = Petuser.objects.get(username=re.session['id'], isDeleted=False)
    items = Product.objects.filter(pk=id)
    for item in items:
        if item.qty == 0:
            messages.info(re, f'Stock Limit Exceeded for {item.prodname}')
            return redirect(shopping)
    return render(re, 'shop.html')

@user_required
def singlesuccess(re, id):
    user = Petuser.objects.get(username=re.session['id'], isDeleted=False)
    product = Product.objects.get(pk=id)
    total = product.price
    return render(re, 'single_checkout.html', {'product': product, 'total': total, 'user': user})

@user_required
def confirm_single_order(re):
    user = Petuser.objects.get(username=re.session['id'], isDeleted=False)
    product_id = re.POST.get('product_id')
    delivery_address = re.POST.get('delivery_address', '')
    product = Product.objects.get(pk=product_id)
    total = product.price
    a = datetime.datetime.now().strftime("%Y-%m-%d")
    Bookings.objects.create(user_details=user, item_details=product, quantity=1, total_price=total, date=a, delivery_address=delivery_address)
    product.qty = product.qty - 1
    product.save()
    messages.success(re, 'Successfully Ordered')
    return redirect(shopping)
