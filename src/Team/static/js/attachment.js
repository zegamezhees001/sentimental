document.getElementById("btn_add").disabled = true;
document.getElementById("message_name").style.display = "none";
const bigBoxList = document.getElementById("big-box-list");
initFetchDataInAddAttachmentPage();
const deleteAttachment = id_a => {
  if (confirm(`Are you sure you want to delete id ${id_a} ?`)) {
    //  post delete `${HOSTMAIN}/Team/delete_attachment/?id_attachment=`
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
  while (bigBoxList.firstChild) {
    bigBoxList.removeChild(bigBoxList.firstChild);
  }
  fetch(`${HOSTMAIN}/Team/show_attachments/`)
    .then(data => data.json())
    .then(dataCB => {
      const { data, message, status } = dataCB;
      if (data.length) {
        for (let i = 0; i < data.length; i++) {
          const createListBox = document.createElement("div");
          createListBox.className = "box-list";
          const createInformationMain = document.createElement("div");
          createInformationMain.className = "information-box";
          const createH5 = document.createElement("h5");
          const textH5Node = document.createTextNode(data[i].name_attachment);
          createH5.appendChild(textH5Node);
          const createSmall = document.createElement("small");
          const textSmall = document.createTextNode(data[i].name_permission);
          createSmall.appendChild(textSmall);
          createInformationMain.appendChild(createH5);
          createInformationMain.appendChild(createSmall);
          // --------------------------------------------
          const createDiv = document.createElement("div");
          const createBtn = document.createElement("button");
          const createI = document.createElement("i");
          createI.className = "far fa-trash-alt";
          createBtn.className = "btn btn-danger";
          createBtn.onclick = () => deleteAttachment(data[i].id_attachment);
          createBtn.appendChild(createI);

          createDiv.appendChild(createBtn);
          createListBox.appendChild(createInformationMain);
          createListBox.appendChild(createDiv);
          bigBoxList.appendChild(createListBox);
        }
      } else {
        const createDiv = document.createElement("div");
        createDiv.className = "for-empty-box";
        const createH5 = document.createElement("h5");
        createH5.className = "text-center";
        const createTextNode = document.createTextNode("Empty Attachment.");
        createH5.appendChild(createTextNode);
        createDiv.appendChild(createH5);
        bigBoxList.appendChild(createDiv);
      }
    })
    .catch(err => console.log(err));
}
