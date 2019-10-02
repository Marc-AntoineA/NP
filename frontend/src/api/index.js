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
      if (results.status !== 200) {
        results.json().then(({ detail }) => {
          reject({ code: results.status, error: detail });
        });
        return;
      }
      resolve(results.json());
    }).catch((err) => {
      reject({ code: undefined, error: err });
    });
  });
}

const API_PATH = require('../settings.json').BACKEND_URL;
console.log(API_PATH);

export function fetchNeigborsForPictureId(pictureId, token) {
  return request({
    url: API_PATH + 'neighbors/' + pictureId,
    data: undefined,
    token: token.access
  }, 'get', 'no-cache');
}

export function fetchTagsForPictureId(pictureId, token) {
  return request({
    url: API_PATH + 'tags/' + pictureId,
    data: undefined,
    token: token.access
  }, 'get', 'no-cache');
}

export function postTagsForPictureId(pictureId, tags, token) {
  return request({
    url: API_PATH + 'tags/' + pictureId,
    data: tags,
    token: token.access
  }, 'post');
}

export function fetchAllTags(token) {
  return request({
    url: API_PATH + 'tags',
    data: undefined,
    token: token.access,
  }, 'get', 'no-cache');
}

export function fetchRandomPicture(token) {
  return request({
    url: API_PATH + 'pictures/random',
    data: undefined,
    token: token.access,
  }, 'get', 'no-cache');
}

export function fetchWholeGraph(token) {
  return request({
    url: API_PATH + 'neighbors',
    data: undefined,
    token: token.access,
  }, 'get', 'no-cache');
}

export function fetchLessTaggedPictures(token) {
  return request({
    url: API_PATH + 'pictures/less-tagged/20',
    data: undefined,
    token: token.access
  }, 'get', 'no-cache');
}

export function fetchToken({ username, password }) {
  return request({
    url: API_PATH + 'login/token/',
    data: { username, password },
    token: ''
  }, 'post');
}

export function refreshToken(token) {
  return request({
    url: API_PATH + 'login/token/refresh/',
    data: { refresh: token.refresh },
    token: '',
  }, 'post');
}

export function uploadPicture(token, picture) {

  console.log(API_PATH + 'picture/upload');
  console.log(picture);
  return request({
    url: API_PATH + 'picture/upload',
    data: picture,
    token: token.access
  }, 'post');
}
