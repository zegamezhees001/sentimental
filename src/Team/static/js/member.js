let choose_user = "";
let atts = [];
window.onload = () => {
  const add_btn_team = document.getElementById("add_btn_team");
  add_btn_team.disabled = true;
  initLoadUserDatas();
  initLoadAttachmentDatas();
};

const handleLoadAttachmentDataInformationSuccesed = (dataCB, id_att) => {
  const { data } = dataCB;
  if (data.length) {
    removeChild(id_att);
    checkSelectNotNull();
    data.forEach(dAtt => {
      const { name_attachment, id_attachment } = dAtt;
      atts[id_attachment] = { name_attachment, id_attachment };
      const createOption = createElementFun("option", "", name_attachment);
      createOption.value = id_attachment;
      id_att.appendChild(createOption);
    });
    handleNameAttachment();
  }
};

const handleDatasWhenUserIsNotEmpty = (dUser, id_user_e) => {
  const { first_name, last_name, employeeID, is_active, id_user } = dUser;
  const createCardDiv = createElementFun("div", "card-user");
  const createEleNameUser = createElementFun(
    "h5",
    "",
    `${first_name} ${last_name}`
  );
  createCardDiv.onclick = () => {
    let eleCards = document.getElementsByClassName("card-active");
    eleCards = Array.from(eleCards);
    if (eleCards.length) {
      eleCards = eleCards.map(eleCard => (eleCard.className = "card-user"));
    }
    createCardDiv.className = "card-active";
    choose_user = id_user;
    show_update_data(`${first_name} ${last_name}`, employeeID, is_active);
  };
  createCardDiv.appendChild(createEleNameUser);
  id_user_e.appendChild(createCardDiv);
};

const handleLoadUserDataInformationSuccesed = dataCB => {
  const { data } = dataCB;
  const id_user_e = document.getElementById("id_user");

  if (data.length) {
    removeChild(id_user);
    checkSelectNotNull();
    data.forEach(db => handleDatasWhenUserIsNotEmpty(db, id_user_e));
  }
};

function initLoadAttachmentDatas() {
  const createOption = createElementFun("option", "", "Null Attachment");
  const id_att = document.getElementById("id_attachment");
  createOption.value = "null";
  checkSelectNotNull();
  id_att.appendChild(createOption);
  fetch(`${HOSTMAIN}/Team/show_attachments/`)
    .then(d => d.json())
    .then(d => handleLoadAttachmentDataInformationSuccesed(d, id_att))
    .catch(err => {
      console.log({ err });
    });
}

function initLoadUserDatas() {
  const createOption = createElementFun("option", "", "Null User");
  createOption.value = "null";
  checkSelectNotNull();
  id_user.appendChild(createOption);
  fetch(`${HOSTMAIN}/Users/user_all/`)
    .then(d => d.json())
    .then(handleLoadUserDataInformationSuccesed)
    .catch(err => {
      console.log({ err });
    });
}

function checkSelectNotNull() {
  const add_btn_team = document.getElementById("add_btn_team");
  const id_att = document.getElementById("id_attachment");
  if (choose_user) add_btn_team.disabled = false;
  else add_btn_team.disabled = true;
  if (id_att.value != "null") add_btn_team.disabled = false;
  else add_btn_team.disabled = true;
}

function show_update_data(name_user, employeeID, is_active) {
  checkSelectNotNull();
  handleNameAttachment();
  document.getElementById("name_user").innerHTML = `Name user : ${name_user}`;

  document.getElementById(
    "employeeID"
  ).innerHTML = `Employee ID: ${employeeID}`;
  document.getElementById("status_active").innerHTML = `Status: ${is_active}`;
}

function addToTeam(e) {
  e.preventDefault();
  console.log({ choose_user });
}

function handleNameAttachment() {
  const id_att_v = document.getElementById("id_attachment").value;
  const filter_att = atts.length ? atts[id_att_v].name_attachment : "Null";
  document.getElementById(
    "name_attachment"
  ).innerHTML = `Attachment: ${filter_att}`;
}
