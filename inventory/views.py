
# Create your views here.

from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from django.contrib import messages
from django.shortcuts import render
from django.utils import timezone
from .models import Product, Sale, Purchase  # make sure your models exist
from .models import Product
from .forms import ProductForm
from django.db.models import Q
from django.db.models import Sum, F  # ✅ add this import at the top
from .models import Product, Sale
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Purchase
from .forms import PurchaseForm


def home_view(request):
    return render(request, 'inventory/home.html')

def about_view(request):
    return render(request, 'inventory/about.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'inventory/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'inventory/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    # Total products
    total_products = Product.objects.count()

    # Products with quantity less than 5 (low stock)
    low_stock_count = Product.objects.filter(quantity__lt=5).count()

    # Sales made today
    sales_today = Sale.objects.filter(date__date=timezone.now().date()).count()

    # Recent activities (replace with real logs or transactions)
    recent_activities = []
    latest_sales = Sale.objects.order_by('-date')[:3]
    latest_purchases = Purchase.objects.order_by('-date')[:3]

    for sale in latest_sales:
        recent_activities.append(f"Sale #{sale.id} of {sale.product.name} ({sale.quantity})")
    for purchase in latest_purchases:
        recent_activities.append(f"Purchase #{purchase.id} of {purchase.product.name} ({purchase.quantity})")

    return render(request, "inventory/dashboard.html", {
        "total_products": total_products,
        "low_stock_count": low_stock_count,
        "sales_today": sales_today,
        "recent_activities": recent_activities,
    })


# View all products with search/filter
def product_list(request):
    query = request.GET.get('q')
    products = Product.objects.all()
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(category__icontains=query) | 
            Q(supplier__icontains=query)
        )
    return render(request, 'inventory/product_list.html', {'products': products})

# Add a new product
def product_add(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'inventory/product_form.html', {'form': form})

# Edit/Update a product
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'inventory/product_form.html', {'form': form})

# Delete a product
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'inventory/product_confirm_delete.html', {'product': product})


# ---------------Sales--------------
@login_required
def sales_list(request):
    products = Product.objects.all()
    sales = Sale.objects.all().order_by('-date')
    return render(request, 'inventory/sales_list.html', {'products': products, 'sales': sales})

@login_required
def invoice(request):
    if request.method == "POST":
        items = request.POST.getlist('product')
        quantities = request.POST.getlist('quantity')
        sales = []
        total_amount = 0

        for i, product_id in enumerate(items):
            product = Product.objects.get(id=product_id)
            qty = int(quantities[i])
            total = product.price * qty
            total_amount += total

            # Save sale in database
            Sale.objects.create(
                product=product,
                quantity=qty,
                total_price=total,
                user=request.user
            )

            sales.append({
                'product': product,
                'quantity': qty,
                'total': total
            })
        # ✅ success notification 
        messages.success(request, " Sale recorded successfully!")
        
        context = {
            'sales': sales,
            'total_amount': total_amount
        }
        
        return render(request, 'inventory/invoice.html', context)

    return redirect('inventory/sales_list')

#-------------------Purchases_list --------------

@login_required
def purchases_list(request):
    if request.method == "POST":
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.purchased_by = request.user
            purchase.save()  # automatically updates product stock
            messages.success(request, "✅ Purchase submitted successfully!")
            return redirect('purchases_list')  # refresh page after adding

    else:
        form = PurchaseForm()

    purchases = Purchase.objects.all().order_by('-date')
    return render(request, 'inventory/purchases_list.html', {
        'purchases': purchases,
        'form': form
    })

@login_required
def reports(request):
    # Totals
    total_products = Product.objects.count()
    total_sales = Sale.objects.count()
    total_purchases = Purchase.objects.count()

    # Revenue from sales (quantity × product price)
    total_revenue = (
        Sale.objects.aggregate(
            total=Sum(F('quantity') * F('product__price'))
        )['total'] or 0
    )

    # Expenses from purchases (quantity × product price)
    total_expenses = (
        Purchase.objects.aggregate(
            total=Sum(F('quantity') * F('product__price'))
        )['total'] or 0
    )

    # Profit (Revenue - Expenses)
    total_profit = total_revenue - total_expenses

    # Top 5 selling products
    top_selling = (
        Sale.objects.values('product__name')
        .annotate(total_sold=Sum('quantity'))
        .order_by('-total_sold')[:5]
    )

    # Low stock products
    low_stock_products = Product.objects.filter(quantity__lt=5)

    # Recent activity logs
    recent_sales = Sale.objects.order_by('-date')[:5]
    recent_purchases = Purchase.objects.order_by('-date')[:5]
    
    context = {
        'total_products': total_products,
        'total_sales': total_sales,
        'total_purchases': total_purchases,
        'total_revenue': total_revenue,
        'total_expenses': total_expenses,
        'total_profit': total_profit,
        'top_selling': top_selling,
        'low_stock_products': low_stock_products,
        'recent_sales': recent_sales,
        'recent_purchases': recent_purchases,
    }
    return render(request, 'inventory/reports.html', context)
