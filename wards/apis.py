from wards.models import Ward
from django.http import JsonResponse
from utils import get_user_wards
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.db.models import Q

class AllWardsAPI(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", "")
        column_mapping = {
            "0": "id",
            "1": "ward_name",
            "2": "ward_class__class_name",
            "4": "ward_parent__first_name",
            "6": "ward_date_added"
        }
        order_column = request.GET.get("order[0][column]", "0")
        order_field = request.GET.get(column_mapping[order_column], "id")
        order_dir = request.GET.get("order[0][dir]", "asc")
        data = []
        all_wards = get_user_wards(request.user)
        wards = all_wards
        total_records = all_wards.count()
        if search_value != "":
            wards = all_wards.filter(
                Q(ward_name__icontains=search_value ) |
                Q(id__icontains=search_value ) |
                Q(ward_parent__user__first_name__icontains=search_value ) |
                Q(ward_parent__user__last_name__icontains=search_value ) |
                Q(ward_class__class_name__icontains=search_value )
            )

        records_filtered = wards.count()
        wards = wards.order_by(order_field) if order_dir == "asc" else wards.order_by(f"-{order_field}")
        wards = wards[start:start + length]
        for ward in wards:
            ward_name_html = ward.ward_name
            ward_parent_html = str(ward.ward_parent)
            actions = f"""<a href="{reverse('view-daily-report', kwargs={'pk':ward.id})}"><button type="button">View Daily Report</button>
                        """
            if request.user.groups.filter(name="Administrators").exists():
                ward_name_html = f"""<a href="{reverse('update-ward', kwargs={'pk':ward.id})}">{ward.ward_name}
                """    

                ward_parent_html = f"""<a href="{reverse('update-parent', kwargs={'pk':ward.ward_parent.user.id})}">{str(ward.ward_parent)}
                """          

            if not request.user.groups.filter(name="Parents").exists():
                actions += f"""<a href="{reverse('add-daily-report', kwargs={'ward_id':ward.id})}"><button type="button">Fill Daily Report</button>
                """

            data.append({
                "id" : ward.id,
                "ward_name" : ward_name_html,
                "ward_date_added" : ward.ward_date_added,
                "ward_parent_name" : ward_parent_html,
                "ward_parent_phone" : ward.ward_parent.user_phone_1,
                "ward_class" : str(ward.ward_class) if ward.ward_class else "",
                "ward_date_added" : ward.ward_date_added,
                "ward_dob" : ward.ward_dob,
                "actions" : actions
            })
        return JsonResponse(
            {
                "draw" : draw,
                "recordsTotal" : total_records,
                "recordsFiltered" : records_filtered,
                "data" : data,
                # "searchBuilder": {
                #     "options": {
                #         "ward_name": [
                #             {"label": name, "value": name} for name in all_wards.order_by("ward_name")
                #                 .values_list("ward_name", flat=True)
                #                 .distinct()
                #         ],
                #         "ward_class": [
                #             {"label": name, "value": name} for name in all_wards.exclude(ward_class__isnull=True)
                #                 .order_by("ward_class__class_name")
                #                 .values_list("ward_class__class_name", flat=True)
                #                 .distinct()
                #         ],
                #         "id": [
                #             {"label": ward_id, "value": ward_id} for ward_id in all_wards.order_by("id")
                #                 .values_list("id", flat=True)
                #                 .distinct()
                #         ],
                #         "ward_date_added": [
                #             {"label": date.strftime("%Y-%m-%d"), "value": date.strftime("%Y-%m-%d")} for date in all_wards.order_by("ward_date_added")
                #             .values_list("ward_date_added", flat=True)
                #             .distinct()
                #         ],
                #         "ward_dob": [
                #             {"label": date.strftime("%Y-%m-%d"), "value": date.strftime("%Y-%m-%d")} for date in all_wards.order_by("ward_dob")
                #             .values_list("ward_dob", flat=True)
                #             .distinct()
                #             if date is not None
                #         ],
                #     }
                # }
            }
        )
