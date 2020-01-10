const fetchDataPost = (url, _csrf_token, data) =>
  fetch(`${HOSTMAIN}/${url}`, {
    method: "POST", // *GET, POST, PUT, DELETE, etc.
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": _csrf_token
    },
    body: JSON.stringify(data)
  }).then(data => data.json());
