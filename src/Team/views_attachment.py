from django.shortcuts import render
import json
from .models import TeamModel
from BaseSettings.respone_data import responseData, message_handle
from Users.models import Permission, Attachment


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


def handleArraysObjectAttachmentToArraysJson(attachmentData):
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


# end extention --------------------------------------------


# add -----––-----------------
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


def add_attachment(req):
    if req.method == "POST":
        attachmentData = json.loads(req.body)
        if attachmentData["name_attachment"] and attachmentData["id_permission"]:
            try:
                permissionD = Permission.objects.get(
                    id_permission=int(attachmentData["id_permission"])
                )
                attachmentModel = Attachment(
                    name_attachment=attachmentData["name_attachment"],
                    id_permission=permissionD,
                )
                attachmentModel.save()
                return responseData(message_handle("Save Attachment Success", [], 200))
            except Exception as e:
                print(e)
                return responseData(
                    message_handle("something worng : {}".format(e), [], 500)
                )
        else:
            return responseData(message_handle("name_a and id_p are empty", [], 500))

    return responseData(message_handle("This method not allow this url.", []) , 401)


# end add ------

# show ---------------------------------------
def show_attachments(req):
    try:
        attachmentData = handleDataObjectAndReturnData(Attachment)
        datas = handleArraysObjectAttachmentToArraysJson(attachmentData)
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
            Attachment.objects.get(id_attachment=id_attachment).delete()
            return responseData(message_handle("delete data attachment id is {} success".format(id_attachment) , []) , 200)
        else:
            return responseData(message_handle("id_attachment is not found." , []) , 404)
    except Exception as e:
        return responseData(message_handle("\n err show: {}".format(e), []), 500)
        

# end delete -------------------------------