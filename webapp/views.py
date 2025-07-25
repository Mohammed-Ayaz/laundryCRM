from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import Record
from django.contrib import messages

def home(request):
    return render(request, 'webapp/landing_page.html')



def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect("")

    context = {'form':form}
    return render(request, 'webapp/register.html', context=context)


def my_login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("dashboard")
    context = {'form':form}
    return render(request, 'webapp/my-login.html', context=context)





# - User logout

def user_logout(request):

    auth.logout(request)

    messages.success(request, "Logout success!")

    return redirect("")




from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Customer, Service, Order, Staff, Task
from .forms import CustomerForm, ServiceForm, OrderForm, OrderItemFormSet, StaffForm, TaskForm

class CustomerListView(ListView):
    model = Customer
    template_name = 'webapp/customers/customer_list.html'
    context_object_name = 'customers'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['export_url'] = reverse_lazy('export_customers_csv')
        return context


class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'webapp/customers/customer_detail.html'


class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'webapp/customers/customer_form.html'
    success_url = reverse_lazy('customer_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Customer created successfully!')
        return super().form_valid(form)

class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'webapp/customers/customer_form.html'
    success_url = reverse_lazy('customer_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Customer updated successfully!')
        return super().form_valid(form)

class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'webapp/customers/customer_confirm_delete.html'
    success_url = reverse_lazy('customer_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Customer deleted successfully!')
        return super().delete(request, *args, **kwargs)
    


class ServiceListView(ListView):
    model = Service
    template_name = 'webapp/services/service_list.html'
    context_object_name = 'services'


class ServiceCreateView(CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'webapp/services/service_form.html'
    success_url = reverse_lazy('service_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Service created successfully!')
        return super().form_valid(form)

class ServiceUpdateView(UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'webapp/services/service_form.html'
    success_url = reverse_lazy('service_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Service updated successfully!')
        return super().form_valid(form)


def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            order = form.save(commit=False)
            order.total_amount = 0
            order.save()
            instances = formset.save(commit=False)
            for instance in instances:
                instance.order = order
                instance.save()
                order.total_amount += instance.subtotal()
            
            order.save()
            messages.success(request, 'Order created successfully!')
            return redirect('order_detail', pk=order.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = OrderForm()
        formset = OrderItemFormSet()
    
    return render(request, 'webapp/orders/order_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Create New Order'
    })

def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        formset = OrderItemFormSet(request.POST, instance=order)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Order updated successfully!')
            return redirect('order_detail', pk=order.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = OrderForm(instance=order)
        formset = OrderItemFormSet(instance=order)
    return render(request, 'webapp/orders/order_form.html', {
        'form': form,
        'formset': formset
    })

def update_order_status(request, pk, status):
    order = get_object_or_404(Order, pk=pk)
    old_status = order.get_status_display()
    order.status = status
    order.save()
    messages.success(request, f'Order status changed from {old_status} to {order.get_status_display()}')
    return redirect('order_detail', pk=order.pk)

class OrderListView(ListView):
    model = Order
    template_name = 'webapp/orders/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10
    ordering = ['-order_date']


class OrderDetailView(DetailView):
    model = Order
    template_name = 'webapp/orders/order_detail.html'



class StaffListView(ListView):
    model = Staff
    template_name = 'webapp/staff/staff_list.html'
    context_object_name = 'staff_members'


class StaffCreateView(CreateView):
    model = Staff
    form_class = StaffForm
    template_name = 'webapp/staff/staff_form.html'
    success_url = reverse_lazy('staff_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Staff member created successfully!')
        return super().form_valid(form)

class StaffUpdateView(UpdateView):
    model = Staff
    form_class = StaffForm
    template_name = 'webapp/staff/staff_form.html'
    success_url = reverse_lazy('staff_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Staff member updated successfully!')
        return super().form_valid(form)
    

class TaskListView(ListView):
    model = Task
    template_name = 'webapp/tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.all().order_by('due_date')


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'webapp/tasks/task_form.html'
    success_url = reverse_lazy('task_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Task created successfully!')
        return super().form_valid(form)

class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'webapp/tasks/task_form.html'
    success_url = reverse_lazy('task_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Task updated successfully!')
        return super().form_valid(form)

def complete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.is_completed = True
    task.save()
    messages.success(request, f'Task "{task.title}" marked as completed!')
    return redirect('task_list')


def dashboard(request):
    recent_orders = Order.objects.all().order_by('-order_date')[:5]
    pending_tasks = Task.objects.filter(is_completed=False).order_by('due_date')[:5]
    active_staff = Staff.objects.filter(is_active=True).count()
    
    context = {
        'recent_orders': recent_orders,
        'pending_tasks': pending_tasks,
        'active_staff': active_staff,
    }
    return render(request, 'webapp/dashboard.html', context)



from django.http import HttpResponse
import csv
def export_customers_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customers.csv"'
    writer = csv.writer(response)
    writer.writerow([
        'ID', 'First Name', 'Last Name', 'Email', 'Phone', 
        'Address', 'City', 'Province', 'Country'
    ])
    customers = Customer.objects.all().order_by('last_name', 'first_name')
    
    for customer in customers:
        writer.writerow([
            customer.id,
            customer.first_name,
            customer.last_name,
            customer.email,
            customer.phone,
            customer.address,
            customer.city,
            customer.province,
            customer.country,
            
        ])
    
    return response
