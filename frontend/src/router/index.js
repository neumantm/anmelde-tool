import Vue from 'vue';
import VueRouter from 'vue-router';
import SettingsUser from '@/views/settings/user/Main.vue';
import EventOverview from '@/views/event/overview/Overview.vue';

import MasterDataOverview from '@/views/event/data/Overview.vue';
import SettingsOverview from '@/views/settings/Main.vue';
import SettingsConfig from '@/views/settings/config/Main.vue';
import LandingPage from '@/views/landingPage/Main.vue';
import Impressum from '@/views/footer/Impressum.vue';
import Datenschutz from '@/views/footer/Datenschutz.vue';
import FAQ from '@/views/footer/FAQ.vue';
import EventPlaner from '@/views/eventPlaner/Main.vue';
import PlanEvent from '@/views/eventPlaner/create/Main.vue';
import registrationNew from '@/views/registration/Main.vue';
import registrationEdit from '@/views/registration/CreateUpdateContainer.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'landing',
    component: LandingPage,
  },
  {
    path: '/eventplaner',
    name: 'eventPlaner',
    component: EventPlaner,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/planevent/:id/:step?',
    name: 'planEvent',
    component: PlanEvent,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/event/overview',
    name: 'eventOverview',
    component: EventOverview,
    meta: {
      requiresAuth: true,
    },
  },
  // {
  //   path: '/event/adminOverview',
  //   name: 'eventAdminOverview',
  //   component: EventAdminOverview,
  // },
  {
    path: '/data/overview',
    name: 'dataOverview',
    component: MasterDataOverview,
  },
  {
    path: '/settings/overview',
    name: 'settingsOverview',
    component: SettingsOverview,
  },
  {
    path: '/settings/user',
    name: 'settingsUser',
    component: SettingsUser,
    meta: {
      requiresAuth: true,
    },
  },
  // {
  //   path: '/statistic/:id',
  //   name: 'statisticOverview',
  //   component: StatisticOverview,
  //   props: true,
  // },
  {
    path: '/registration/:id',
    name: 'registrationNew',
    component: registrationNew,
    props: true,
  },
  {
    path: '/registration/edit/:id',
    name: 'registrationEdit',
    component: registrationEdit,
    props: true,
  },
  {
    path: '/settings/config',
    name: 'settingsConfig',
    component: SettingsConfig,
  },
  // {
  //   path: '/statistic/:id',
  //   name: 'statisticOverview',
  //   component: StatisticOverview,
  //   props: true,
  // },
  // {
  //   path: '/registration/create/:id',
  //   name: 'registrationCreate',
  //   component: RegistrationCreate,
  //   props: true,
  // },
  {
    path: '/impressum',
    name: 'impressum',
    component: Impressum,
  },
  {
    path: '/datenschutz',
    name: 'datenschutz',
    component: Datenschutz,
  },
  {
    path: '/faq',
    name: 'faq',
    component: FAQ,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

function sleep(ms) {
  // eslint-disable-next-line no-promise-executor-return
  return new Promise((resolve) => setTimeout(resolve, ms));
}

router.beforeEach(async (to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    // We wait for Keycloak init, then we can call all methods safely
    while (router.app.$keycloak.createLoginUrl === null) {
      // eslint-disable-next-line no-await-in-loop
      await sleep(100);
    }
    if (router.app.$keycloak.authenticated) {
      next();
    } else {
      const loginUrl = router.app.$keycloak.createLoginUrl();
      window.location.replace(loginUrl);
    }
  } else {
    next();
  }
});

export default router;
