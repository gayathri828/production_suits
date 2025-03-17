from django.shortcuts import render,redirect,reverse
from .ml_model import predict_suit  # Import the predict_suit function from ml_model.py in the suits app
from .models import SuitCustomization, Customer, SuitOrder  # Assuming you have a model for storing customer orders
from .forms import UserRegistrationForm, CustomerDetailsForm
from django.contrib.auth import login,authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


# View to display the form where the customer selects suit attributes
def suit_customization(request):
    if request.method == 'POST':
        # Get the selected features from the form
        fireproof = 1 if request.POST.get('fireproof') == 'on' else 0
        waterproof = 1 if request.POST.get('waterproof') == 'on' else 0
        gas_resistance = 1 if request.POST.get('gas_resistance') == 'on' else 0
        chemical_resistance = 1 if request.POST.get('chemical_resistance') == 'on' else 0
        germ_resistance = 1 if request.POST.get('germ_resistance') == 'on' else 0
        bulletproof = 1 if request.POST.get('bulletproof') == 'on' else 0

        # Create a list of the features (this is what will be passed to the ML model)
        features = [fireproof, waterproof, gas_resistance, chemical_resistance, germ_resistance, bulletproof]

        # Use the ML model to predict the suit name
        predicted_suit_name = predict_suit(features)

        # Retrieve or create the customer (Assume customer is logged in or exists in the session)
        try:
            customer = Customer.objects.get(user=request.user.id)
        except Customer.DoesNotExist:
            # Create a new Customer if one does not exist
            customer = Customer.objects.create(user=request.user.id,
                                               first_name=request.user.first_name,
                                               last_name=request.user.last_name,
                                               email=request.user.email)
            customer.save()
        # Create a SuitCustomization instance with the customer and their selected features
        suit_customization = SuitCustomization(
            customer=customer,
            fireproof=fireproof,
            waterproof=waterproof,
            gas_resistance=gas_resistance,
            chemical_resistance=chemical_resistance,
            germ_resistance=germ_resistance,
            bulletproof=bulletproof,
            suit_name=predicted_suit_name
        )
        suit_customization.save()  # Save the customization

        # Calculate price
        total_price = suit_customization.calculate_price()

        # Create the order and associate with the customization
        suit_order = SuitOrder(
            customer=customer,
            suit_customization=suit_customization,
            total_price=total_price
        )
        suit_order.save()
        context = {
            'predicted_suit_name': predicted_suit_name,
            'features': {
                'fireproof': fireproof,
                'waterproof': waterproof,
                'gas_resistance': gas_resistance,
                'chemical_resistance': chemical_resistance,
                'germ_resistance': germ_resistance,
                'bulletproof': bulletproof
            },
            'total_price': total_price
        }
        return render(request,'suit_result.html',context) # Assuming 'order_confirmation' is the name of the URL for confirmation page

    # If GET request, render the form
    return render(request, 'suit_customization.html')


# Optional: API endpoint to handle customer orders asynchronously (for example, for AJAX requests)
def place_order(request):
    if request.method == 'POST':
        fireproof = 1 if request.POST.get('fireproof') == 'on' else 0
        waterproof = 1 if request.POST.get('waterproof') == 'on' else 0
        gas_resistance = 1 if request.POST.get('gas_resistance') == 'on' else 0
        chemical_resistance = 1 if request.POST.get('chemical_resistance') == 'on' else 0
        germ_resistance = 1 if request.POST.get('germ_resistance') == 'on' else 0
        bulletproof = 1 if request.POST.get('bulletproof') == 'on' else 0

        # Create feature array for prediction
        features = [fireproof, waterproof, gas_resistance, chemical_resistance, germ_resistance, bulletproof]

        # Use the ML model to predict the suit
        predicted_suit_name = predict_suit(features)

        # Optionally, save the order to the database
        customer = Customer.objects.get(id=request.user.id)
        suit_customization = SuitCustomization(
            customer=customer,
            fireproof=fireproof,
            waterproof=waterproof,
            gas_resistance=gas_resistance,
            chemical_resistance=chemical_resistance,
            germ_resistance=germ_resistance,
            bulletproof=bulletproof,
            suit_name=predicted_suit_name
        )
        suit_customization.save()

        # Calculate the price
        total_price = suit_customization.calculate_price()

        # Create an order
        suit_order = SuitOrder(
            customer=customer,
            suit_customization=suit_customization,
            total_price=total_price
        )
        suit_order.save()

        # Return a JSON response with the predicted suit name
        return redirect(reverse('order_confirmation'))
    return render(request,'order_confirmation.html')

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        customer_form = CustomerDetailsForm(request.POST)

        if user_form.is_valid() and customer_form.is_valid():
            # Create the User object
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            # Create the Customer object and link it to the user
            customer = customer_form.save(commit=False)
            customer.user = user  # Link the user to the customer
            customer.save()

            # Log the user in
            login(request, user)
            return redirect('suit_customization')  # Redirect to the suit customization page

    else:
        user_form = UserRegistrationForm()
        customer_form = CustomerDetailsForm()

    return render(request, 'register.html', {'user_form': user_form, 'customer_form': customer_form})

# user_login view - redirect after successful login
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('suit_customization')  # Change this to your desired redirect page after login
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})
from django.shortcuts import render, get_object_or_404
from .models import SuitOrder, Customer
@login_required
def order_confirmation(request):
    if request.method == 'GET':
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return render(request, 'order_confirmation.html', {'error': 'Please log in to view your order.'})

        # Fetch the customer linked to the logged-in user
        customer = get_object_or_404(Customer, user=request.user)

        # Get the latest order for the customer
        latest_order = SuitOrder.objects.filter(customer=customer).order_by('-order_date').first()

        # Handle case where no order exists
        if not latest_order:
            return render(request, 'order_confirmation.html', {'error': 'No recent orders found.'})

        # Prepare context for the template
        context = {
            'customer_name': f"{customer.first_name} {customer.last_name}",
            'customer_email': customer.email,
            'order_id': latest_order.id,
            'predicted_suit_name': latest_order.suit_customization.suit_name,
            'features': {
                'fireproof': latest_order.suit_customization.fireproof,
                'waterproof': latest_order.suit_customization.waterproof,
                'gas_resistance': latest_order.suit_customization.gas_resistance,
                'chemical_resistance': latest_order.suit_customization.chemical_resistance,
                'germ_resistance': latest_order.suit_customization.germ_resistance,
                'bulletproof': latest_order.suit_customization.bulletproof,
            },
            'total_price': latest_order.total_price,
            'order_date': latest_order.order_date,
            'order_status': latest_order.order_status,
        }
        return render(request, 'order_confirmation.html', context)

    # POST request (When the Confirm Order button is clicked)
    elif request.method == 'POST':
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return render(request, 'order_confirmation.html', {'error': 'Please log in to confirm your order.'})

        # Fetch the customer and the latest order
        customer = get_object_or_404(Customer, user=request.user)
        latest_order = SuitOrder.objects.filter(customer=customer).order_by('-order_date').first()

        # Handle case where no order exists
        if not latest_order:
            return render(request, 'order_confirmation.html', {'error': 'No recent orders found.'})

        # Update the order status to 'Confirmed'
        if latest_order.order_status == 'Pending':
            latest_order.order_status = 'Confirmed'
            latest_order.save()

            # Redirect to the same page to show updated status
            return redirect('order_confirmation')

        # In case the order is already confirmed, display a message (optional)
        return render(request, 'order_confirmation.html', {'message': 'Your order is already confirmed.'})