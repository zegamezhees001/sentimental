window.onload = () => {
  document.getElementById("btn_create_user").disabled = true;

  initLoadAttachmentDatasForCreateUser();
};
function initLoadAttachmentDatasForCreateUser() {
  //   dc_id("message-create-user").style.display = "none";
  const err = "ff";
  message_show_success(err, dc_id("message-create-user"), "success-message");

  const id_att = document.getElementById("id_attachment");
  const createOption = createElementFun("option", "", "Null Attachment");
  createOption.value = "null";

  id_att.appendChild(createOption);
  fetch(`${HOSTMAIN}/Team/show_attachments/`)
    .then(d => d.json())
    .then(dataCB => {
      const { data } = dataCB;
      if (data.length) {
        removeChild(id_att);
        data.forEach(dAtt => {
          const { name_attachment, id_attachment } = dAtt;
          const createOption = createElementFun("option", "", name_attachment);
          createOption.value = id_attachment;
          id_att.appendChild(createOption);
        });
      }
    })
    .catch(err => {
      alert(err);
    });
}

function dc_id(name) {
  return document.getElementById(name);
}

function checkBtnCanClick() {
  const id_employee = dc_id("id_employee");
  const name_user = dc_id("name_user");
  const last_name_user = dc_id("last_name_user");
  const username = dc_id("username");
  const password = dc_id("password");
  const id_attachment = dc_id("id_attachment");
  const tel = dc_id("tel");
  const email = dc_id("email");
  if (
    id_employee.value &&
    name_user.value &&
    last_name_user.value &&
    username.value &&
    password.value &&
    id_attachment.value &&
    tel.value &&
    email.value
  ) {
    document.getElementById("btn_create_user").disabled = false;
  } else {
    document.getElementById("btn_create_user").disabled = true;
  }
}

const whenUserClick = event => {
  event.preventDefault();
  const message_create_user = dc_id("message-create-user");
  const id_employee = dc_id("id_employee");
  const name_user = dc_id("name_user");
  const last_name_user = dc_id("last_name_user");
  const username = dc_id("username");
  const password = dc_id("password");
  const id_attachment = dc_id("id_attachment");
  const tel = dc_id("tel");
  const zipDatas = {
    id_employee: id_employee.value,
    name_user: name_user.value,
    last_name_user: last_name_user.value,
    username: username.value,
    password: password.value,
    id_attachment: id_attachment.value,
    tel: tel.value,
    email: email.value
  };
  fetchDataPost("Users/admin_create_user/", csrf_token, zipDatas)
    .then(dataCB => {
      const { message } = dataCB;
      message_show_success(message, message_create_user, "success-message");
      clear_input();
    })
    .catch(err =>
      message_show_success(err, message_create_user, "err-message")
    );
};
document
  .getElementById("btn_create_user")
  .addEventListener("click", whenUserClick);

function clear_input() {
  id_employee.value = "";
  name_user.value = "";
  last_name_user.value = "";
  username.value = "";
  password.value = "";
  tel.value = "";
  email.value = "";
}
