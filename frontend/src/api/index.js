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

const API_PATH = require('../settings.json').BACKEND_URL;
console.log(API_PATH);

export function fetchNeigborsForPictureId(pictureId) {
  return request({
    url: API_PATH + 'neighbors/' + pictureId,
    data: undefined,
    token: ''
  }, 'get', 'no-cache');
}

export function fetchTagsForPictureId(pictureId) {
  return request({
    url: API_PATH + 'tags/' + pictureId,
    data: undefined,
    token: ''
  }, 'get', 'no-cache');
}

export function postTagsForPictureId(pictureId, tags) {
  return request({
    url: API_PATH + 'tags/' + pictureId,
    data: tags,
    token: ''
  }, 'post');
}

export function fetchAllTags() {
  return request({
    url: API_PATH + 'tags',
    data: undefined,
    token: '',
  }, 'get', 'no-cache');
}

export function fetchRandomPicture() {
  return request({
    url: API_PATH + 'pictures/random',
    data: undefined,
    token: '',
  }, 'get', 'no-cache');
}

export function fetchWholeGraph() {
  return request({
    url: API_PATH + 'neighbors',
    data: undefined,
    token: '',
  }, 'get', 'no-cache');
}

export function fetchLessTaggedPictures() {
  return request({
    url: API_PATH + 'pictures/less-tagged/20',
    data: undefined,
    token: ''
  }, 'get', 'no-cache');
}
