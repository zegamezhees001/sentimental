document.getElementById("btn_add").disabled = true;
document.getElementById("message_name").style.display = "none";
const bigBoxList = document.getElementById("big-box-list");
const _csrf_token = csrf_token; // pass from html file
initFetchDataInAddAttachmentPage();
const deleteAttachment = id_a => {
  if (confirm(`Are you sure you want to delete id ${id_a} ?`)) {
    const url = `${HOSTMAIN}/Team/delete_attachment/?id_attachment=${id_a}`;
    fetch(url, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": _csrf_token
      }
    })
      .then(data => data.json())
      .then(dataCb => {
        const { message } = dataCb;
        alert(message);
        initFetchDataInAddAttachmentPage();
      })
      .catch(err => alert(`cannot delete this id becase server err. ${err}`));
  }
};
const createAttachment = e => {
  e.preventDefault();
  const name_attachment = document.getElementById("name_attachment");
  const id_permission = document.getElementById("id_permissions");
  const name_attachmentVal = name_attachment.value;
  const id_permissionVal = id_permission.value;
  if (name_attachmentVal && id_permissionVal) {
    const data = {
      name_attachment: name_attachmentVal,
      id_permission: id_permissionVal
    };
    fetchDataPost("Team/add_attachment/", csrf_token, data)
      .then(dataCb => {
        const { data, message, status } = dataCb;
        name_attachment.value = "";
        initFetchDataInAddAttachmentPage();
        alert(`${message} status: ${status}`);
      })
      .catch(err => {
        alert("Error fetching Data");
      });
  }
};
const inputNameA = e => {
  if (e.target.value) {
    document.getElementById("btn_add").disabled = false;
    document.getElementById("message_name").style.display = "none";
  } else {
    document.getElementById("btn_add").disabled = true;
    document.getElementById("message_name").style.display = "block";
  }
};

function initFetchDataInAddAttachmentPage() {
  removeChild(bigBoxList);
  fetch(`${HOSTMAIN}/Team/show_attachments/`)
    .then(data => data.json())
    .then(dataCB => {
      const { data, message, status } = dataCB;
      createElementAttachmentList(data);
    })
    .catch(err => console.log(err));
}

function createElementAttachmentList(data) {
  if (data.length) {
    for (let i = 0; i < data.length; i++) {
      const { name_attachment, id_attachment } = data[i];
      //createElementFun is a function for create element path file in 'handle_ele_func.js'.
      const createH5 = createElementFun("h5", "", name_attachment);
      const createSmall = createElementFun("small", "", name_attachment);
      const createInformationMain = createElementFun(
        "div",
        "information-box",
        ""
      );
      createInformationMain.appendChild(createH5);
      createInformationMain.appendChild(createSmall);
      // --------------------------------------------
      const createDiv = createElementFun("div");
      const createBtn = createElementFun("button", "btn btn-danger", "", () =>
        deleteAttachment(id_attachment)
      );
      const createI = createElementFun("i", "far fa-trash-alt");
      createBtn.appendChild(createI);
      createDiv.appendChild(createBtn);
      const createBoxList = createElementFun("div", "box-list", "");
      createBoxList.appendChild(createInformationMain);
      createBoxList.appendChild(createDiv);
      bigBoxList.appendChild(createBoxList);
    }
  } else {
    const createDiv = createElementFun("div", "for-empty-box");
    const createH5 = createElementFun("h5", "text-center", "Empty Attachment.");
    createH5.appendChild(createTextNode);
    createDiv.appendChild(createH5);
    bigBoxList.appendChild(createDiv);
  }
}
