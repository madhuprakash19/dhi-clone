from django.shortcuts import render,get_object_or_404
from django.views.generic import (TemplateView,DetailView,
                                CreateView,DetailView,
                                ListView,RedirectView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from accounts.models import UserProfileInfo
from user.models import CreateClass,ClassMember
from django.contrib import messages


class HomePage(LoginRequiredMixin,TemplateView):
    template_name = 'user/index.html'
    model = UserProfileInfo


class CreatClassView(LoginRequiredMixin,CreateView):
    fields=('sem','subject','subject_code')
    model = CreateClass
    context_object_name = 'class'
    template_name = 'user/class_form.html'
    success_url = '/user/class'

    def form_valid(self,form):
        classroom = form.save(commit=False)
        classroom.teacher = self.request.user
        classroom = classroom.save()
        return HttpResponseRedirect(self.success_url)

class SingleClass(LoginRequiredMixin,DetailView):
    model = CreateClass
    context_object_name = 'class'
    template_name = 'user/class_detail.html'

class ListClass(LoginRequiredMixin,ListView):
    model = CreateClass
    context_object_name = 'class'
    template_name = 'user/class_list.html'

class JoinClass(LoginRequiredMixin,RedirectView):

    def get_redirect_url(self,*args,**kwargs):
        return reverse('user:single_class',kwargs={'slug':self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):
        classroom = get_object_or_404(CreateClass,slug=self.kwargs.get('slug'))

        try:
            ClassMember.objects.create(user=self.request.user,class_group=classroom)
        except IntegrityError:
            messages.warning(self.request,'Warning already a student of the class!')
        else:
            messages.success(self.request,'You are now a student of this class!')

        return super().get(request,*args,**kwargs)

class LeaveClass(LoginRequiredMixin,RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return reverse('user:single_class',kwargs={'slug':self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):
        try:
            membership = ClassMember.objects.filter(
            user = self.request.user,
            class_group__slug = self.kwargs.get('slug')
            ).get()
        except ClassMember.DoesNotExist:
            messages.warning(self.request,'Sorry you are not in this class!')
        else:
            membership.delete()
            messages.success(self.request,'You hav left the class!')
        return super().get(request,*args,**kwargs)
