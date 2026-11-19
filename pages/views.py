from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from wards.models import Ward, Allergy, Classroom, Attendance
from daily_details.models import Nap
from users.models import StaffProfile
from django.utils import timezone
from django.db.models import Q
from datetime import datetime
from daily_details.models import DailyDetails
from pages.models import Holiday

# Create your views here.

class HomePageView(TemplateView):
    template_name = "pages/index.html"

class SeeGeneralReportParentView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        is_daycare_parent = self.request.user.groups.filter(name="Parents").exists()
        ward_id = self.kwargs["pk"]
        ward = Ward.objects.filter(id=ward_id).select_related("ward_parent").first()
        return (is_daycare_parent and (ward.ward_parent.user == self.request.user))

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.groups.filter(name="Parents").exists():
            ward = Ward.objects.filter(id=kwargs["pk"]).first()
            allergies = Allergy.objects.filter(allergy_ward=ward)
            naps = Nap.objects.filter(nap_ward=ward)
            meds = Nap.objects.filter(med_ward=ward)
            meals = Allergy.objects.filter(meal_ward=ward)
            context = {
                "ward" : ward,
                "allergies" : allergies,
                "naps" : naps,
                "meds" : meds,
                "meals" : meals
            }
            return render(request, "parents/general_report.html", context)

class SeeGeneralReportStaffView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name="Staff").exists()

    def get(self, request, *args, **kwargs):
        context = {

        }
        return render(request, "staff/general_report_staff.html", context)


class SeeGeneralReportAdminView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name="Administrators").exists()

    def get(self, request, *args, **kwargs):
        today = timezone.localdate()
        date_from_input = request.GET.get("date_from")
        date_from = datetime.strptime(date_from_input, '%Y-%m-%d').date() if (date_from_input and date_from_input != "") else None
        date_to_input = request.GET.get("date_to")
        date_to = datetime.strptime(date_to_input, '%Y-%m-%d').date() if (date_to_input and date_to_input != "") else today
        total_children = Ward.objects.filter(ward_status="active")
        total_classrooms = Classroom.objects.filter()
        total_active_staff = StaffProfile.objects.filter(staff__is_active=True)
        day_total_present = Attendance.objects.filter(attendance_status="present", attendance_date=today).count()
        day_total_children = total_children.count()
        day_percentage = (day_total_present / day_total_children) * 100
        total_daily_reports = DailyDetails.objects.filter(daily_details_date=today)
        total_daily_reports_count = total_daily_reports.count()
        day_dd_percentage = (total_daily_reports_count / day_total_children) * 100
        average_percentage_attendance = None
        attendance_days = []
        percentages = []
        dd_percentages = 0
        dd_submitted = 0
        dd_expected = 0
        initial_date = date_from or (date_to - timezone.timedelta(days=6))
        holidays = set(Holiday.objects.filter(holiday_date__range=[initial_date, date_to]).values_list("holiday_date", flat=True))
        
        if date_from:
            days = 0
            period_days = (date_to - date_from).days + 1
            for i in range(max(period_days, 0)):
                cur_date = date_from + timezone.timedelta(days=i)
                if cur_date in holidays:
                    continue
                days += 1

                cur_day_total_children = total_children.filter(
                    Q(ward_date_added__lt=cur_date)&
                    (Q(ward_status="active") | (Q(ward_status="inactive") & Q(ward_date_removed__gte=cur_date)))
                ).count()

                day_total_daily_reports_filled = DailyDetails.objects.filter(
                    daily_details_date = cur_date
                ).count()

                day_present_count = Attendance.objects.filter(
                    attendance_date = cur_date,
                    attendance_status = "present",
                    attendance_ward__in = total_children
                ).count()



                percentages.append((day_present_count / cur_day_total_children) * 100)
                attendance_days.append(f"{cur_date.strftime('%a, %d %b')}")
                dd_percentages += (day_total_daily_reports_filled / cur_day_total_children) * 100
                dd_submitted += day_total_daily_reports_filled
                dd_expected += cur_day_total_children



        average_percentage_attendance = (sum(percentages) / len(percentages) if percentages else 0) if date_from else day_percentage
        average_dd_filled_percentage = (dd_percentages / days if days else 0) if date_from else day_dd_percentage
        dd_submitted = dd_submitted if date_from else total_daily_reports_count
        dd_expected = dd_expected if date_from else day_total_children

        attendance_percentages = percentages if date_from else []
        if not attendance_percentages:
            i = 0
            j = 0
            while j < 5:
                cur_date = initial_date + timezone.timedelta(days=i)
                i += 1
                if cur_date > date_to:
                    break
                if cur_date.weekday() >= 5:
                    continue
                if cur_date in holidays:
                    continue

                cur_date_total_children = total_children.filter(
                    Q(ward_date_added__lt=cur_date)&
                    (Q(ward_status="active") | (Q(ward_status="inactive") & Q(ward_date_removed__gte=cur_date)))
                ).count()
                
                if cur_date_total_children == 0:
                    continue

                cur_date_present = Attendance.objects.filter(
                    attendance_date = cur_date,
                    attendance_status = "present",
                    attendance_ward__in = total_children
                ).count()

                attendance_percentages.append((cur_date_present / cur_date_total_children) * 100)
                attendance_days.append(f"{cur_date.strftime('%a, %d %b')}")
                j += 1
                

        

        context = {
            "total_children" : total_children.count(),
            "total_classrooms" : total_classrooms.count(),
            "total_staff" : total_active_staff.count(),
            "average_attendance" : average_percentage_attendance,
            "average_dd_filled" : average_dd_filled_percentage,
            "dd_submitted" : dd_submitted,
            "dd_expected" : dd_expected,
            "dd_outstanding" : dd_expected - dd_submitted,
            "chart_attendance_data" : attendance_percentages,
            "chart_attendance_labels" : attendance_days
        }

        return render(request, "staff/general_report_admin.html", context)
    


