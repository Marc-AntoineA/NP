// TODO error handling

function request({ url, data, token }, method, cache) {
  return new Promise((resolve, reject) => {
    fetch(url, {
      method: method,
      body: data ? JSON.stringify(data) : undefined,
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
      },
      cache: cache ? cache : 'default'
    }).then((results) => {
      resolve(results.json());
    }).catch((err) => {
      reject();
    });
  });
}

const API_PATH = 'http://localhost:8000/';

export function fetchNeigborsForImageId(imageId) {
  return request({
    url: API_PATH + 'neighbors/' + imageId,
    data: undefined,
    token: ''
  }, 'get', 'no-cache');
}
