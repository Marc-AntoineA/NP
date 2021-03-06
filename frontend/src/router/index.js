import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router);

// import pages
const LoginView = () => import('../views/LoginView.vue');
const HomeView = () => import('../views/HomeView.vue');
const EditView = () => import('../views/EditView.vue');
const WalkView = () => import('../views/WalkView.vue');
const UploadView = () => import('../views/UploadView.vue');
const GraphAnalyzerView = () => import('../views/GraphAnalyzerView.vue');

export function createRouter() {
  return new Router({
    mode: 'history',
    fallback: false,
    scrollBehavior: () => ({ y: 0}),
    routes: [
      {
        path: '/',
        name: 'home',
        component: HomeView,
        meta: { requiresAuth: true }
      },
      {
        path: '/login',
        name: 'login',
        component: LoginView,
        meta: { requiresAuth: false }
      },
      {
        path: '/edit/:pictureId',
        name: 'edit',
        component: EditView,
        meta: { requiresAuth: true }
      },
      {
        path: '/walk/:pictureId',
        name: 'walk',
        component: WalkView,
        meta: { requiresAuth: true }
      },
      {
        path: '/analyze',
        name: 'analyze',
        component: GraphAnalyzerView,
        meta: { requiresAuth: true }
      },
      {
        path: '/upload',
        name: 'upload',
        component: UploadView,
        meta: { requiresAuth: true }
      }
    ]
  });
}
