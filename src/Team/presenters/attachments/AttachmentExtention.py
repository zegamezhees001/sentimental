from Users.models import Permission, Attachment

class AttachmentExtention:

    def _save_attachment(self , permissionD):
        try:
            if self.attachmentData["name_attachment"]:
                attModel = Attachment(name_attachment=self.attachmentData["name_attachment"],id_permission=permissionD)
                attModel.save()
                return "save permission to attachment and create attachment success"
            else:
                return "name_attachment not found"
        except Exception as e:
            return e

    def _find_permission(self):
        try:
            if self.attachmentData['id_permission']:
                return Permission.objects.get(id_permission=int(self.attachmentData["id_permission"]))
            return "not id_permission self"
        except Exception as e:
            return e
    
    def object_to_json(attachmentData):
        datas = []
        if len(attachmentData) > 0:
            for attachment in attachmentData:
                data = {
                    "name_attachment": attachment.name_attachment,
                    "id_attachment" : attachment.id_attachment ,
                    "id_permission" : attachment.id_permission.id_permission,
                    "name_permission" : attachment.id_permission.name_permission
                }
                datas.append(data)
        return datas
