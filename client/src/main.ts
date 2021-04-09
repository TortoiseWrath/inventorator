import {createApp} from 'vue';
import App from './App.vue';
import router from './router';
import Toast, {POSITION} from 'vue-toastification';
import {stateSymbol, createState} from '@/state';

import 'vue-toastification/dist/index.css';

const toastOptions = {
    showCloseButtonOnHover: true,
    draggablePercent: 0.3,
    position: POSITION.TOP_CENTER,
    transition: 'Vue-Toastification__fade',
};

createApp(App).use(router).use(Toast, toastOptions).provide(stateSymbol, createState()).mount('#app');

