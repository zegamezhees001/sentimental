let choose_user;
let atts = [];
let usersInGroup = [];
let attsInGroup = [];
let typeOfUserGroup = [];
let status_remove_childs_ele = false;

window.onload = () => {
  const add_btn_team = document.getElementById("add_btn_team");
  add_btn_team.disabled = true;
  initMemberListDatas();
};

const handleLoadAttachmentDataInformationSuccesed = (dataCB, id_att) => {
  const { data } = dataCB;
  if (data.length) {
    removeChild(id_att);
    checkSelectNotNull();
    data.forEach(dAtt => {
      const { name_attachment, id_attachment } = dAtt;
      if (!attsInGroup[name_attachment] || name_attachment !== "L0") {
        atts[id_attachment] = { name_attachment, id_attachment };
        const createOption = createElementFun("option", "", name_attachment);
        createOption.value = id_attachment;
        id_att.appendChild(createOption);
      }
    });
    handleNameAttachment();
  }
};

function clearEveryElement() {
  removeChild(document.getElementById("id_user"));
  // removeChild(document.getElementById("show-list-member"));
  // removeChild(document.getElementById("id_attachment"));
  atts = [];
  usersInGroup = [];
  attsInGroup = [];
  typeOfUserGroup = [];
}
const handleDatasWhenUserIsNotEmpty = (dUser, id_user_e) => {
  const { first_name, last_name, employeeID, is_active, id_user } = dUser;
  console.log({ dUser });
  if (!usersInGroup[id_user]) {
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
  }
};

const handleLoadUserDataInformationSuccesed = dataCB => {
  const { data } = dataCB;
  const id_user_e = document.getElementById("id_user");
  if (data.length) {
    checkSelectNotNull();
    if (usersInGroup.length === data.length) {
    }
    data.forEach(db => handleDatasWhenUserIsNotEmpty(db, id_user_e));
  }
};

const handleLoadDataMember = dataCB => {
  const show_list_member = document.getElementById("show-list-member");
  const { data } = dataCB;
  if (data.length) {
    // clear children
    removeChild(show_list_member);
    data.forEach(d => {
      if (d.name_user) {
        usersInGroup[d.id_user] = 1;
        attsInGroup[d.name_attachment] = 1;
        if (!typeOfUserGroup[d.name_attachment]) {
          typeOfUserGroup[d.name_attachment] = 0;
        }
        typeOfUserGroup[d.name_attachment] += 1;
      }
      const createElementDivBig = createElementFun(
        "div",
        "show-list-big-sub-member"
      );
      const createElementDiv = createElementFun("div", "show-list-sub-member");
      const createH5_NameUser = createElementFun(
        "h5",
        "",
        `ชื่อสมาชิก: ${d.name_user}`
      );
      const createH5_NameAttachment = createElementFun(
        "h5",
        "",
        `บทบาท: ${d.name_attachment}`
      );

      const createDiv2 = createElementFun("div", "");
      const createI = createElementFun("i", "far fa-window-close");
      createI.onclick = () => {
        removeChildrendUserInGruop(d.id_role);
      };
      createDiv2.appendChild(createI);
      createElementDiv.appendChild(createH5_NameUser);
      createElementDiv.appendChild(createH5_NameAttachment);
      createElementDivBig.appendChild(createElementDiv);
      createElementDivBig.appendChild(createDiv2);
      show_list_member.appendChild(createElementDivBig);
    });
    initLoadUserDatas();
    initLoadAttachmentDatas();
    // createElementTypeOfUserInGroup();
  } else {
    removeChild(show_list_member);
    initLoadUserDatas();
    initLoadAttachmentDatas();
    // createElementTypeOfUserInGroup();
    const createTextNull = createElementFun("h5", "text-center", "Null Group");
    show_list_member.appendChild(createTextNull);
  }
};

function createElementTypeOfUserInGroup() {
  const show_type_list = document.getElementById("show-type-list");
  removeChild(show_type_list);
  const typeObjectGruopArr = Object.keys(typeOfUserGroup);
  if (typeObjectGruopArr.length) {
    typeObjectGruopArr.forEach(key => {
      const createElementDiv = createElementFun("div", "col-12 col-md-4");
      const createaH5 = createElementFun("h5", "", `${key}`);
      const createaH52 = createElementFun("h5", "", typeOfUserGroup[key]);
      createElementDiv.appendChild(createaH5);
      createElementDiv.appendChild(createaH52);
      show_type_list.appendChild(createElementDiv);
    });
  }
}

function initMemberListDatas() {
  fetch(`${HOSTMAIN}/Team/show_member_list_by_team/?id_team=${id_team}`)
    .then(d => d.json())
    .then(handleLoadDataMember)
    .catch(e => console.log({ e }));
}

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
  checkSelectNotNull();
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
  if (choose_user && id_att.value) {
    add_btn_team.disabled = false;
  } else {
    add_btn_team.disabled = true;
  }
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
  const id_att = document.getElementById("id_attachment");

  if (choose_user && id_team && id_att.value) {
    const data = {
      id_user: choose_user,
      id_team,
      id_attachment: id_att.value
    };
    fetchDataPost(`Team/add_member/`, csrf_token, data)
      .then(data => {
        clearEveryElement();
        message_show_success(data.message, "success-message");
        initMemberListDatas();
      })
      .catch(err => console.log({ err }));
  }
}

function handleNameAttachment() {
  const id_att_v = document.getElementById("id_attachment").value;
  const filter_att = atts.length ? atts[id_att_v].name_attachment : "Null";
  document.getElementById(
    "name_attachment"
  ).innerHTML = `Attachment: ${filter_att}`;
}

function removeChildrendUserInGruop(id_role) {
  if (confirm(`Are you sure you want to delete id ${id_role} ?`)) {
    const url = `${HOSTMAIN}/Team/delete_member_from_id_role/?id_role=${id_role}`;
    fetch(url, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf_token
      }
    })
      .then(data => data.json())
      .then(dataCb => {
        clearEveryElement();
        const { message } = dataCb;
        message_show_success(message, "success-message");
        initMemberListDatas();
      })
      .catch(err => alert(`cannot delete this id becase server err. ${err}`));
  }
}
