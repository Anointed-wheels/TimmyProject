from django.shortcuts import render, redirect
from django.contrib import messages
from users.models import PendingUser, CustomUser
from users.forms import RegistrationForm
import random, string
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from books.models import Book
from django.http import JsonResponse
from ai.chatbot import library_ai_response
from books.models import Book
from django.contrib.auth import get_user_model
from borrow.models import BorrowRecord
from django.utils.timezone import now
from django.contrib.auth import get_user_model



from .forms import LoginForm
from django.contrib.auth import get_user_model
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'users/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    return render(request, 'users/dashboard.html')


from django.shortcuts import render, redirect
from django.contrib import messages
from users.models import PendingUser, CustomUser
from users.forms import RegistrationForm
import random, string
from django.core.mail import send_mail
from django.conf import settings


def generate_otp():
    return ''.join(random.choices(string.digits, k=6))


def register_view(request):

    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data['email']

            # Check if user already exists
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email already registered.")
                return redirect('register')

            otp = generate_otp()

            # Delete old pending user if exists
            PendingUser.objects.filter(email=email).delete()

            # Create new pending user
            PendingUser.objects.create(
                username=form.cleaned_data['username'],
                email=email,
                password=form.cleaned_data['password'],
                otp=otp
            )

            # Send OTP email
            send_mail(
                'Digital Library OTP Verification',
                f'Your OTP is: {otp}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False
            )

            request.session['pending_email'] = email

            messages.success(request, "OTP sent to your email.")
            return redirect('verify_otp')

    else:
        form = RegistrationForm()

    return render(request, 'users/register.html', {'form': form})

def verify_otp_view(request):
    email = request.session.get('pending_email')
    if not email:
        messages.error(request, 'No registration in progress.')
        return redirect('register')

    pending = PendingUser.objects.filter(email=email).first()
    if not pending:
        messages.error(request, 'Pending user not found.')
        return redirect('register')

    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        if not pending.is_otp_valid():
            pending.delete()
            messages.error(request, 'OTP expired. Please register again.')
            return redirect('register')
        if otp_input != pending.otp:
            messages.error(request, 'Incorrect OTP. Try again.')
        else:
            # Save actual user
            user = CustomUser.objects.create_user(
                username=pending.username,
                email=pending.email,
                password=pending.password,  # will be hashed by create_user
                user_type='normal'
            )
            pending.delete()
            messages.success(request, 'Registration successful. You can now login.')
            return redirect('login')

    return render(request, 'users/verify_otp.html')



def ai_chat(request):

    message = request.GET.get("message")

    response = library_ai_response(message)

    return JsonResponse({"response": response})




def login_view(request):

    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            try:
                user_obj = CustomUser.objects.get(email=email)
                username = user_obj.username
            except CustomUser.DoesNotExist:
                return render(request,"users/login.html",{
                    "form":form,
                    "error":"Invalid email or password"
                })

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request,user)
                return redirect("dashboard")

            else:
                return render(request,"users/login.html",{
                    "form":form,
                    "error":"Invalid email or password"
                })

    return render(request,"users/login.html",{"form":form})


    from django.contrib.auth.decorators import login_required


User = get_user_model()
@login_required
def dashboard(request):

    user = request.user
    user_type = user.user_type

    total_books = Book.objects.count()
    total_users = CustomUser.objects.filter(is_deleted=False).count()
    suspended_users = CustomUser.objects.filter(is_suspended=True).count()

    borrowed_books = BorrowRecord.objects.filter(status="approved").count()

    overdue_books = BorrowRecord.objects.filter(
        status="approved",
        due_date__lt=timezone.now()
    ).count()

    context = {
        "user_type": user_type,
        "total_books": total_books,
        "total_users": total_users,
        "borrowed_books": borrowed_books,
        "overdue_books": overdue_books
    }

    return render(request,"users/dashboard.html",context)



User = get_user_model()

from django.db.models import Q

def manage_users(request):

    users = CustomUser.objects.all()

    # SEARCH
    query = request.GET.get("search")
    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query)
        )

    # FILTER
    status = request.GET.get("status")

    if status == "active":
        users = users.filter(is_suspended=False, is_deleted=False)

    elif status == "suspended":
        users = users.filter(is_suspended=True)

    elif status == "deleted":
        users = users.filter(is_deleted=True)

    return render(request, "users/manage_users.html", {
        "users": users
    })


@login_required
def delete_user(request, user_id):

    user = User.objects.get(id=user_id)

    user.is_deleted = True
    user.save()

    return redirect("manage_users")

@login_required
def suspend_user(request,user_id):

    user = User.objects.get(id=user_id)

    user.is_suspended = True
    user.save()

    send_mail(
        "Account Suspended",
        "Your account has been suspended",
        settings.DEFAULT_FROM_EMAIL,
        [user.email]
    )

    return redirect("manage_users")


@login_required
def activate_user(request,user_id):

    user = User.objects.get(id=user_id)

    user.is_suspended = False
    user.save()

    send_mail(
        "Account Activated",
        "Your account has been activated",
        settings.DEFAULT_FROM_EMAIL,
        [user.email]
    )

    return redirect("manage_users")

@login_required
def change_role(request,user_id):

    user = User.objects.get(id=user_id)

    if request.method == "POST":

        role = request.POST.get("role")

        user.user_type = role
        user.save()

    send_mail(
        "Account Role Changed",
        f"Your account role has been changed to {user.user_type}",
        settings.DEFAULT_FROM_EMAIL,
        [user.email]
    )

    return redirect("manage_users")


@login_required
def suspended_users(request):

    users = CustomUser.objects.filter(is_suspended=True)

    return render(request, "users/suspended_users.html", {"users": users})

@login_required
def delete_own_account(request):

    user = request.user
    user.is_deleted = True
    user.is_active = False
    user.save()

    logout(request)

    return redirect("homepage")