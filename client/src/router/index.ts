import {createRouter, createWebHistory, RouteRecordRaw} from 'vue-router';

const routes: Array<RouteRecordRaw> = [
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
