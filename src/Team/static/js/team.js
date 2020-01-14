const _csrf_token = csrf_token; // get token
const show_team_items = document.getElementById("show_team_items");
window.onload = () => {
  const load_data_teams = () =>
    fetch(`${HOSTMAIN}/Team/show_team_all/`).then(data => data.json());

  load_data_teams()
    .then(data => {
      const datas = data.data;
      for (let i = 0; i < datas.length; i++) {
        const { id_team, name_team } = datas[i];
        const textBtn = "add team member";
        const classDiv = "col-12 div_team col-md-4";
        const divCredted = createElementFun("div", classDiv);
        const createH5 = createElementFun("h5", "", name_team);
        const classBtn = "btn btn-primary col-12";
        const createButton = createElementFun("button", classBtn, textBtn, () =>
          goToAddmember(id_team)
        );
        divCredted.appendChild(createH5);
        divCredted.appendChild(createButton);
        show_team_items.appendChild(divCredted);
      }
    })
    .catch(err => console.log({ err }));
};

const onCreateTeam = e => {
  e.preventDefault();
  const nameTeam = document.getElementById("name_team").value;
  if (nameTeam) {
    const data = {
      name_team: nameTeam
    };
    fetchDataPost("Team/create_team_save/", _csrf_token, data)
      .then(dataCb => {
        // console.log({ dataCb });
        if (status === 200) {
          document.getElementById("name_team").value = "";
          message_show_success(dataCb.message, "success-message");
        } else {
          message_show_success(dataCb.message, "err-message");
        }
      })
      .catch(err => {
        console.log({ err });
      });
  } else {
    alert("name team not found");
  }
};

function goToAddmember(id_team) {
  if (id_team)
    window.location.href = `${HOSTMAIN}/Team/add_member_page/?id_team=${id_team}`;
}
