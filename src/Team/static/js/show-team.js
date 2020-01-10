window.onload = () => {
  const load_data_teams = () =>
    fetch(`${HOSTMAIN}/Team/show_team_all/`).then(data => data.json());

  load_data_teams()
    .then(data => {
      const datas = data.data;
      console.log({ data });
      const show_team_items = document.getElementById("show_team_items");
      for (let i = 0; i < datas.length; i++) {
        const divCredted = document.createElement("div");
        const createH5 = document.createElement("h5");
        const text = document.createTextNode(datas[i].name_team);
        const createButton = document.createElement("button");
        const textButton = document.createTextNode("add team member");
        createH5.appendChild(text);
        createButton.appendChild(textButton);
        createButton.className = "btn btn-primary col-12";
        divCredted.appendChild(createH5);
        divCredted.appendChild(createButton);
        divCredted.className = "col-12 div_team col-md-4";
        show_team_items.appendChild(divCredted);
      }
    })
    .catch(err => console.log({ err }));
};
