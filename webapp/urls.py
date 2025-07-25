
from django.urls import path

from . import views

urlpatterns = [


    path('register', views.register, name="register"),

    path('', views.my_login, name=""),

    path('user-logout', views.user_logout, name="user-logout"),

    # CRUD

    path('dashboard', views.dashboard, name="dashboard"),



    path('dashboard', views.dashboard, name='dashboard'),
    
    # Customer URLs
    path('customers/', views.CustomerListView.as_view(), name='customer_list'),
    path('customers/<int:pk>/', views.CustomerDetailView.as_view(), name='customer_detail'),
    path('customers/new/', views.CustomerCreateView.as_view(), name='customer_create'),
    path('customers/<int:pk>/edit/', views.CustomerUpdateView.as_view(), name='customer_update'),
    path('customers/<int:pk>/delete/', views.CustomerDeleteView.as_view(), name='customer_delete'),
    path('customers/export/', views.export_customers_csv, name='export_customers_csv'),
    
    # Service URLs
    path('services/', views.ServiceListView.as_view(), name='service_list'),
    path('services/new/', views.ServiceCreateView.as_view(), name='service_create'),
    path('services/<int:pk>/edit/', views.ServiceUpdateView.as_view(), name='service_update'),
    
    # Order URLs
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/new/', views.order_create, name='order_create'),
    path('orders/<int:pk>/edit/', views.order_update, name='order_update'),
    path('orders/<int:pk>/status/<str:status>/', views.update_order_status, name='update_order_status'),
    
    # Staff URLs
    path('staff/', views.StaffListView.as_view(), name='staff_list'),
    path('staff/new/', views.StaffCreateView.as_view(), name='staff_create'),
    path('staff/<int:pk>/edit/', views.StaffUpdateView.as_view(), name='staff_update'),
    
    # Task URLs
    path('tasks/', views.TaskListView.as_view(), name='task_list'),
    path('tasks/new/', views.TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/edit/', views.TaskUpdateView.as_view(), name='task_update'),
    path('tasks/<int:pk>/complete/', views.complete_task, name='complete_task'),

    

]
