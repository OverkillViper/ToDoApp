<template>

    <div class="fixed top-0 bottom-0 left-0 right-0 bg-primary  flex justify-center content-center" v-if="isModalOpen">
        <div class="bg-secondary shadow-2xl rounded-2xl p-10 text-white w-4/5 md:w-2/5 m-auto z-40 ">
            <div class="flex flex-row justify-between content-center">
                <div class="font-primary text-2xl mb-4">Edit Task</div>
                <div>
                    <span class="material-icons text-white cursor-pointer" id="close" @click="closeModal">close</span>
                </div>
            </div>

            <form class="grid grid-cols-1 md:grid-cols-2 text-md gap-x-10" v-on:submit.prevent="updateTask()">
                <div class="mt-3">
                    <div class="font-primary text-white mb-2">Task Name</div>
                    <input type="text" name="title" id="title" v-model="title" class="bg-secondary2 p-3 rounded-sm border-b-4 border-accent font-primary outline-none w-full" placeholder="Enter task title">
                </div>
                <div class="mt-3">
                    <div class="font-primary text-white mb-2">Task Group</div>
                    <select name="group_id" id="group_id" v-model="groupID" class="bg-secondary2 p-4 font-primary w-full">
                        <option class="font-primary" v-for="group in groups" :key="group.id" :value="group.id" :selected="task.group.id === group.id">{{ group.name }}</option>
                    </select>
                </div>
                <div class="mt-3">
                    <div class="font-primary text-white mb-2">Task Deadline</div>
                    <input type="date" name="deadline" id="deadline" v-model="deadline" class="bg-secondary2 p-3 rounded-sm border-b-4 border-accent font-primary outline-none w-full" pattern="\d{4}-\d{2}-\d{2}">
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

    <div class="bg-secondary rounded-2xl overflow-hidden ">
        <div class="w-full p-5" :style="{ 'border-left': `8px solid ${task.group.color}` }">
            <div class="font-primary text-lg flex flex-row justify-between content-center">
                <div>{{ task.title }}</div>
                <div>
                    <span href="#"><span class="material-icons text-accent text-md mr-4 cursor-pointer" id="edit" @click="openModal">edit</span></span>
                    <span @click="deleteTask(task)" class="cursor-pointer"><span class="material-icons text-accent text-md">delete</span></span>
                </div>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-4 gap-y-3 mt-5 w-auto">
                <div class="">
                    <div class="font-normal textsm flex flex-row content-center"><span class="material-icons text-md mr-2" :style="{ color: task.group.color }">workspaces</span>Group</div>
                    <div class="font-primary pl-8" :style="{ color: task.group.color }">
                        {{ task.group.name }}
                    </div>
                </div>
                <div class="">
                    <div class="font-normal textsm flex flex-row content-center"><span class="material-icons text-md mr-2" :style="{ color: task.group.color }">event</span>Deadline</div>
                    <div class="font-primary pl-8" :style="{ color: task.group.color }">
                        {{ getDeadline(task.deadline) }}
                    </div>
                </div>
                <div class="">
                    <div class="font-normal textsm flex flex-row content-center"><span class="material-icons text-md mr-2" :style="{ color: task.group.color }">calendar_month</span>Remaining</div>
                    <div class="font-primary pl-8" :style="{ color: task.group.color }">
                        {{ calculateDaysRemaining(task.deadline) }} Days
                    </div>
                </div>
                <div>
                    <div class="flex flex-row content-center" v-if="task.status != 'complete'">
                        <div :class="(taskMissed)?'py-3 px-4 bg-red-300 rounded-md text-white font-primary text-xs 2xl:text-sm uppercase mr-4':'py-3 px-4 bg-primary rounded-md text-white font-primary text-xs 2xl:text-sm uppercase mr-4'">
                            {{ taskMissed ? 'Missed' : 'Pending'}}
                        </div>
                        <div class="py-3 px-4 bg-ternary rounded-md text-secondary font-primary text-xs 2xl:text-sm uppercase flex content-center flex-grow justify-center cursor-pointer" @click="markTaskComplete(task)">
                            <span class="material-icons text-primary text-xs 2xl:text-sm mr-2">check_circle</span>Done
                        </div>
                    </div>
                    <div class="flex flex-row content-center" v-else>
                        <div class="py-3 px-4 bg-accent rounded-md text-primary font-primary text-xs 2xl:text-sm uppercase mr-4">
                            Complete
                        </div>
                        <div class="py-3 px-4 bg-ternary rounded-md text-secondary font-primary text-xs 2xl:text-sm uppercase flex content-center cursor-pointer" @click="markTaskPending(task)">
                            <span class="material-icons text-primary text-xs 2xl:text-sm mr-2">cancel</span>Incomplete
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
    import axios from 'axios';
    import { ref } from 'vue'
    import { useTaskStore } from '@/stores/task'

    const taskStore = useTaskStore();
    const props = defineProps(['task', 'groups'])
    const emit = defineEmits(['delete'])

    const title = ref();
    const groupID = ref(null);
    const deadline = ref();

    title.value         = props.task.title
    groupID.value       = props.task.group.id
    deadline.value      = props.task.deadline

    const isModalOpen = ref(false);
    let taskMissed  = false;

    function openModal() {
        isModalOpen.value = true;
    }

    function closeModal() {
        isModalOpen.value= false;
    }

    function deleteTask(task) {
        emit('delete', task.id);

        axios
            .delete(`api/task-manager/tasks/delete/`+task.id)
            .then(response => {
                console.log(response.data);
                taskStore.getAllTasks()
                taskStore.getPendingTasks()
                taskStore.getCompletedTasks()
                taskStore.getTodaysTasks()
            })
            .catch(error => {
                console.log('error', error);
            })
    }

    function updateTask() {
        props.task.title    = title.value
        props.task.group.id = groupID.value

        for(let i = 0; i < props.groups.length; i++) {
            if (props.groups[i].id == groupID.value) {
                props.task.group.name = props.groups[i].name
                props.task.group.color = props.groups[i].color
                break
            }
        }

        props.task.deadline = deadline.value

        axios
            .post('api/task-manager/tasks/update/'+props.task.id, {
                'title'     : title.value,
                'groupID'   : groupID.value,
                'deadline'  : deadline.value
            })
            .then(response => {
                console.log('data', response.data);
                
                closeModal()
                taskStore.getAllTasks()
                taskStore.getPendingTasks()
                taskStore.getCompletedTasks()
                taskStore.getTodaysTasks()
            })
            .catch(error => {
                console.log('error', error);
            })

        closeModal()
    }

    function markTaskComplete(task) {
        task.status = 'complete'

        axios
            .post(`api/task-manager/tasks/mark-complete/`+task.id)
            .then(response => {
                taskStore.getAllTasks()
                taskStore.getPendingTasks()
                taskStore.getCompletedTasks()
                taskStore.getTodaysTasks()
            })
            .catch(error => {
                console.log('error', error);
            })
    }

    function markTaskPending(task) {
        task.status = 'pending'

        axios
            .post(`api/task-manager/tasks/mark-pending/`+task.id)
            .then(response => {
                taskStore.getAllTasks()
                taskStore.getPendingTasks()
                taskStore.getCompletedTasks()
                taskStore.getTodaysTasks()
            })
            .catch(error => {
                console.log('error', error);
            })
    }

    function getDeadline(deadline) {
        const deadlineDate = new Date(deadline);

        return deadlineDate.getDate() + " / " + (deadlineDate.getMonth() + 1) + " / " + deadlineDate.getFullYear()
    }


    function calculateDaysRemaining(deadline) {
        const today = new Date();
        const deadlineDate = new Date(deadline);
        const timeDifference = deadlineDate.getTime() - today.getTime();
        const daysRemaining = Math.ceil(timeDifference / (1000 * 60 * 60 * 24));

        taskMissed = daysRemaining < 0 ? true : false;

        return daysRemaining >= 0 ? daysRemaining : 0;
    }

</script>

<style scoped>
</style>
