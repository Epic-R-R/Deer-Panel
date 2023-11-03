from django.urls import path
from .views import (
    SigninAdminView,
    ServerStatus,
    ServerFiltering,
    ServerOnlineUser,
    SignupUserView,
    DeleteUserView,
    GetAllUsersView,
    ActivateDeactivateUserView,
    SettingInitial,
    UserEditView,
    DetailUserView,
    CustomTokenRefreshView,
    KillUserView,
    KillPidView,
)

urlpatterns = [
    path("accounts/signin", SigninAdminView.as_view(), name="signin-admin"),
    path(
        "accounts/token/refresh", CustomTokenRefreshView.as_view(), name="refresh-token"
    ),
    path("accounts/signup", SignupUserView.as_view(), name="create-user"),
    path(
        "accounts/delete_user/<str:username>",
        DeleteUserView.as_view(),
        name="delete-user",
    ),
    path("accounts/edit-user", UserEditView.as_view(), name="edit-user"),
    path(
        "accounts/user-detail/<str:username>",
        DetailUserView.as_view(),
        name="user-detail",
    ),
    path(
        "accounts/kill_user/<str:username>",
        KillUserView.as_view(),
        name="user-kill",
    ),
    path(
        "accounts/toggle-user-status/<str:username>",
        ActivateDeactivateUserView.as_view(),
        name="toggle-user-status",
    ),
    path(
        "accounts/kill_pid/<str:pid>",
        KillPidView.as_view(),
        name="pid-kill",
    ),
    path("accounts/get-all-users", GetAllUsersView.as_view(), name="get-all-users"),
    path("server/status", ServerStatus.as_view(), name="vps-status"),
    path("server/filtering", ServerFiltering.as_view(), name="vps-filtering"),
    path("server/online-users", ServerOnlineUser.as_view(), name="vps-online-users"),
    path("server/setting-initial", SettingInitial.as_view(), name="settings"),
]
