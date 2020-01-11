const createBigBoxList = document.getElementById("big-box-list");

window.onload = () => {
  initElementPermissionList();
};

const addPermission = e => {
  e.preventDefault();
  const name_permission = document.getElementById("name_permission").value;
  if (name_permission) {
    const data = {
      name_permission: name_permission
    };
    fetchDataPost("Team/add_permission/", csrf_token, data)
      .then(dataCB => {
        const { data, message } = dataCB;
        alert(message);
      })
      .catch(errCb => console.log({ errCb }));
  } else {
    alert("name permission not found");
  }
};

function createElePermissionsList(data) {
  if (data.length > 0) {
    for (let i = 0; i < data.length; i++) {
      const { name_permission } = data[i];
      const createBoxList = createElementFun("div", "box-list");
      const createInformationEle = createElementFun("div", "information-box");
      const createH5 = createElementFun("h5", "", name_permission);
      createInformationEle.appendChild(createH5); // div.box-list element
      const createDiv = createElementFun("div");
      const createButtonDelete = createElementFun("button", "btn btn-danger");
      const createI_Trash_Icon = createElementFun("i", "far fa-trash-alt");
      createButtonDelete.appendChild(createI_Trash_Icon); // button element
      createDiv.appendChild(createButtonDelete); // div element

      createBoxList.appendChild(createInformationEle);
      createBoxList.appendChild(createDiv);
      createBigBoxList.appendChild(createBoxList);
    }
  } else {
    const createDiv = createElementFun("div", "for-empty-box");
    const createH5 = createElementFun("h5", "text-center", "Empty Attachment.");
    createH5.appendChild(createTextNode);
    createDiv.appendChild(createH5);
    createBigBoxList.appendChild(createDiv);
  }
}

function initElementPermissionList() {
  removeChild(createBigBoxList);
  fetch(`${HOSTMAIN}/Team/show_permissions`)
    .then(d => d.json())
    .then(dataCb => {
      const { message, data } = dataCb;
      console.log({ messagePermission: message });
      createElePermissionsList(data);
    })
    .catch(err => console.log({ err }));
}
