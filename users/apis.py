from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse
from django.utils.html import format_html
from django.views import View


class AllParentsAPI(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name="Administrators").exists()

    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", "")
        column_mapping = {
            "0": "id",
            "1": "first_name",
            "2": "staff_profile__staff_classroom",
            "3": "email",
            "4": "profile__user_phone_1",
            "5": "profile__user_phone_2",
            "6": "date_joined",
        }
        order_column = request.GET.get("order[0][column]", "0")
        order_field = column_mapping.get(order_column, "id")
        order_dir = request.GET.get("order[0][dir]", "asc")
        all_parents = User.objects.filter(groups__name="Parents").select_related("profile")
        total_records = all_parents.count()
        parents = all_parents

        if search_value:
            parents = parents.filter(
                Q(username__icontains=search_value)
                | Q(id__icontains=search_value)
                | Q(first_name__icontains=search_value)
                | Q(last_name__icontains=search_value)
                | Q(email__icontains=search_value)
                | Q(profile__user_phone_1__icontains=search_value)
                | Q(profile__user_phone_2__icontains=search_value)
            )

        records_filtered = parents.count()
        if order_dir != "asc":
            order_field = f"-{order_field}"
        parents = parents.order_by(order_field)
        if length != -1:
            parents = parents[start : start + length]

        data = []
        for parent in parents:
            data.append(
                {
                    "id": parent.id,
                    "full_name": format_html(
                        '<a href="{}">{}</a>',
                        reverse("update-parent", kwargs={"pk": parent.id}),
                        parent.get_full_name(),
                    ),
                    "email": parent.email,
                    "user_phone_1": parent.profile.user_phone_1,
                    "user_phone_2": parent.profile.user_phone_2,
                    "date_added": parent.date_joined.date().isoformat(),
                }
            )

        return JsonResponse(
            {
                "draw": draw,
                "recordsTotal": total_records,
                "recordsFiltered": records_filtered,
                "data": data,
            }
        )


class AllStaffAPI(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name="Administrators").exists()

    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", "")
        column_mapping = {
            "0": "id",
            "1": "first_name",
            "2": "email",
            "3": "profile__user_phone_1",
            "4": "profile__user_phone_2",
            "5": "date_joined",
            "6": "staff__profile__staff_classroom",
        }
        order_column = request.GET.get("order[0][column]", "0")
        order_field = column_mapping.get(order_column, "id")
        order_dir = request.GET.get("order[0][dir]", "asc")
        all_staff = User.objects.filter(groups__name="Staff").select_related("profile","staff_profile")
        total_records = all_staff.count()
        staff = all_staff

        if search_value:
            staff = staff.filter(
                Q(username__icontains=search_value)
                | Q(id__icontains=search_value)
                | Q(first_name__icontains=search_value)
                | Q(last_name__icontains=search_value)
                | Q(email__icontains=search_value)
                | Q(profile__user_phone_1__icontains=search_value)
                | Q(profile__user_phone_2__icontains=search_value)
                | Q(staff_profile__staff_classroom__class_name__icontains=search_value)
            )

        records_filtered = staff.count()
        if order_dir != "asc":
            order_field = f"-{order_field}"
        staff = staff.order_by(order_field)
        if length != -1:
            staff = staff[start : start + length]

        data = []
        for member in staff:
            data.append(
                {
                    "id": member.id,
                    "full_name": format_html(
                        '<a href="{}">{}</a>',
                        reverse("update-staff", kwargs={"pk": member.id}),
                        member.get_full_name(),
                    ),
                    "email": member.email,
                    "user_phone_1": member.profile.user_phone_1,
                    "user_phone_2": member.profile.user_phone_2,
                    "staff_classroom": str(member.staff_profile.staff_classroom),
                    "date_added": member.date_joined.date().isoformat(),
                }
            )

        return JsonResponse(
            {
                "draw": draw,
                "recordsTotal": total_records,
                "recordsFiltered": records_filtered,
                "data": data,
            }
        )

