def get_authorization_headers(request):
    access_token = request.session['access_token']
    headers = {'Authorization': f'Bearer {access_token}'}
    return headers
