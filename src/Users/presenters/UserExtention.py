class UserExtention:
    def __init__(self):
        pass

    def zip_data_profiles(self, profiles):
        zip_datas = []
        if len(profiles):
            for profile in profiles:
                bd = ""
                if profile.birth_date is not None:
                    bd = profile.birth_date.strftime("%d/%m/%YT%H:%M:%S")
                else:
                    bd = profile.birth_date
                print(profile.birth_date is not None, profile.birth_date, bd)
                data = {
                    "avatar": str(profile.avatar),
                    "bio": profile.bio,
                    "tel": profile.tel,
                    "birth_date": bd,
                    "first_name": profile.user.first_name,
                    "last_name": profile.user.last_name,
                    "employeeID": profile.employeeID,
                    "is_staff": profile.user.is_staff,
                    "is_active": profile.user.is_active,
                    "id_user": profile.id,
                }
                zip_datas.append(data)
        return zip_datas

    def get_model(self):
        return {
            "id_employee": self.id_employee,
            "first_name": self.first_name,
            "last_name_user": self.last_name_user,
            "username": self.username,
            "password": self.password,
            "tel": self.tel,
            "email": self.email,
        }

