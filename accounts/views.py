from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout


def login_view(request):
    login_form = AuthenticationForm(request, data=request.POST or None)
    for field in login_form.fields.values():
        existing = field.widget.attrs.get("class", "")
        field.widget.attrs["class"] = (existing + " form-control").strip()

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('products_list')
    return render(request, 'login.html', {'login_form': login_form})


def logout_view(request):
    logout(request)
    return redirect('login')
