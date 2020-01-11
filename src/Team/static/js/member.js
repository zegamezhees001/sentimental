const id_att = document.getElementById("id_attachment");
const id_user = document.getElementById("id_user");
const add_btn_team = document.getElementById("add_btn_team");
window.onload = () => {
  add_btn_team.disabled = true;
  initLoadAttachmentDatas();
  initLoadUserDatas();
};

function initLoadAttachmentDatas() {
  const createOption = createElementFun("option", "", "Null Attachment");
  createOption.value = "null";
  checkSelectNotNull();
  id_att.appendChild(createOption);
  fetch(`${HOSTMAIN}/Team/show_attachments/`)
    .then(d => d.json())
    .then(dataCB => {
      const { data } = dataCB;
      if (data.length) {
        removeChild(id_att);
        checkSelectNotNull();
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
function initLoadUserDatas() {
  const createOption = createElementFun("option", "", "Null User");
  createOption.value = "null";
  checkSelectNotNull();
  id_user.appendChild(createOption);
  // fetch(`${HOSTMAIN}/`)
}

function checkSelectNotNull() {
  if (id_att.value != "null") add_btn_team.disabled = false;
  else add_btn_team.disabled = true;
  if (id_user.value != "null") add_btn_team.disabled = false;
  else add_btn_team.disabled = true;
}

function addToTeam(e) {
  e.preventDefault();
}
