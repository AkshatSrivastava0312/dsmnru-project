from django.shortcuts import render
from app_users.forms import UserForm, UserProfileInfoForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from curriculum.models import Department
from .models import UserProfileInfo, Query
from django.views.generic import CreateView
from app_users.models import AboutUs,Contact

def user_login(request):
    objAbout = AboutUs.objects.all()[0]
    objContact = Contact.objects.all()
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT IS DEACTIVATED")
        else:
            return HttpResponse("Please use correct id and password")
            # return HttpResponseRedirect(reverse('register'))

    elif request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'app_users/login.html',{'aboutus':objAbout,'contactus':objContact})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


# Create your views here.
# def index(request):
#     return render(request,'app_users/index.html')

def register(request):
    objAbout = AboutUs.objects.all()[0]
    objContact = Contact.objects.all()

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            # user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)

    elif request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
        
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'app_users/registration.html',
                            {'registered':registered,
                             'user_form':user_form,
                             'profile_form':profile_form,'aboutus':objAbout,'contactus':objContact})

class HomeView(TemplateView):
    template_name = 'app_users/index.html'

    def get_context_data(self, **kwargs):
        objAbout = AboutUs.objects.all()[0]
        objContact = Contact.objects.all()
        context = super().get_context_data(**kwargs)
        departments = Department.objects.all()
        teachers = UserProfileInfo.objects.filter(user_type='teacher')
        context['departments'] = departments
        context['teachers'] = teachers
        context['aboutus'] = objAbout
        context['contactus'] = objContact
        return context

class ContactView(CreateView):
    model = Query
    fields = '__all__'
    template_name = 'app_users/contact.html'

    def get_context_data(self, **kwargs):
        objAbout = AboutUs.objects.all()[0]
        objContact = Contact.objects.all()
        context = super().get_context_data(**kwargs)
        context['aboutus'] = objAbout
        context['contactus'] = objContact
        return context
