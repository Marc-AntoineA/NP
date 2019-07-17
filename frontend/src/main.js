import Vue from 'vue';
import App from './App.vue';
import { sync } from 'vuex-router-sync';
import { createRouter } from './router';
import { createStore } from './store';

import { library } from '@fortawesome/fontawesome-svg-core'
import { faTimes } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

async function test() {
  const wasm = await import('wasm-graph-analyzer');
  wasm.greet();
  // console.log(`%c WASM Loaded `, `background: #049741; color: #fff`);
}
test();
library.add(faTimes)

Vue.component('font-awesome-icon', FontAwesomeIcon)


export function createApp() {
  const router = createRouter();
  const store = createStore();

  router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requiresAuth)) {
      /* if (store.getters.isLoggedIn) {
        next();
        return;
      }*/
      //next('/login');
      next();
    } else {
      next();
    }
  })

  sync(store, router);

  const app = new Vue({
    router,
    store,
    render: h => h(App)
  });

  return { app, router, store };
}

const { app } = createApp();
app.$mount('#app');
