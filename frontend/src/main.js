import Vue from 'vue';
import App from './App.vue';
import { sync } from 'vuex-router-sync';
import { createRouter } from './router';

export function createApp() {
  const router = createRouter();
  // const store = createStore();

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

  //sync(store, router);

  const app = new Vue({
    router,
    //store,
    render: h => h(App)
  });

  return { app, router };//, store };
}

const { app } = createApp();
app.$mount('#app');
