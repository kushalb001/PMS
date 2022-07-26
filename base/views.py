import re
from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from .forms import AddressForm, CForm, CustomerForm,PForm,CovidForm
from datetime import date,timedelta

from .models import Address, Customer, Medicine,Category,Order,OrderItem,Covid, Prescription
# Create your views here.
def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method =='POST':
        username=request.POST.get('username').lower()
        password=request.POST.get('password')

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,"user does not exist")

        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username or password does not exist')
    context={'page':page}
    return render(request,'base/login.html',context)

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')

def layout(request):
    return render(request,'base/layout.html')

@login_required(login_url='login')
def home(request):
    return render(request,'base/home.html')

@login_required(login_url='login')
def billing(request,ck):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    medicines=Medicine.objects.filter((Q(category__name__icontains=q)| Q(name__icontains=q)| Q(description__icontains=q))&Q(quantity__gt=0))
    categories=Category.objects.all()

    context={"categories":categories,"medicines":medicines,"ck":ck}

    return render(request,'base/billing.html',context)





@login_required(login_url='login')
def add_to_cart(request,pk,ck):
    
    item = get_object_or_404(Medicine, id=pk)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        customer=Customer.objects.get(phno=ck),
        ordered=False
    )
    order_qs = Order.objects.filter(customer=Customer.objects.get(phno=ck), ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id,customer=Customer.objects.get(phno=ck)).exists():
            if(order_item.item.quantity>order_item.quantity):
                order_item.quantity += 1
                order_item.item.quantity-=1
                order_item.item.save()

            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect('cart',ck=ck)
        else:
            order.items.add(order_item)
            order_item.item.quantity-=1
            order_item.item.save()
            messages.info(request, "This item was added to your cart.")
            return redirect('billing',ck=ck)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date,customer=Customer.objects.get(phno=ck))
        order.items.add(order_item)
        order_item.item.quantity-=1
        order_item.item.save()
        messages.info(request, "This item was added to your cart.")
        return redirect('billing',ck=ck)

@login_required(login_url='login')
def order_summary(request,ck):
    try:
        order = Order.objects.get(user=request.user, ordered=False,customer=Customer.objects.get(phno=ck))
    except:
        return redirect('home')
    ali=0
    items=OrderItem.objects.filter(order=order)
    for each_item in items:
        if each_item.item.ali==True:
            ali=1

    context = {'object': order,'ck':ck,'ali':ali}
    return render(request,'base/cart.html',context)

@login_required(login_url='login')
def checkout(request,ck,ali):
    if ali==1:
        customer=Customer.objects.get(phno=ck)
        form=AddressForm()
        if request.method == 'POST':
            form = AddressForm(request.POST)
            if form.is_valid():
                a=form.save(commit=False)
                
                a.save()
                customer.address=a
                customer.save()
                return redirect('checkout2',ck=ck)

        return render(request,"base/covid_form.html",{'form': form,'ck':ck})
    else:
        order = Order.objects.get(user=request.user, ordered=False,customer=Customer.objects.get(phno=ck))
        customer=Customer.objects.get(phno=ck)
        form=PForm()
        if request.method == 'POST':
            form = PForm(request.POST, request.FILES)
            if form.is_valid():
                prescription=form.save(commit=False)
                prescription.order=order;
                prescription.save()
                return redirect('bill',ck=ck)
                
            

        return render(request,"base/checkout.html",{'form': form,'order':order,'ck':ck})



@login_required(login_url='login')
def c_form(request,ck):
    c=Customer.objects.get(phno=ck)
    try:
        co=Covid.objects.get(customer=c)
        form=CovidForm(instance=co)
        if request.method == 'POST':
        
        
            form=CovidForm(request.POST,instance=co)
            if form.is_valid:
                form.save()
            return redirect('checkout',ck=ck,ali=0)
    except:
        form=CovidForm()

        if request.method == 'POST':
        
        
            form=CovidForm(request.POST)
            if form.is_valid:
                covid=form.save(commit=False)
                covid.customer=c
                covid.save()
            return redirect('checkout',ck=ck,ali=0)
        


    return render(request,"base/cform.html",{'form': form,'ck':ck})



@login_required(login_url='login')
def remove_from_cart(request, pk,ck):
    item = get_object_or_404(Medicine, id=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False,
        customer=Customer.objects.get(phno=ck)
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id,customer=Customer.objects.get(phno=ck)).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                
                ordered=False,
                customer=Customer.objects.get(phno=ck)
            )[0]
            order_item.item.quantity+=order_item.quantity
            order_item.item.save()

            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("cart",ck=ck)
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("cart",ck=ck)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("cart",ck=ck)



@login_required(login_url='login')
def remove_single_item_from_cart(request, pk,ck):
    item = get_object_or_404(Medicine, id=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False,
        customer=Customer.objects.get(phno=ck)

    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id,customer=Customer.objects.get(phno=ck)).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                
                ordered=False,
                customer=Customer.objects.get(phno=ck)
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.item.quantity+=1
                order_item.item.save()

                order_item.save()
            else:
                order_item.item.quantity+=1
                order_item.item.save()
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("cart",ck=ck)
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("cart",ck=ck)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("cart",ck=ck)




@login_required(login_url='login')
def bill(request,ck):
    order = Order.objects.get(user=request.user, ordered=False,customer=Customer.objects.get(phno=ck))
    customer=Customer.objects.get(phno=ck)
    items=OrderItem.objects.filter(order=order)
    for each_item in items:
        each_item.ordered=True
        ###med.save()
        each_item.save()
    order.ordered=True
    order.save()
    context={'object':order,'customer':customer}
    return render(request,'base/bill.html',context)




@login_required(login_url='login')
def register(request):
    form=CForm()
    if request.method == 'POST':
            form = CForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()

                return redirect('home')

    return render(request,'base/register.html',{'form':form})





@login_required(login_url='login')
def billing1(request):
    if request.method=='POST':
        phno=request.POST.get('phno')
        try:
            customer=Customer.objects.get(phno=phno)
            return redirect('billing',ck=phno)
        except:
            return redirect('billing1')
    return render(request,'base/billing1.html')



@login_required(login_url='login')
def myorders(request):
    orders=Order.objects.filter(user=request.user,ordered=True)
    context={'orders':orders}
    return render(request,'base/my_orders.html',context)




@login_required(login_url='login')
def display_bill(request,id):
    order=Order.objects.get(id=id)
    customer=order.customer
    context={'object':order,'customer':customer}
    return render(request,'base/bill.html',context)



@login_required(login_url='login')
def customer_order(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    orders=Order.objects.filter((Q(customer__first_name__icontains=q)|Q(customer__phno__icontains=q))&(Q(ordered=True)))
    context={'orders':orders}
    return render(request,'base/customer_order.html',context)



@login_required(login_url='login')
def orderdetails(request,id):
    order=Order.objects.get(id=id)
    ps=Prescription.objects.filter(order=order)

    context={'ps':ps,'id':id}
    return render(request,'base/orderdetails.html',context)





def covid_data(request):
    c=True if request.GET.get('c')=='on' else None
    f=True if request.GET.get('f')=='on' else None
    b=True if request.GET.get('b')=='on' else None
    co=True if request.GET.get('co')=='on' else None
    z=request.GET.get('z') if request.GET.get('z')!=None else ''
    from_date= date.today()
    t=timedelta(days=15)
    to_date=from_date-t
    cs=Covid.objects.filter(((Q(start_date__gte=to_date)&Q(start_date__lte=from_date))&Q(cold=c)&Q(customer__address__zip__icontains=z))|((Q(start_date__gte=to_date)&Q(start_date__lte=from_date))&Q(fever=f)&Q(customer__address__zip__icontains=z))|((Q(start_date__gte=to_date)&Q(start_date__lte=from_date))&Q(breathing_difficulty=b)&Q(customer__address__zip__icontains=z))|((Q(start_date__gte=to_date)&Q(start_date__lte=from_date))&Q(comorbid=co)&Q(customer__address__zip__icontains=z)))
    #cs=Covid.objects.all()
    context={'cs':cs}
    return render(request,'base/covid_data.html',context)

def projectname(request):
    return render(request,'base/projectname.html')