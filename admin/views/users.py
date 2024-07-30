# ruff: noqa: RUF012
from flask_admin.contrib.sqla import ModelView
from wtforms import PasswordField

class UserView(ModelView):
    can_delete = True
    can_create = False
    can_edit = True
    can_view_details = True
    edit_modal = True
    can_export = True
    details_modal = True
    export_types = ["csv", "xlsx", "json", "yaml"]

    column_searchable_list = ["id", "username", "first_name", "last_name", "phone"]
    column_filters = ["is_admin", "is_suspicious", "is_block", "is_premium", "created_at"]
    column_list = [
        "id",
        "username",
        "first_name",
        "last_name",
        "phone",
        "language_code",
        "is_admin",
        "is_suspicious",
        "is_block",
        "is_premium",
        "created_at",
    ]
    column_default_sort = ("created_at", True)


class ManagerView(ModelView):
    can_delete = True
    can_create = True
    can_edit = True
    can_view_details = True
    edit_modal = True
    can_export = True
    details_modal = True
    export_types = ["csv", "xlsx", "json", "yaml"]

    column_editable_list = ["name", "phone", "login", "password"]
    column_exclude_list = ["password"]
    column_details_exclude_list = column_exclude_list
    column_filters = column_editable_list
    form_overrides = {"password": PasswordField}
    column_searchable_list = ("id", "name", "phone", "login")
    column_list = (
        "id",
        "name",
        "phone",
        "login",
        "active",
    )
    
    # column_default_sort = ("created_at", True)


class ClientView(ModelView):
    can_delete = True
    can_create = True
    can_edit = True
    can_view_details = True
    can_export = True
    details_modal = True
    export_types = ["csv", "xlsx", "json", "yaml"]

    column_searchable_list = ("id", "name", "phone", ) #"manager.name"
    column_filters = ("active",)
    column_list = (
        "id",
        "name",
        "manager.name",
        "phone",
        "active",
    )

    # form_ajax_refs = {
    #     'user': QueryAjaxModelLoader('user', db.session, User, fields=['name'], page_size=10)
    # }
    # column_default_sort = ("created_at", True)
