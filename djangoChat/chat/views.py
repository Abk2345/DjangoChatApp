from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm

# home page
def frontpage(request):
    return render(request, 'chat/frontpage.html')

# signup submit
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        # valid form
        if form.is_valid():
            user = form.save()
            
            # login this user
            login(request, user)
            # redirect to home
            return redirect('frontpage')
    else:
        form = SignUpForm()

    # not signed up, be on same page
    return render(request, 'chat/signup.html', {'form': form})


