<script setup>
import Tasks from '../components/Tasks.vue'
import Sidebar from '../components/Sidebar.vue'
import { useTaskStore } from '@/stores/task'
import { useGroupStore } from '@/stores/group'
import { ref } from 'vue'

const taskStore = useTaskStore();
const groupStore = useGroupStore();

taskStore.initStore();
groupStore.initStore();

// let tasks = taskStore.tasks;
const tasks  = ref();
const groups = ref();

tasks.value = taskStore.completedTasks
groups.value = groupStore.groups

function deleteTask(id) {
    tasks.value = tasks.value.filter(tasks => tasks.id !== id)
    console.log(tasks);
}

</script>

<template>
    <div class="relative flex flex-grow h-full">
        <Sidebar/>
        <div class="p-10 mx-auto text-white w-full md:w-auto">
            <div class="flex flex-row content-center justify-between">
                <div class="text-2xl md:text-3xl font-primary">Completed Tasks</div>
                <div class="text-ternary text-2xl md:text-3xl font-bd p-0 text-end" v-if="tasks.length != 0">{{ tasks.length < 10 ? "0" + tasks.length : tasks.length }}</div>
            </div>
            <ul class="mt-5 mb-16" v-if="tasks.length != 0">
                <li class="mt-5" v-for="task in tasks">
                    <Tasks :task="task" v-on:delete="deleteTask" :groups="groups"/>
                </li>
            </ul>
            <div class="text-accent text-lg font-primary text-center mt-5" v-else>
                No completed tasks
            </div>
        </div>
    </div>
</template>

<style scoped>
</style>