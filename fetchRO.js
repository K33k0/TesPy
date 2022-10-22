const getUsers = () => {
  return fetch('https://www.reddit.com/askreddit.json', {
    method: 'GET',
  })
    .then(res => {
      return res.json();
    })
}

getUsers().then(users => return users)

fetch('https://www.reddit.com/askreddit.json', {
    method: 'GET',
  })
    .then(res => {
      return res.json();
    })