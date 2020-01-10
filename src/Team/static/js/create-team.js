// const showSomeData = e => {
//   const csrf_token = document.getElementById("csrf_token");
//   console.log({ });
// };

const _csrf_token = csrf_token; // get token
const onCreateTeam = e => {
  e.preventDefault();
  const nameTeam = document.getElementById("name_team").value;
  if (nameTeam) {
    const data = {
      name_team: nameTeam
    };
    fetchDataPost(
      "Team/create_team_save/",
      _csrf_token,
      data
    ).then(data => console.log({ data }));
  } else {
    alert("name team not found");
  }
};
