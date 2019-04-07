from django.shortcuts import render
from users.models import Profile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import operator
from itertools import chain
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

@login_required( login_url='/login' )
def home(request):
    query = request.GET.get('q', None)
    qs_user = User.objects.all()
    qs_profile = Profile.objects.all()
    context={}
    if query is not None and query is not "":
        qs_user = qs_user.filter(Q(first_name__contains=query) |
                       Q(last_name__contains=query) |
                       Q(email__contains=query)
        )
        qs_profile = qs_profile.filter(
                       Q(year__contains=query) |
                       Q(company__contains=query) |
                       Q(position__contains=query) |
                       Q(phone__contains=query) |
                       Q(major__contains=query)
        )

        context = {
            'users': qs_user,
            'profiles' : qs_profile
            }

    else:
        qs_user = qs_user.order_by('last_name', 'first_name')
        context = {
            'users': qs_user
            }

    return render( request, 'home/home.html', context)




class UserListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = '/home/'
    model = User
    context_object_name = 'users'
    template_name = 'home/home.html'
    ordering = ['last_name']
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query != "":
            qs_user = User.objects.all()
            qs_profile = Profile.objects.all()
            context={}
            if query is not None and query is not "":
                for term in query.split():
                    qs_user = qs_user.filter(Q(first_name__contains=term) |
                                   Q(last_name__contains=term) |
                                   Q(email__contains=term)
                    )
                    qs_profile = qs_profile.filter(
                                   Q(year__contains=term) |
                                   Q(company__contains=term) |
                                   Q(position__contains=term) |
                                   Q(phone__contains=term) |
                                   Q(major__contains=term)
                    )

                    context = {
                        'users': qs_user,
                        'profiles' : qs_profile
                        }

                return list(chain(qs_profile, qs_user))
            else:
                return User.objects.all().order_by('first_name')
        else:
            return User.objects.all().order_by('first_name')


        #return User.objects.filter(first_name__contains = 'jack') # or anything



class UserDetailView(LoginRequiredMixin,UserPassesTestMixin, DetailView):
    login_url = '/login/'
    redirect_field_name = '/home/'
    model = User
    template_name= "home/user_detail.html"

    def dispatch(self, request, *args, **kwargs):
        profile = self.get_object()
        if self.request.user.username == profile.username:
            return redirect('/profile/')
        else:
            return super(UserDetailView, self).dispatch(request, *args, **kwargs)


    def test_func(self):
        return True

def about(request):
    return render ( request, 'home/about.html')


def landing(request):
    return render(request, 'home/landing.html')


def contact(request):
    return render(request, 'home/contact.html')

def login(request):
    return render ( request, 'users/login.html')


# def profile(request):
#     args = {'user': request.user}
#     return render(request, 'users/home.html', args)

#
# def search( request):
#     template = 'home/home.html'
#     query = request.GET.get('q')
#     results = UserProfile.objects.filter(Q(name__icontains=query))
#     print('hello world')
#     return render_to_response( 'home/home.html')
