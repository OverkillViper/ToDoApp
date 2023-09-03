<template>
    <div class="flex p-10 md:p-0 md:justify-center md:items-center flex-grow">
        <div class="w-full md:w-auto">
            <div class="text-xl md:text-2xl font-primary text-white">Good Day</div>
            

            <div v-if="userStore.user.isAuthenticated">
                <div class="text-2xl md:text-5xl font-normal text-white mt-2 w-auto md:w-96">{{ userStore.user.name }}</div>
            </div>
            <div v-else class="font-normal text-md text-white mt-2">
                Please Sign In or Sign up to continue
                <div class="mb-10">
                    <div>
                        <RouterLink to="/login" class="px-3 py-3 rounded-md flex my-5 bg-secondary2 w-full justify-center font-primary hover:bg-accent transition">Sign In</RouterLink>
                    </div>
                    <div>
                        <RouterLink to="/register" class="px-3 py-3 rounded-md flex my-5 bg-secondary2 w-full justify-center font-primary hover:bg-accent transition">Sign Up</RouterLink>
                    </div>
                </div>
            </div>

            <div class="grid grid-cols-2 gap-10 mt-5">
                <router-link class="p-5 bg-secondary aspect-square rounded-xl hover:drop-shadow-xl hover:bg-secondary2 transition ease-in delay-50 content-between grid" to="/pending-tasks">
                    <span><span class="material-icons bg-accent p-1 md:p-3 rounded-lg">task_alt</span></span>
                    <div class="font-normal text-white text-xl md:text-3xl">Tasks</div>
                </router-link>
                <router-link class="p-5 bg-secondary aspect-square rounded-xl hover:drop-shadow-xl hover:bg-secondary2 transition ease-in delay-50 content-between grid" to="/groups">
                    <span><span class="material-icons bg-accent p-1 md:p-3 rounded-lg">workspaces</span></span>
                    <div class="font-normal text-white text-xl md:text-3xl">Groups</div>
                </router-link>
            </div>

            <!-- <div class="text-lg font-normal text-ternary mt-5 uppercase">Todays Tasks</div> -->
            <!-- <div v-if="tasks.length > 0">
                <div class="p-4 bg-secondary text-white rounded-lg mt-2 font-primary" v-for="task in tasks">
                    <div class="font-normal text-xl">{{ task.title }}</div>
                </div>
            </div> -->
            <!-- <div v-else class="font-normal text-md text-accent text-center mt-3">No task has deadline today</div> -->
        </div>
    </div>
</template>

<script setup>
    // import Tasks from '../components/Tasks.vue'
    import axios from 'axios'
    import { useUserStore } from '@/stores/user'
    import { useTaskStore } from '@/stores/task'
    import { useGroupStore } from '@/stores/group'
    import { RouterLink } from 'vue-router';

    const userStore     = useUserStore()
    const taskStore     = useTaskStore()
    const groupStore    = useGroupStore()

    userStore.initStore()
    const token = userStore.user.access

    if (token) {
        axios.defaults.headers.common["Authorization"] = "Bearer " + token;
    } else {
        axios.defaults.headers.common["Authorization"] = "";
    }

    if (userStore.user.isAuthenticated) {
        taskStore.getAllTasks()
        taskStore.getPendingTasks()
        taskStore.getCompletedTasks()
        taskStore.getTodaysTasks()
        groupStore.getAllGroups()
    }

</script>

<style scoped>
</style>
