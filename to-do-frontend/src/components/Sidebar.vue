<template>
    <div class="bg-secondary inset-y-0 left-0 hidden md:block p-6">
        <RouterLink to="/tasks" class="text-ternary font-primary text-md uppercase">Tasks</RouterLink>
        <div class="rounded-lg border border-accent py-2 px-4 uppercase font-primary flex content-center mt-4 text-accent cursor-pointer hover:bg-accent hover:text-white transition ease-in" @click="openTaskModal">
            <span class="material-icons text-md mr-3">add</span>Create new Task
        </div>

        <ul class="mt-5">
            <li class="my-1">
                <router-link to="/todays-tasks" class="flex flex-row content-center justify-between text-white p-1">
                    <div class="font-normal text-md p-2 flex flex-row content-center mr-7 hover:text-accent transition ease-in"><span class="material-icons text-md mr-2">event</span>Today's Tasks</div>
                    <div class="font-primary text-md bg-accent py-2 px-3 rounded-lg content-center">{{ taskStore.todaysTasks.length < 10 ? "0" + taskStore.todaysTasks.length : taskStore.todaysTasks.length }}</div>
                </router-link>
            </li>
            <li class="my-1">
                <router-link to="/pending-tasks" class="flex flex-row content-center justify-between text-white p-1">
                    <div class="font-normal text-md p-2 flex flex-row content-center mr-7 hover:text-accent transition ease-in"><span class="material-icons text-md mr-2">upcoming</span>Pending Task</div>
                    <div class="font-primary text-md bg-accent py-2 px-3 rounded-lg content-center">{{ taskStore.pendingTasks.length < 10 ? "0" + taskStore.pendingTasks.length : taskStore.pendingTasks.length }}</div>
                </router-link>
            </li>
            <li class="my-1">
                <router-link to="/completed-tasks" class="flex flex-row content-center justify-between text-white p-1">
                    <div class="font-normal text-md p-2 flex flex-row content-center mr-7 hover:text-accent transition ease-in"><span class="material-icons text-md mr-2">check_circle</span>Completed Tasks</div>
                    <div class="font-primary text-md bg-accent py-2 px-3 rounded-lg content-center">{{ taskStore.completedTasks.length < 10 ? "0" + taskStore.completedTasks.length : taskStore.completedTasks.length }}</div>
                </router-link>
            </li>
        </ul>

        <RouterLink class="text-ternary font-primary text-md uppercase mt-5" to="/groups">Groups</RouterLink>
        <div class="rounded-lg border border-accent py-2 px-4 uppercase font-primary flex content-center mt-4 text-accent cursor-pointer hover:bg-accent hover:text-white transition ease-in" @click="openGroupModal">
            <span class="material-icons text-md mr-3">add</span>Create new group
        </div>

        <ul class="mt-5" v-if="groupStore.groups.length != 0">
            <li class="my-1" v-for="group in groupStore.groups" :key="group.id">
                <router-link :to="{ name: 'GroupDetails', params: { groupId: group.id } }" class="flex flex-row content-center justify-between text-white p-1">
                    <div class="font-normal text-md p-2 flex flex-row content-center mr-7 hover:underline underline-offset-4 decoration-2"><div class="px-3 mr-3 rounded-full" :style="{ backgroundColor: group.color }"></div>{{ group.name}}</div>
                </router-link>
            </li>
        </ul>
    </div>
    <div class="bg-secondary fixed inset-x-0 bottom-0 p-2 text-white md:hidden">
        <div class="grid grid-cols-5 content-center">
            <a class="p-2 text-center" href="/todays-tasks">
                <span class="material-icons text-md">event</span>
                <div class="font-primary text-sm">Today</div>
            </a>
            <a class="p-2 text-center" href="/pending-tasks">
                <span class="material-icons text-md">upcoming</span>
                <div class="font-primary text-sm">Pending</div>
            </a>
            <div class="p-2 text-center bg-ternary text-secondary rounded-xl" @click="openTaskModal">
                <span class="material-icons text-md bg-ternary">add</span>
                <div class="font-primary text-sm">Create</div>
            </div>
            <a class="p-2 text-center" href="/completed-tasks">
                <span class="material-icons text-md">check_circle</span>
                <div class="font-primary text-sm">Complete</div>
            </a>
            <a class="p-2 text-center" href="/groups">
                <span class="material-icons text-md">workspaces</span>
                <div class="font-primary text-sm">Groups</div>
            </a>
        </div>
    </div>
    <GroupCreateModal v-if="isGroupModalOpen" @close="closeGroupModal"/>
    <TaskCreateModal v-if="isTaskModalOpen" @close="closeTaskModal" @taskCreated="updateAllTasks()"/>
</template>

<script setup>
    import GroupCreateModal from '../components/GroupCreateModal.vue'
    import TaskCreateModal from '../components/TaskCreateModal.vue'

    import { ref } from 'vue'
    import { useGroupStore } from '@/stores/group'
    import { useTaskStore } from '@/stores/task'

    const groupStore    = useGroupStore()
    const taskStore     = useTaskStore()

    const isGroupModalOpen  = ref(false);
    const isTaskModalOpen   = ref(false);



    function openGroupModal() {
        isGroupModalOpen.value = true;
    }

    function closeGroupModal() {
        isGroupModalOpen.value = false;
    }

    function openTaskModal() {
        isTaskModalOpen.value = true;
    }

    function closeTaskModal() {
        isTaskModalOpen.value = false;
    }

    function updateAllTasks() {
        taskStore.getAllTasks()
        taskStore.getPendingTasks()
        taskStore.getCompletedTasks()
        taskStore.getTodaysTasks()
    }

    taskStore.initStore()
    groupStore.initStore()

</script>

<style scoped>
</style>