from django.shortcuts import render,redirect
from  django.views.generic import ListView,FormView
from  django.views.generic import CreateView,DetailView,UpdateView,DeleteView
from django.urls import reverse_lazy
from .models import Task
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date

# Create your views here.
class customLogin(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authentic_user = True

    def get_success_url(self):
        return reverse_lazy('taskList')

class register(FormView):
    template_name = "register.html"
    form_class = UserCreationForm
    redirect_authentic_user = True
    success_url = reverse_lazy('taskList') # like redirect

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request,user)            
        return super(register,self).form_valid(form)
    
    def get(self,*args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('taskList')
        return super(register,self).get(*args, **kwargs) 
        
class taskList(LoginRequiredMixin,ListView):
    model = Task    # displaying a list of Task model instances.
                    # Django will automatically query Task.objects.all() unless overridden.
    context_object_name = 'tasks' # access the list of tasks using the variable tasks.                                     
    template_name = 'tasklist.html'
    
    # This method is overridden to customize the data passed to the template.
    def get_context_data(self, **kwargs): # **kwargs allows accepting additional keyword arguments passed by the superclass.
        # Call the base implementation first to get a context 
        context = super().get_context_data(**kwargs)
        # add users given task as a list
        context['tasks'] = context['tasks'].filter(user = self.request.user)
        # retrive search area given input through GET
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            # match search input with title and add into tasks list
            context['tasks'] = context['tasks'].filter(title__contains = search_input)
        context['search_input'] = search_input
        context['today_date'] = date.today()
        return context

class taskCreate(LoginRequiredMixin,CreateView):
    model = Task 
    fields = ['title','description','due_date','completed']
    template_name = 'taskCreate.html'
    success_url = reverse_lazy('taskList')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(taskCreate,self).form_valid(form)

class taskDetail(LoginRequiredMixin,DetailView):
    model = Task 
    context_object_name = 'task'
    template_name = 'task.html'

class taskUpdate(LoginRequiredMixin,UpdateView):
    model = Task 
    fields = ['title','description','due_date','completed']
    template_name = "taskUpdate.html"
    success_url = reverse_lazy('taskList')

class taskDelete(LoginRequiredMixin,DeleteView):
    model = Task 
    fields = ['title','description','due_date','completed']
    template_name = "taskConfirmDelete.html"
    success_url = reverse_lazy('taskList')

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)
