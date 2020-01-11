function dc_id(name) {
  return document.getElementById(name);
}

function checkBtnCanClick() {
  const id_employee = dc_id("id_employee");
  const name_user = dc_id("name_user");
  const last_name_user = dc_id("last_name_user");
  const username = dc_id("username");
  const password = dc_id("password");

  const tel = dc_id("tel");
  const email = dc_id("email");
  if (
    id_employee.value &&
    name_user.value &&
    last_name_user.value &&
    username.value &&
    password.value &&
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
  const id_employee = dc_id("id_employee");
  const name_user = dc_id("name_user");
  const last_name_user = dc_id("last_name_user");
  const username = dc_id("username");
  const password = dc_id("password");
  const tel = dc_id("tel");
  const zipDatas = {
    id_employee: id_employee.value,
    name_user: name_user.value,
    last_name_user: last_name_user.value,
    username: username.value,
    password: password.value,
    tel: tel.value,
    email: email.value
  };
  fetchDataPost("Users/admin_create_user/", csrf_token, zipDatas)
    .then(dataCB => {
      const { message } = dataCB;
      message_show_success(message, "success-message");
      clear_input();
    })
    .catch(err => message_show_success(err, "err-message"));
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
