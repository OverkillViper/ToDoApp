<script>
import TaskGroup from '../components/TaskGroup.vue'
import GroupCreateModal from '../components/GroupCreateModal.vue'
import axios from 'axios'

const api_root = import.meta.env.VITE_ROOT_API

export default {
    components: {
        TaskGroup,
        GroupCreateModal
    },
    data() {
        return {
            isGroupModalOpen: false,
            groups: []
        };
    },
    mounted() {
        this.getGroups()
    },
    updated() {
        this.getGroups()
    },
    methods: {
        openGroupModal() {
            this.isGroupModalOpen = true;
        },
        closeGroupModal() {
            this.isGroupModalOpen = false;
        },
        getGroups() {
            axios({
                method: 'get',
                url: `http://${api_root}/api/groups/`,
                auth: {
                    name: 'asifemon66@gmail.com',
                    password: 'XMtbXX954#'
                },
                crossDomain:true,
            }).then(response => this.groups = response.data)
        },
    }
}

</script>


<template>     
    <div class="p-10 mx-auto text-white w-full md:w-auto">
        <div @click="openGroupModal" class="rounded-lg border border-accent py-2 px-4 uppercase font-primary flex content-center justify-center mt-2 mb-6  text-accent cursor-pointer hover:bg-accent hover:text-white transition ease-in md:hidden">
            <span class="material-icons text-md mr-3">add</span>Create new group
        </div>
        <div class="flex flex-row content-center justify-between">
            <div class="text-2xl md:text-3xl font-primary">Task Groups</div>
            <div class="text-ternary text-2xl md:text-3xl font-bd p-0 text-end">{{ this.groups.length < 10 ? "0" + this.groups.length : this.groups.length}}</div>
        </div>
        
        <ul class="mt-5 mb-16">

            <li class="mt-5" v-for="group in groups" v-bind:key="group.id">
                <TaskGroup :group="group" />
            </li>
        </ul>
    </div>
    <GroupCreateModal v-if="isGroupModalOpen" @close="closeGroupModal"/>
</template>

<style scoped>

</style>