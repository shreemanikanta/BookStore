from django.shortcuts import render, redirect
from front_end.utils import get_authorization_headers
import requests
from django.contrib import messages
from django.http import JsonResponse


def home_page(request):
    """
    Renders the home page and displays the available books.
    Render the home page or search results.

    If the request method is GET, fetch the home page data and render the
    'front_end/home_page.html' template with the home page data and the
    user's first name (if available in the session).

    If the request method is POST, search for products based on the 'search'
    parameter. Return the search results
    rendered using the 'front_end/search.html' template.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered search or home page template.
    """

    home_page_endpoint = "http://127.0.0.1:8002/e_store/home_page/"
    search_endpoint = "http://127.0.0.1:8002/e_store/search/"
    if request.method == "POST":
        search_params = {
            'search': request.POST['search'],
        }
        response = requests.get(search_endpoint, params=search_params)
        data = response.json()
        return render(request, 'front_end/search.html',
                          {'data': data})

    else:
        response = requests.get(home_page_endpoint)
        first_name = ""
        try:
            first_name = request.session['first_name']
        except:
            first_name = "Guest"
        data = response.json()
        return render(request, 'front_end/home_page.html',
                    {'data': data, 'first_name': first_name})


def book_details(request, id):
    """Renders the page for displaying the details of a book
        and adding it to the cart.

    Args:
        request: The HTTP request object.
        id (int): The ID of the book to display.

    Returns:
        If the request method is 'POST' and the book is successfully
        added to the cart, redirects to the cart page.
        If the request method is 'GET' and the book details are successfully
        retrieved, renders the 'book_details.html' template. If an error
        occurs, renders the 'home_page.html' template with an error message.
    """
    book_detail_endpoint = f"http://127.0.0.1:8002/e_store/book_detail/{id}/"
    add_to_cart_endpoint = "http://127.0.0.1:8002/e_store/add_book_to_cart/"
    if 'access_token' not in request.session:
        return redirect('front_end:login')
    if request.method == 'POST':
        headers = get_authorization_headers(request)
        data = {
            'book_id': request.POST['id'],
            'quantity': request.POST['quantity']
        }
        response = requests.post(add_to_cart_endpoint,
                                 data=data, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return redirect('front_end:cart')
        else:
            error_message = "Failed to add book to cart"
            return render(request, 'front_end/home_page.html',
                          {'message': error_message})

    else:
        headers = get_authorization_headers(request)
        response = requests.get(book_detail_endpoint, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return render(request, 'front_end/book_details.html',
                          {'data': data})
        else:
            return redirect('front_end:login')


def add_book(request):
    """
    If a GET request is received, the user is shown the page
    to add a book.
    """
    endpoint = "http://127.0.0.1:8002/e_store/add_book/"
    if 'access_token' not in request.session:
        return redirect('front_end:login')
    headers = get_authorization_headers(request)
    response = requests.get(endpoint, headers=headers)
    languages = response.json()
    return render(request, 'front_end/add_book.html', {'languages': languages})


def register(request):
    """
    Function to register a new account using POST method to the
    to the register endpoint. if the registration is successful,
    redirect to login page.
    if there is an error, display the error message on the registration page.
    """
    endpoint = "http://127.0.0.1:8002/account/register/"
    if request.method == 'POST':
        data = {
            'username': request.POST['username'],
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'email': request.POST['email'],
            'password': request.POST['password'],
            'role': request.POST['role']
        }
        response = requests.post(endpoint, data=data)
        if response.status_code == 201:
            message = response.json()
            return render(request, 'front_end/login.html',
                          {'success': message})
        else:
            error_message = response.json()
            return render(request, 'front_end/register.html',
                          {'error_message': error_message})
    else:
        response = requests.get(endpoint)
        roles = response.json()
        return render(request, 'front_end/register.html', {'roles': roles})


def login(request):
    """
    Log in the user by sending a POST request to the login endpoint with the
    provided credentials. If the request is successful, the user is redirected
    to the home page. If the request fails, the error message is rendered on
    the login page.
    """

    endpoint = "http://127.0.0.1:8002/account/login/"
    if request.method == 'POST':
        data = {
            'username': request.POST['username'],
            'password': request.POST['password']
        }
        response = requests.post(endpoint, data=data)
        if response.status_code == 200:
            data = response.json()
            messages.info(request, "You have successfully logged in.")
            first_name = data['first_name']
            refresh_token = data['tokens']['refresh']
            access_token = data['tokens']['access']
            role = data['role']
            request.session['refresh_token'] = refresh_token
            request.session['access_token'] = access_token
            request.session['first_name'] = first_name
            request.session['role'] = role
            return redirect('front_end:home_page')

        else:
            messages.info(request, "Invalid username or password.")
            error_message = response.json()['error']
            return render(request, 'front_end/login.html',
                          {'message': error_message})

    else:
        return render(request, 'front_end/login.html')


def logout(request):
    """
    Logout the user by sending a POST request to the logout endpoint with the
    token. If the request is successful, the user is redirected
    to the home page. If the request fails, the error message is rendered on
    the home page.
    """

    endpoint = "http://127.0.0.1:8002/account/logout/"
    headers = get_authorization_headers(request)

    response = requests.post(endpoint, headers=headers)
    if response.status_code == 200:
        data = response.json()
        messages.info(request, "You have successfully logged out.")
        try:
            del request.session['access_token']
        except KeyError:
            pass
        request.session['first_name'] = "Guest"
        return redirect("front_end:home_page")

    elif response.status_code == 403:
        return redirect("front_end:login")

    else:
        error_message = response.json()['error']
        return render(request, 'front_end/home_page.html',
                        {'error_message': error_message})


def cart(request):
    """
    View and manage the user's cart. If a delete request is received, the book
    with the specified ID is removed from the cart. If a GET request is
    received, the contents of the cart are displayed.
    """
    endpoint = 'http://127.0.0.1:8002/cart/cart_books/'
    if 'access_token' not in request.session:
        return redirect('front_end:login')
    headers = get_authorization_headers(request)
    if request.method == 'POST':
        data = {
            'book_id': request.POST['id']
        }
        response = requests.delete(endpoint, data=data, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return redirect('front_end:cart')
        else:
            data = response.json()
            return redirect('front_end:cart')

    else:
        response = requests.get(endpoint, headers=headers)
        dataset = response.json()
        return render(request, 'front_end/cart.html', {'dataset': dataset})


def invoice(request):
    """
    Generate an invoice for the user's cart and display it. If a POST request
    is received, the invoice is checked out and the user is redirected to their
    My orders page. If a GET request is received, the invoice is displayed.
    """
    endpoint = 'http://127.0.0.1:8002/cart/checkout/'
    headers = get_authorization_headers(request)
    if request.method == 'POST':
        response = requests.post(endpoint, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return redirect('front_end:my_orders')
        else:
            data = response.json()
            return redirect('front_end:invoice')

    else:
        response = requests.get(endpoint, headers=headers)
        dataset = response.json()
        return render(request, 'front_end/invoice.html', {'dataset': dataset})


def my_orders(request):
    """
    View the user's past orders.
    """
    endpoint = 'http://127.0.0.1:8002/cart/my_orders/'
    headers = get_authorization_headers(request)
    response = requests.get(endpoint, headers=headers)
    dataset = response.json()
    return render(request, 'front_end/my_orders.html', {'orders': dataset})


def session_token(request):
    access_token = request.session.get('access_token', None)
    if access_token:
        return JsonResponse({'access_token': access_token})
    else:
        return JsonResponse({'error': 'Access token not found'})
