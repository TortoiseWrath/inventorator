import {createRouter, createWebHistory, RouteRecordRaw} from 'vue-router';
import Home from '../views/Home.vue';

const routes: Array<RouteRecordRaw> = [
    {
        path: '/',
        name: 'Home',
        component: Home,
    },
    {
        path: '/about',
        name: 'About',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "about" */ '../views/About.vue'),
    },
    {
        path: '/items',
        name: 'Items',
        component: () => import('@/views/Items.vue'),
    },
    {
        path: '/item/:id',
        name: 'Edit Item',
        component: () => import('@/views/EditItem.vue'),
    },
    {
        path: '/add/:id',
        name: 'Add Item',
        component: () => import('@/views/AddItem.vue'),
    },
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
});

export default router;
