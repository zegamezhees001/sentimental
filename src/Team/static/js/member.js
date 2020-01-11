let choose_user = "";
window.onload = () => {
  const add_btn_team = document.getElementById("add_btn_team");
  add_btn_team.disabled = true;
  initLoadUserDatas();
};

function initLoadUserDatas() {
  const id_user_e = document.getElementById("id_user");
  const createOption = createElementFun("option", "", "Null User");
  createOption.value = "null";
  checkSelectNotNull();
  id_user.appendChild(createOption);
  fetch(`${HOSTMAIN}/Users/user_all/`)
    .then(d => d.json())
    .then(dataCB => {
      const { data } = dataCB;
      if (data.length) {
        removeChild(id_user);
        checkSelectNotNull();
        data.forEach(dUser => {
          console.log({ dUser });
          const {
            avatar,
            bio,
            tel,
            birth_date,
            name_attachment,
            first_name,
            last_name,
            employeeID,
            is_staff,
            is_active,
            id_user
          } = dUser;

          const createCardDiv = createElementFun("div", "card-user");
          const createEleNameUser = createElementFun(
            "h5",
            "",
            `${first_name} ${last_name}`
          );
          const createEleAttachment = createElementFun(
            "h5",
            "",
            `${name_attachment}`
          );
          createCardDiv.onclick = () => {
            const eleCards = document.getElementsByClassName("card-active");
            if (eleCards.length) {
              for (let i = 0; i < eleCards.length; i++) {
                eleCards[i].className = "card-user";
              }
            }
            createCardDiv.className = "card-active";
            choose_user = id_user;
            show_update_data(
              `${first_name} ${last_name}`,
              name_attachment,
              employeeID,
              is_active
            );
          };
          createCardDiv.appendChild(createEleNameUser);
          createCardDiv.appendChild(createEleAttachment);
          id_user_e.appendChild(createCardDiv);
        });
      }
    })
    .catch(err => {
      alert(err);
    });
}

function checkSelectNotNull() {
  const add_btn_team = document.getElementById("add_btn_team");
  if (choose_user) add_btn_team.disabled = false;
  else add_btn_team.disabled = true;
}

function show_update_data(name_user, name_attachment, employeeID, is_active) {
  checkSelectNotNull();
  document.getElementById("name_user").innerHTML = `Name user : ${name_user}`;
  document.getElementById(
    "name_attachment"
  ).innerHTML = `Attachment: ${name_attachment}`;
  document.getElementById(
    "employeeID"
  ).innerHTML = `Employee ID: ${employeeID}`;
  document.getElementById("status_active").innerHTML = `Status: ${is_active}`;
}

function addToTeam(e) {
  e.preventDefault();
  console.log({ choose_user });
}
