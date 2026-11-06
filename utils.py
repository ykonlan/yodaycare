from wards.models import Ward

def get_user_wards(user):
    if user.groups.filter(name="Administrators").exists():
        return Ward.objects.select_related("ward_parent__user", "ward_class")
    wards = None
    p_wards = None
    if user.groups.filter(name="Staff").exists():
        wards = Ward.objects.filter(ward_class=user.staff_profile.staff_classroom).select_related("ward_parent__user", "ward_class").order_by("id")
    if user.groups.filter(name="Parents").exists():
        p_wards = Ward.objects.filter(ward_parent__user=user).select_related("ward_parent__user", "ward_class").order_by("id")
    if (wards is not None) and (p_wards is not None):
        return wards.union(p_wards).order_by("id")
    if wards or p_wards:
        return wards if wards else p_wards
    return Ward.objects.none()