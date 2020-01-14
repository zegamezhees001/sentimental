from django.shortcuts import render
import json
from .models import TeamModel
from BaseSettings.respone_data import responseData, message_handle
from Users.models import Permission, Attachment
from django.contrib.auth.decorators import user_passes_test
from BaseSettings.permissions import check_user_is_admin
from .presenters.attachments.AttachmentModel import AttachmentModel, AttachmentExtention

# extention --------------------------------------------

# objectModel is a Model ex. Permission or Attachment to get all objects.
# this function will return data each of model data.
def handleDataObjectAndReturnData(objectModel):
    zipDatas = []
    try:
        objectsModelVal = objectModel.objects.all()
        zipDatas = []
        if len(objectsModelVal) > 0:
            for objectVal in objectsModelVal:
                zipDatas.append(objectVal)
        return zipDatas
    except Exception as e:
        return e


# end extention --------------------------------------------


# add -----––-----------------
@user_passes_test(check_user_is_admin, login_url="Users:login")
def add_attachment_page(req):
    try:
        zipDatas = []
        try:
            get_datas = handleDataObjectAndReturnData(Permission)
            zipDatas = {"permissions_data": get_datas}
            return render(
                req,
                "add_attachment.html",
                {"message": "did not Add attachment", "datas": zipDatas, "status": 404},
            )
        except:
            return render(
                req,
                "add_attachment.html",
                {
                    "message": "something wrong in database get data.\n err show {}".format(
                        e
                    ),
                    "datas": zipDatas,
                    "status": 500,
                },
            )
    except:
        return render(req, "add_attachment.html")


@user_passes_test(check_user_is_admin, login_url="Users:login")
def add_attachment(req):
    try:
        if req.method == "POST":
            attachmentData = json.loads(req.body)
            attModel = AttachmentModel(attachmentData)
            getMessage = attModel.add_attachment()
            messageF = message_handle("", getMessage["message"])
            return responseData(messageF, getMessage["status"])
        messageF2 = message_handle("This method not allow this url.", [])
        return responseData(messageF2, 401)
    except Exception as e:
        return responseData(message_handle("err message: {}".format(e), [], 500), 500)


# end add ------

# show ---------------------------------------
@user_passes_test(check_user_is_admin)
def show_attachments(req):
    try:
        attachmentData = handleDataObjectAndReturnData(Attachment)
        datas = AttachmentExtention.object_to_json(attachmentData)
        return responseData(message_handle("Attachment show success", datas, 200), 200)
    except Exception as e:
        print(e)
        return responseData(message_handle("\n err show: {}".format(e), []), 500)


# end show ------------------------


# delete -------------------------------
def delete_attachment(req):
    try:
        if req.method == "DELETE" and req.GET.get("id_attachment"):
            id_attachment = req.GET.get("id_attachment")
            message_delete = AttachmentModel().delete_attachment(id_attachment)
            messageF = message_handle(message_delete, [])
            return responseData(messageF, 200)
        else:
            message_handle("id_attachment is not found.", [])
            return responseData(message_, 404)
    except Exception as e:
        return responseData(message_handle("\n err show: {}".format(e), []), 500)


# end delete -------------------------------
