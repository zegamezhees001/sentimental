from Team.models import TeamModel
from Users.models import Role_user, Attachment
from django.contrib.auth.models import User
from .MemberExtention import MemberExtention


class MemberModel(MemberExtention):
    def __init__(self, member_data):
        self.member_data = member_data

    def add_member(self):
        try:
            find_team = self._find_team()
            find_user = self._find_user()
            find_attachment = self._find_attachment()
            saveGroupUser = Role_user(
                id_attachment=find_attachment, id_user=find_user, id_team=find_team
            )
            saveGroupUser.save()
            return "Save Group user success"
        except Exception as e:
            return e

    def find_member_by_role(self, id_role):
        try:
            find_member = Role_user.objects.filter(id_role=id_role)
            return self._handle_object_to_json(find_member)
        except Exception as e:
            return e

    def find_member_by_team(self, id_team):
        try:

            find_member = Role_user.objects.filter(id_team=id_team)

            return self._handle_object_to_json(find_member)
        except Exception as e:
            return e

    def delete_member_by_id_role(self, id_role):
        try:
            Role_user.objects.get(id_role=id_role).delete()
            return "ลบรายการรหัส: {}".format(id_role)
        except Exception as e:
            return e
