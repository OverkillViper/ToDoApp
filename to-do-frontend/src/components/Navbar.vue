<template>
    <div class="bg-secondary p-4 md:p-3 content-center grid grid-cols-2">
        <div class="flex items-center">
            <RouterLink class="flex items-center" to="/">
                <img src="/logo-main.png" alt="logo" class="w-10 p-0 m-0">
                <span class="text-white font-primary text-lg ml-4 align-middle">ToDo App</span>
            </RouterLink>

            <span class="text-gray-300 font-primary text-lg ml-16 hidden md:block">
                <RouterLink to="/tasks" class="text-gray-300">Tasks</RouterLink>
            </span>
        </div>
        
        <div class="flex items-center justify-end">
            <span class="text-gray-300 font-primary text-lg ml-16 md:hidden mr-3">
                <router-link to="/tasks" class="text-gray-300 flex items-center"><span class="material-icons">dashboard</span></router-link>
            </span>
            <RouterLink to="/profile" v-if="userStore.user.isAuthenticated" class="mr-2 md:mr-4 font-primary text-white hidden md:block">{{ userStore.user.name }}</RouterLink>
            <RouterLink to="/profile" class="rounded-full bg-white flex flex-row justify-end content-center" style="overflow: hidden;" v-if="userStore.user.isAuthenticated">
                <img :src="userStore.user.avatar" alt="user_dp" class="w-10 p-0 m-0 aspect-square object-cover">
            </RouterLink>
            <div class="rounded-full flex flex-row justify-end content-center text-white" style="overflow: hidden;" v-else>
                <RouterLink to="/login" class="material-icons text-white mx-2">login</RouterLink>
                <RouterLink to="/register" class="material-icons text-white mx-2">app_registration</RouterLink>
            </div>
        </div>
    </div>
</template>

<script>
import { RouterLink } from 'vue-router';
import { useUserStore } from '@/stores/user'
import axios from 'axios';

export default {
    setup() {
        const userStore = useUserStore()

        return {
            userStore
        }
    },
    beforeCreate() {
        this.userStore.initStore()
        const token = this.userStore.user.access

        if (token) {
            axios.defaults.headers.common["Authorization"] = "Bearer " + token;
        } else {
            axios.defaults.headers.common["Authorization"] = "";
        }
    }
}

</script>

<style scoped>
</style>
