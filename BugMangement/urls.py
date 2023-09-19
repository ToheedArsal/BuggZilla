from django.urls import path
from .views import *
from django.conf.urls import handler404


urlpatterns = [
    path('signupaccount/', signup_user, name='signupaccount'),
    path('loginaccount/', login_user, name='loginaccount'),
    path('logoutaccount/', logout_account, name='logoutaccount'),
    path('managerdashboard/', manager_dashboard, name='managerdashboard'),
    path("addaproject/", add_project, name="addaproject"),
    path('updateproject/<int:project_id>/',
         update_project, name='updateproject'),
    path('deleteproject/<int:project_id>/',
         delete_project, name='deleteproject'),
    path('showallavailabledevelopers/<int:project_id>/',
         show_all_available_developers, name='showallavailabledevelopers'),
    path('assignadevelpor/<int:project_id>/',
         assign_a_developer, name='assignadevelpor'),
    path('showallavailableqa/<int:project_id>/',
         show_all_available_qa, name='showallavailableqa'),
    path('assignaqa/<int:project_id>/', assign_a_qa, name='assignaqa'),
    path('showassigneddeveloper/<int:project_id>',
         show_assigned_developers, name='showassigneddeveloper'),
    path('removedev/<int:project_id>', remove_developer, name='removedev'),
    path('showassignedqa/<int:project_id>',
         show_assigned_qa, name='showassignedqa'),
    path('removeqa/<int:project_id>', remove_qa, name='removeqa'),
    path("showallprojects/", show_all_projects, name="showallprojects"),
    path('qadashboard', qa_dashboard, name='qadashboard'),
    path('create_bug/<int:project_id>', create_bug, name='create_bug'),
    path('show_bug_of_qa', show_all_the_bugs_of_a_qa, name='show_bug_of_qa'),
    path('show_bug_detail/<int:project_id>',
         show_bug_of_a_project, name='show_bug_detail'),
    path('delete_a_bug/<int:bug_id>', delete_a_bug, name="delete_a_bug"),
    path('update_bug/<int:bug_id>', update_bug, name='update_bug'),
    path('developerdashboard', developer_dashboard, name='developerdashboard'),
    path('showallthebugsofaproject/<int:project_id>',
         show_all_the_bugs_of_a_project, name='showallthebugsofaproject'),
    path('assignabug/<int:bug_id>', assign_a_bug, name="assignabug"),
    path('showallassignedbugs', show_all_the_assigned_bugs_of_qa,
         name='showallassignedbugs'),
    path('markbug/<int:bug_id>', mark_the_bug, name='markbug'),
    path('no_access/', no_access, name='no_access'),
    path('', home, name='home'),
    path('showerror', show_error, name="showerror")

]
handler404 = handle_not_found_pages
