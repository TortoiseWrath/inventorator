import {reactive, provide, inject} from 'vue';

// See: https://dev.to/vuesomedev/you-might-not-need-vuex-with-vue-3-52e4

type VideoState = {
    videoDevices?: MediaDeviceInfo[],
    videoDevice?: number,
}

export const stateSymbol = Symbol('state');
export const createState = () => reactive({} as VideoState);
export const useState = () => inject(stateSymbol) as VideoState;
export const provideState = () => provide(stateSymbol, createState());