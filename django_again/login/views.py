from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import View, CreateView, DetailView, UpdateView, DeleteView, ListView
from django.contrib.auth.models import User
from .models import *
from django.urls import reverse_lazy
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class Home(View):
    def get(self, request):
        ctx = {
                'username_model': "",
                'username_request': ""
            }
        if(request.user.is_authenticated):
            username_from_req = request.user.username
            username = User.objects.get(username=request.user.username)
            ctx = {
                'username_model': username.username,
                'username_request': username_from_req
            }
            print(ctx)
        return render(request, template_name='login/home.html', context=ctx)



class CreateType(CreateView):
    model = ItemType
    fields = ['name']
    success_url = reverse_lazy('login:home')

class CreateCondition(CreateView):
    model = ItemCondition
    fields = ['name']
    success_url = reverse_lazy('login:home')

class ItemList(ListView):
    model = Item

class UpdateItem(UpdateView):
    model = Item
    fields = ['name', 'quantity', 'notes', 'item_type', 'condition']
    template_name_suffix = '_update'
    success_url = reverse_lazy('login:home')

class CreateItem(LoginRequiredMixin, CreateView):
    form_class = ItemForm
    template_name = 'login/item_form.html'
    success_url = reverse_lazy('login:create_item')

    def get_form_kwargs(self):
        kwargs = super(CreateItem, self).get_form_kwargs()
        kwargs['request'] = self.request

        return kwargs
    
class Register(CreateView):
    form_class = RegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login:create_item')

class ListItems(LoginRequiredMixin,ListView):
    model = Item

    def get_context_data(self, **kwargs):
        ctx = super(ListItems, self).get_context_data(**kwargs)
        ctx['choices_type'] = ItemType.objects.all()
        ctx['choices_condition'] = ItemCondition.objects.all()
        return ctx

    def get_queryset(self):
        qs = super(ListItems, self).get_queryset()

        filter_by = self.request.GET.get('category', '')
        if not filter_by == '':
            if filter_by == "type":
                qs = qs.filter(owner=self.request.user, item_type=ItemType.objects.get(name=self.request.GET.get('type_choice', "Switch")))
            elif filter_by == "condition":
                qs = qs.filter(owner=self.request.user, condition=ItemCondition.objects.get(name=self.request.GET.get('condition_choice', "New")))
            else:
                qs = qs.filter(owner=self.request.user )
        else:
            qs = qs.filter(owner=self.request.user )
        
        len(qs)
        return qs

class ItemDetail(DetailView):
    model = Item

    def get_context_data(self, **kwargs):
        ctx = super(ItemDetail, self).get_context_data(**kwargs)
        ctx['back'] = self.request.META.get('HTTP_REFERER')
        return ctx
    

class ListItemsJson(View):
    def get(self, request):

        ctx = {
            "choices_type": ItemType.objects.all(),
            "choices_condition": ItemCondition.objects.all(),
        }

        category = request.GET.get('category', '')
        filter_by = ''
        items = None
        if category == 'type':
            filter_by = request.GET.get('type_choice', '')
            items = Item.objects.filter(owner=request.user, item_type=ItemType.objects.get(name=filter_by))
        elif category == 'condition':
            filter_by = request.GET.get('condition_choice', '')
            items = Item.objects.filter(owner=request.user, condition=ItemCondition.objects.get(name=filter_by))
        else:
            items = Item.objects.filter(owner=request.user)
            print('now request', len(items))
        item_list = []

        

        if items: 
            for item in items:
                name = item.name.name
                id = item.pk

                item_dict = {
                    'name': name,
                    'id': id
                }

                item_list.append(item_dict)
            print(item_list)
        if not category == '':
            response = {
                'items': item_list,
            }
            return JsonResponse(response, safe=False)
        else:
            return render(request, 'login/item_list_json.html', context=ctx)

        

                
    
            
