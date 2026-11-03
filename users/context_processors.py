def user_roles(request):
    user = request.user
    if not user.is_authenticated:
        return {
            "is_daycare_admin" : False,
            "is_daycare_staff" : False,
            "is_daycare_parent" : False,
        }

    return {
                "is_daycare_admin" : user.groups.filter(name="Administrators").exists(),
                "is_daycare_staff" : user.groups.filter(name="Staff").exists(),
                "is_daycare_parent" : user.groups.filter(name="Parents").exists()
            }