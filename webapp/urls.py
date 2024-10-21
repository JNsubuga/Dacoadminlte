from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from pathlib import Path

#######
urlpatterns = [
    # users
    # general
    path("", views.index, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("users/", views.users, name="users"),
    path("user/add/", views.Adduser, name="add_user"),
    path("user/<int:userid>/update/", views.updateuser, name="update_user"),
    path("roles/", views.Roles, name="roles"),
    # path("staff/", views.staff, name="staff"),
    ### Logout
    path("logout/", views.logout, name="logout"),
    path("access-denied/", views.AccessDenied, name="access_denied"),

    path("accounts/", views.accounts, name="accounts"),
    # path("add_account/", views.createAccount, name="add_account"),
    # path("account/<accountid>", views.account, name="add_account"),

    path("members/", views.members, name="members"),
    # path("register_member/", views.createAccount, name="add_account"),
    # path("member/<accountid>", views.account, name="add_account"),

    path("transactions/", views.transactions, name="transactions"),

]
urlpatterns = urlpatterns + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)