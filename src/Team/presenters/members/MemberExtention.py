from Team.models import TeamModel
from Users.models import Role_user, Attachment
from django.contrib.auth.models import User


class MemberExtention:
    def _find_team(self):
        try:
            if self.member_data["id_team"]:
                find_team = TeamModel.objects.get(id_team=self.member_data["id_team"])
                if find_team:
                    return find_team
                else:
                    return "Can not found this id"

        except Exception as e:
            return e

    def _find_user(self):
        try:
            if self.member_data["id_user"]:
                find_user = User.objects.get(id=self.member_data["id_user"])
                if find_user:
                    return find_user
                else:
                    return "Can not found this id"

        except Exception as e:
            return e

    def _find_attachment(self):
        try:
            if self.member_data["id_attachment"]:
                find_attachment = Attachment.objects.get(
                    id_attachment=self.member_data["id_attachment"]
                )
                if find_attachment:
                    return find_attachment
                else:
                    return "Can not found this id"

        except Exception as e:
            return e

    def _handle_object_to_json(self, members):
        zipDatas = []
        if len(members) > 0:
            for member in members:
                data = {
                    "id_role": member.id_role,
                    "name_attachment": member.id_attachment.name_attachment,
                    "name_team": member.id_team.name_team,
                    "name_user": "{} {}".format(
                        member.id_user.first_name, member.id_user.last_name
                    ),
                    "id_user": member.id_user.id,
                }
                zipDatas.append(data)
        return zipDatas
