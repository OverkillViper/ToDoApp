<script setup>
    import Sidebar from '../components/Sidebar.vue'
    import Tasks from '../components/Tasks.vue'
    import { useTaskStore } from '@/stores/task'
    import { useGroupStore } from '@/stores/group'
    import { ref } from 'vue'

    const props = defineProps(['groupId'])

    const taskStore = useTaskStore();
    const groupStore = useGroupStore();

    groupStore.initStore();
    taskStore.initStore();
    taskStore.getGroupTasks(props.groupId);

    const group = ref();
    group.value = groupStore.getGroup(props.groupId)

    const tasks = ref();
    tasks.value = taskStore.groupTasks
</script>


<template>
   <div class="relative flex flex-grow h-full">
        <Sidebar/>
        <div class="p-10 mx-auto text-white w-full md:w-auto">
            <div class="flex flex-row content-center justify-between">
                <div class="flex content-center">
                    <div class="px-1 rounded-md mr-4" :style="{ backgroundColor: group.color }">&nbsp</div>
                    <div class="text-2xl md:text-3xl font-primary">{{ group.name }}</div>
                </div>
                
                <div class="text-ternary text-2xl md:text-3xl font-bd p-0 text-end" v-if="tasks.length != 0">{{ tasks.length < 10 ? "0" + tasks.length : tasks.length }}</div>
            </div>
            
            <ul class="mt-5 mb-16" v-if="tasks.length != 0">
                <li class="mt-5" v-for="task in tasks">
                    <Tasks :task="task"/>
                </li>
            </ul>
            <div class="text-accent text-lg font-primary text-center mt-4" v-else>
                No pending tasks
            </div>
        </div>
    </div>
</template>


<style scoped>

</style>