
from Users.models import Permission, Attachment
from Team.presenters.attachments.AttachmentExtention import AttachmentExtention

class AttachmentModel(AttachmentExtention):
    def __init__(self , attachmentData):
        self.attachmentData = attachmentData

    def add_attachment(self):
        if self.attachmentData["name_attachment"] and self.attachmentData["id_permission"]:
            try:
                permissionD = self._find_permission()
                attachmentModel = self._save_attachment(permissionD)
                return {"message" : attachmentModel , "status" : 200}
            except Exception as e:
                print("aa " , e )
                return  e
        else:
            return {"message" : "name_a and id_p are empty" , "status" : 404}

    def delete_attachment(self , id_attachment):
        try:
            Attachment.objects.get(id_attachment=id_attachment).delete()
            return "delete data attachment id is {} success".format(id_attachment)
        except Exception as e:
            return e