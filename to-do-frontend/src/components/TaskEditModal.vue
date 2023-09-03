<template>
    <div class="fixed top-0 bottom-0 left-0 right-0 bg-primary  flex justify-center content-center">
        <div class="bg-secondary shadow-xl rounded-xl p-10 text-white w-4/5 md:w-2/5 m-auto z-40 ">
            <div class="flex flex-row justify-between content-center">
                <div class="font-primary text-xl mb-4">Edit Task</div>
                <div>
                    <span class="material-icons text-white cursor-pointer" id="close" @click="closeModal">close</span>
                </div>
            </div>
            
            <form class="grid grid-cols-1 md:grid-cols-2 text-md gap-x-10" v-on:submit.prevent="updateTask">
                <div class="mt-3">
                    <div class="font-primary text-white mb-2">Task Name</div>
                    <input type="text" name="title" id="title" class="bg-secondary2 p-3 rounded-sm border-b-4 border-accent font-primary outline-none w-full" placeholder="Enter task title">
                </div>
                <div class="mt-3">
                    <div class="font-primary text-white mb-2">Task Group</div>
                    <select name="group_id" id="group_id" class="bg-secondary2 p-4 font-primary w-full">
                        <option class="font-primary" v-for="group in groupStore.groups" :key="group.id" :value="group.id" :selected="task.group.id === group.id">{{ group.name }}</option>
                    </select>
                </div>
                <div class="mt-3">
                    <div class="font-primary text-white mb-2">Task Deadline</div>
                    <input type="date" name="deadline" id="deadline" class="bg-secondary2 p-3 rounded-sm border-b-4 border-accent font-primary outline-none w-full" pattern="\d{4}-\d{2}-\d{2}">
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
    import { defineEmits } from 'vue'

    const groupStore = useGroupStore()

    const props = defineProps(['task'])
    const emit = defineEmits(['close'])

    function closeModal() {
        emit('close');
    }

    groupStore.initStore()

    // function getGroups() {
    //         axios({
    //             method: 'get',
    //             url: `http://${api_root}/api/groups/`,
    //             auth: {
    //                 name: 'asifemon66@gmail.com',
    //                 password: 'XMtbXX954#'
    //             },
    //             crossDomain:true,
    //         }).then(response => this.groups = response.data)
    // }
    
    // async function updateTask() {
    //         try {
    //             const response = await axios.put(`http://${api_root}/api/tasks/update/${this.task.id}/`, this.editedTask);
    //             console.log("Task updated successfully", response.data);
    //             this.closeModal();
    //             // window.location.href = '/tasks'
    //         } catch (error) {
    //             console.error("Error updating task", error);
    //         }
    //     }

</script>
  