<template>
    <div class="fixed top-0 bottom-0 left-0 right-0 bg-primary  flex justify-center content-center">
        <div class="bg-secondary shadow-xl rounded-xl p-10 text-white w-4/5 md:w-2/5 m-auto z-40 ">
            <div class="flex flex-row justify-between content-center">
                <div class="font-primary text-xl mb-4">Create Task</div>
                <div>
                    <span class="material-icons text-white cursor-pointer" id="close" @click="closeModal">close</span>
                </div>
            </div>
            
            <form class="grid grid-cols-1 md:grid-cols-2 text-md gap-x-10" v-on:submit.prevent="createTask" method="POST">
                <div class="mt-3">
                    <div class="font-primary text-white mb-2">Task Title</div>
                    <input type="text" id="title" v-model="title" class="bg-secondary2 p-3 rounded-sm border-b-4 border-accent font-primary outline-none w-full" placeholder="Enter task title">
                </div>
                <div class="mt-3">
                    <div class="font-primary text-white mb-2">Task Group</div>
                    <select name="group_id" id="group_id" v-model="groupID" class="bg-secondary2 p-4 font-primary w-full">
                        <option v-for="group in groupStore.groups"  class="font-primary" :key="group.id" :value="group.id">{{ group.name }}</option>
                    </select>
                </div>
                <div class="mt-3">
                    <div class="font-primary text-white mb-2">Task Deadline</div>
                    <input type="date" id="deadline" v-model="deadline" class="bg-secondary2 p-3 rounded-sm border-b-4 border-accent font-primary outline-none w-full">
                </div>
                <div class="mt-3">
                    <div class="mb-2">&nbsp</div>
                    <button type="submit" class="p-3 bg-accent w-full rounded-md font-primary text-primary flex content-center justify-center">
                        <span class="material-icons text-primary mr-3 cursor-pointer">check</span>Save
                    </button>
                </div>
            </form>
        </div>
    </div>

</template>
  
<script setup>
    import axios from 'axios'
    import { useGroupStore } from '@/stores/group'
    import { useTaskStore } from '@/stores/task'
    import { defineEmits } from 'vue'
    import { ref } from 'vue'
    import router from '../router'


    const title = ref();
    const groupID = ref(null);
    const deadline = ref();

    const groupStore = useGroupStore()
    const taskStore = useTaskStore()

    const emit = defineEmits(['close', 'taskCreated'])

    function closeModal() {
        emit('close');
    }

    groupStore.initStore()

    function createTask() {
        // console.log('createTask', title.value, groupID.value, deadline.value);

        axios
            .post('api/task-manager/tasks/create', {
                'title'     : title.value,
                'groupID'   : groupID.value,
                'deadline'  : deadline.value
            })
            .then(response => {
                console.log('data', response.data);
            
                taskStore.getAllTasks()
                taskStore.getPendingTasks()
                taskStore.getCompletedTasks()
                taskStore.getTodaysTasks()
                router.push('/')
                closeModal()
            })
            .catch(error => {
                console.log('error', error);
            })
    }

</script>
  