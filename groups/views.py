from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin
from django.contrib import messages
# Create your views here.
from django.urls import reverse
from django.views import generic
from groups.models import Group, GroupMember
from .forms import GroupForm

class CreateGroup(LoginRequiredMixin,generic.CreateView):
    model = Group
    form_class = GroupForm


class SingleGroup(generic.DetailView):
    model= Group


class ListGroup(generic.ListView):
    model= Group
    

class JoinGroup(LoginRequiredMixin, generic.RedirectView):
    
    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single', kwargs={'slug':self.kwargs.get('slug')})

    def get(self,request,*args,**kwrags):
        group = get_object_or_404(Group,slug=self.kwargs.get('slug'))


        try: 
            GroupMember.objects.create(user=self.request.user , group=group)

        except IntegrityError:
            messages.warning(self.request,('Warning alreday a member'))
        else:
             messages.success(self.request,('You are now a member '))
        
        return super().get(request,*args,**kwrags)


class LeaveGroup(LoginRequiredMixin,generic.RedirectView):
    
    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single', kwargs={'slug':self.kwargs.get('slug')})
    
    def get(self,request,*args,**kwrags):
        
        try: 
            membership = GroupMember.objects.filter(
                user= self.request.user,
                group__slug=self.kwargs.get('slug')
                ).get()
        except GroupMember.DoesNotExist:
            messages.warning(self.request,('Sorry you aren not in this group'))
        else:
            messages.success(self.request,('You have left the group !! '))
        
        return super().get(request,*args,**kwrags)