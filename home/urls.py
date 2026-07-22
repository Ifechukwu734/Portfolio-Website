from django.urls import path
from . import views


urlpatterns = [
    path('', views.landing_page_view, name='landing_page'),

    path('signup/', views.signup_page, name='signup'),

    path('login/', views.login_page, name='login'),

    path('dashboard/', views.dashboard_page, name='dashboard'),

    path('projects/', views.auth_project_page, name='projects_page'),

    path('profile/', views.auth_profile_page, name='auth_profile'),

    path('update-project/<int:id>', views.update_project_page, name='update_project'),

    path('delete-project/<int:id>', views.delete_project, name='delete_project'),

    path('save-tech-stack/', views.save_tech_stacks, name='save_tech_stack'),

    path('save-account/', views.save_account, name='save_account'),

    path('<str:name>/<uuid:user_id>', views.portfolio_page, name='portfolio_page'),

    path('experiences/', views.experience_page, name='experience'),

    path('add-experience/', views.add_experience, name='add_experience'),

    path('update-experience/<int:id>', views.update_experience_page, name='update_experience'),

    path('delete-experience/<int:id>', views.delete_experience, name='delete_experience'),

    path('save-professional-profile/', views.save_professional_info, name='save_professional_profile'),

    path('<str:name>/<uuid:user_id>/projects/', views.portfolio_project_page, name='portfolio_project_page'),

    path('<str:name>/<uuid:user_id>/contact/', views.portfolio_contact_page, name='portfolio_contact_page'),

    path('logout/', views.user_logout, name='logout'),

    path('deactivate/', views.deactivate_portfolio, name='deactivate_portfolio'),

    path('reactivate/', views.reactivate_portfolio, name='reactivate_portfolio'),

    path("contact/<int:id>/mark-read/", views.mark_contact_read, name="mark_contact_read"),

    path("contact/<int:id>/mark-unread/", views.mark_contact_unread, name="mark_contact_unread"),

    path("contact/<int:id>/delete/", views.delete_contact, name="delete_contact"),
]