import Vue from 'vue';
import VueRouter from 'vue-router';
import SettingsUser from '@/views/settings/user/Main.vue';
import LandingPage from '@/views/landingPage/Main.vue';
import Impressum from '@/views/footer/Impressum.vue';
import Datenschutz from '@/views/footer/Datenschutz.vue';

// import CheckTokenMain from '@/views/login/CheckToken.vue';
// import EventOverview from '@/views/event/overview/Overview.vue';
// import StatisticOverview from '@/views/statistic/Main.vue';
// import RegistrationForm from '@/views/registration/Main.vue';
// import RegistrationCreate from '@/views/registration/create/Main.vue';
// import CreateEvent from '@/views/event/create/Main.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'landing',
    component: LandingPage,
  },
  // {
  //   path: '/check-token',
  //   name: 'checkToken',
  //   component: CheckTokenMain,
  // },
  // {
  //   path: '/event/create/:id',
  //   name: 'createEvent',
  //   component: CreateEvent,
  //   props: true,
  // },
  // {
  //   path: '/event/overview',
  //   name: 'eventOverview',
  //   component: EventOverview,
  // },
  {
    path: '/settings/user',
    name: 'settingsUser',
    component: SettingsUser,
  },
  // {
  //   path: '/statistic/:id',
  //   name: 'statisticOverview',
  //   component: StatisticOverview,
  //   props: true,
  // },
  // {
  //   path: '/registration/form/:id',
  //   name: 'registrationForm',
  //   component: RegistrationForm,
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
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
