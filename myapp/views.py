from .models import Vendor
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from .models import Vendor, PurchaseOrder
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate


from django.contrib.auth import authenticate
from django.contrib import messages
from django.shortcuts import render, redirect

from django.contrib import messages

# views.py
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import CustomUser


def dashboard(request):
    return render(request, 'dashboard.html')


def login_page(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            request.session['user_id'] = user.id
            return redirect('dashboard')  # Replace with your actual dashboard URL or view name
        else:
            messages.error(request, "Invalid Credentials!")

    return render(request, 'login_page.html', {'messages': messages.get_messages(request)})

# views.py
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import CustomUser

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')

        if CustomUser.objects.filter(username=username).exists() or CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Username or email is already taken.')
            return redirect('signup')

        user = CustomUser.objects.create_user(
            email=email,
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        if user is not None:
            # Authenticate the user after account creation
            authenticated_user = authenticate(request, username=email, password=password)

            if authenticated_user is not None:
                # Login the authenticated user
                login(request, authenticated_user)
                messages.success(request, 'Account created successfully. You are now logged in.')
                return redirect('add_vendor')  # Replace with your actual dashboard URL or view name
            else:
                # If authentication fails, show an error message
                messages.error(request, 'Failed to log in after account creation.')
                return redirect('signup')  # Redirect to the login page

        else:
            messages.error(request, 'Failed to create an account. Please try again.')
            return redirect('signup')

    return render(request, 'signup.html')

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse
from django.http import HttpResponseRedirect

def forgot(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # Check if the provided email exists in the User model
        if User.objects.filter(email=email).exists():
            # Send the password reset email
            # (You can customize this part based on your email sending logic)
            # For simplicity, we'll use Django's built-in PasswordResetView
            return PasswordResetView.as_view(
                success_url=reverse('password_reset_done'),
                template_name='password_reset_form.html',
                extra_context={'email': email}
            )(request)
        else:
            # If email doesn't exist, display an error message
            messages.error(request, 'Invalid email. Please enter a registered email address.')

    return render(request, 'forgot.html')


from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User

class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset_form.html'
    email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'

def add_vendor(request):
    if request.method == 'POST':
        # Get form data and save the vendor
        name = request.POST.get('name')
        contact_details = request.POST.get('contact_details')
        address = request.POST.get('address')
        vendor_code = request.POST.get('vendor_code')
        on_time_delivery_rate = float(request.POST.get('on_time_delivery_rate'))
        quality_rating_avg = float(request.POST.get('quality_rating_avg'))
        average_response_time = float(request.POST.get('average_response_time'))
        fulfillment_rate = float(request.POST.get('fulfillment_rate'))

        vendor = Vendor(
            name=name,
            contact_details=contact_details,
            address=address,
            vendor_code=vendor_code,
            on_time_delivery_rate=on_time_delivery_rate,
            quality_rating_avg=quality_rating_avg,
            average_response_time=average_response_time,
            fulfillment_rate=fulfillment_rate
        )
        vendor.save()

        # You can redirect to another page or display a success message here

    return render(request, 'add_vendor.html')


def add_vendor_details(request):
    if request.method == 'POST':
        # Retrieve form data from POST request
        po_number = request.POST.get('po_number')
        vendor_id = request.POST.get('vendor')
        order_date = request.POST.get('order_date')
        delivery_date = request.POST.get('delivery_date')
        items = request.POST.get('items')
        quantity = request.POST.get('quantity')
        status = request.POST.get('status')
        quality_rating = request.POST.get('quality_rating')
        issue_date = request.POST.get('issue_date')
        acknowledgment_date = request.POST.get('acknowledgment_date')

        # Create a PurchaseOrder instance and save it
        PurchaseOrder.objects.create(
            po_number=po_number,
            vendor_id=vendor_id,
            order_date=order_date,
            delivery_date=delivery_date,
            items=items,
            quantity=quantity,
            status=status,
            quality_rating=quality_rating,
            issue_date=issue_date,
            acknowledgment_date=acknowledgment_date
        )

        return redirect('vendor_list')  # Redirect to the vendor list page after successful form submission

    # Render the form for GET requests
    vendors = Vendor.objects.all()  # You may want to pass a list of vendors to populate the dropdown
    return render(request, 'add_vendor_details.html', {'vendors': vendors})



def vendor_list(request):
    vendors = Vendor.objects.all()
    return render(request, 'vendor_list.html', {'vendors': vendors})



def vendor_detail(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    return render(request, 'vendor_detail.html', {'vendor': vendor})

   
def delete_vendor(request, vendor_id):
    if request.method == 'POST':
        vendor = get_object_or_404(Vendor, id=vendor_id)
        vendor.delete()
        return redirect('vendor_list')
    else:
        return HttpResponseForbidden("Invalid request method for deleting a vendor.")
    


def vendor_detail(request, vendor_id):
    # Retrieve the vendor object based on the vendor_id
    vendor = get_object_or_404(Vendor, id=vendor_id)

    # Check if the form is submitted (POST request)
    if request.method == 'POST':
        # Update the vendor details with the submitted data
        vendor.name = request.POST.get('name')
        vendor.contact_details = request.POST.get('contact_details')
        vendor.address = request.POST.get('address')
        vendor.vendor_code = request.POST.get('vendor_code')
        vendor.on_time_delivery_rate = float(request.POST.get('on_time_delivery_rate'))
        vendor.quality_rating_avg = float(request.POST.get('quality_rating_avg'))
        vendor.average_response_time = float(request.POST.get('average_response_time'))
        vendor.fulfillment_rate = float(request.POST.get('fulfillment_rate'))

        # Save the updated vendor object
        vendor.save()

        # Redirect to the vendor list page after saving changes
        return redirect('vendor_list')

    # Render the vendor_detail.html template with the vendor object
    return render(request, 'vendor_detail.html', {'vendor': vendor})




@require_POST
def edit_vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)

    # Update vendor details based on the submitted form data
    vendor.name = request.POST.get('name')
    vendor.contact_details = request.POST.get('contact_details')
    vendor.address = request.POST.get('address')
    vendor.vendor_code = request.POST.get('vendor_code')
    vendor.on_time_delivery_rate = float(request.POST.get('on_time_delivery_rate'))
    vendor.quality_rating_avg = float(request.POST.get('quality_rating_avg'))
    vendor.average_response_time = float(request.POST.get('average_response_time'))
    vendor.fulfillment_rate = float(request.POST.get('fulfillment_rate'))
    vendor.save()

    return JsonResponse({'status': 'success'})



def vendor_order_list(request):
    orders = PurchaseOrder.objects.all()
    return render(request, 'vendor_order_list.html', {'PurchaseOrders': orders})


def vendor_order_detail(request, vendor_id):
    order = get_object_or_404(PurchaseOrder, id=vendor_id)
    return render(request, 'vendor_order_detail.html', {'order': order})


def edit_vendor_order(request, order_id):
    order = get_object_or_404(PurchaseOrder, id=order_id)

    if request.method == 'POST':
        # Update order details based on the submitted form data
        order.po_number = request.POST.get('po_number')
        order.order_date = request.POST.get('order_date')
        order.delivery_date = request.POST.get('delivery_date')
        order.items = request.POST.get('items')
        order.quantity = request.POST.get('quantity')
        order.status = request.POST.get('status')
        order.quality_rating = request.POST.get('quality_rating')
        order.issue_date = request.POST.get('issue_date')
        order.acknowledgment_date = request.POST.get('acknowledgment_date')

        # Save the updated order object
        order.save()

        return redirect('vendor_order_list')  # Redirect to the vendor_order_list page

    return render(request, 'edit_vendor_order.html', {'order': order})

def delete_vendor_order(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(PurchaseOrder, id=order_id)
        order.delete()
        return redirect('vendor_order_list')
    else:
        return HttpResponseForbidden("Invalid request method for deleting an order.")