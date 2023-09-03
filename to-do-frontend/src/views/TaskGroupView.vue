<script setup>
import Sidebar from '../components/Sidebar.vue'
import TaskGroup from '../components/TaskGroup.vue'
import GroupCreateModal from '../components/GroupCreateModal.vue'
import { useGroupStore } from '@/stores/group'
import { ref } from 'vue'

const groupStore = useGroupStore();

groupStore.initStore();

const isGroupModalOpen = ref(false);
const groups = ref();

groups.value = groupStore.groups

function deleteGroup(id) {
    groups.value = groups.value.filter(groups => groups.id !== id)
}


</script>


<template>
    <div class="relative flex flex-grow h-full">
        <Sidebar/>

        <div class="p-10 mx-auto text-white w-full md:w-auto">
            <div @click="openGroupModal" class="rounded-lg border border-accent py-2 px-4 uppercase font-primary flex content-center justify-center mt-2 mb-6  text-accent cursor-pointer hover:bg-accent hover:text-white transition ease-in md:hidden">
                <span class="material-icons text-md mr-3">add</span>Create new group
            </div>
            <div class="flex flex-row content-center justify-between" v-if="groups.length">
                <div class="text-2xl md:text-3xl font-primary">Task Groups</div>
                <div class="text-ternary text-2xl md:text-3xl font-bd p-0 text-end" v-if="groups.length">{{ groups.length < 10 ? "0" + groups.length : groups.length}}</div>
            </div>

            <div v-else>
                <div class="flex flex-row content-center justify-between">
                    <div class="text-2xl md:text-3xl font-primary">Task Groups</div>
                </div>

                <div class="text-accent text-lg font-primary text-center mt-2">
                    No groups found
                </div>
            </div>

            
            <ul class="mt-5 mb-16">

                <li class="mt-5" v-for="group in groups" v-bind:key="group.id">
                    <TaskGroup :group="group" v-on:delete="deleteGroup"/>
                </li>
            </ul>
        </div>
        <GroupCreateModal v-if="isGroupModalOpen" @close="closeGroupModal"/>
    </div>
</template>


<style scoped>

</style>