<template>
    <div v-if="isModalOpen" class="fixed top-0 bottom-0 left-0 right-0 bg-primary  flex justify-center content-center">
        <div class="bg-secondary shadow-xl rounded-xl p-10 text-white w-4/5 md:w-2/5 m-auto z-40 ">
            <div class="flex flex-row justify-between content-center">
                <div class="font-primary text-xl mb-4">Edit Group</div>
                <div>
                    <span class="material-icons text-white cursor-pointer" id="close" @click="closeModal">close</span>
                </div>
            </div>
            
            <form class="text-md gap-x-10" v-on:submit.prevent="updateGroup">
                <div class="grid grid-cols-1 md:flex md:flex-row">
                    <div class="mt-3 flex-grow mr-10">
                        <div class="font-primary text-white mb-2">Group Name</div>
                        <input type="text" name="name" id="name"  v-model="name" autocomplete="off" class="bg-secondary2 p-3 rounded-sm border-b-4 border-accent font-primary outline-none w-full" placeholder="Enter group name">
                    </div>
                    <div class="mt-3">
                        <div class="font-primary text-white mb-2">Group Color</div>
                        <div class="text-center">
                            <color-input v-model="color" />
                        </div>
                    </div>
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

    <div class="bg-secondary rounded-xl p-5">
        <div class="font-primary text-lg flex flex-row justify-between content-center">
            <div class="flex flex-row">
                <div class="px-4 py-0 rounded-md mr-4" :style="{ backgroundColor: group.color }">&nbsp</div>
                <RouterLink :to="{ name: 'GroupDetails', params: { groupId: group.id } }">{{ group.name }}</RouterLink>
            </div>
            <div class="hidden md:block">
                <span href="#"><span class="material-icons text-accent text-md mr-4 cursor-pointer" @click="openModal">edit</span></span>
                <span @click="deleteGroup"><span class="material-icons text-accent text-md cursor-pointer">delete</span></span>
            </div>
        </div>
        <div class="font-primary text-lg flex flex-row justify-between content-center">
            <div class="flex flex-row md:mr-96">
                <div class="px-4 py-0 rounded-md bg-secondary mr-4">&nbsp</div>
                <div>
                    <div class="font-normal text-ternary text-sm">Total items in group</div>
                    <div class="text-2xl text-accent">{{ groupItemCount < 10 ? "0" + groupItemCount : groupItemCount }}</div>
                </div>
            </div>
        </div>

        <div class="text-end md:hidden">
            <span href="#"><span class="material-icons text-accent text-md mr-4 cursor-pointer" @click="openModal">edit</span></span>
            <span @click="deleteGroup"><span class="material-icons text-accent text-md">delete</span></span>
        </div>
    </div>
</template>

<script setup>
    import { ref } from 'vue'
    import ColorInput from 'vue-color-input'
    import { useGroupStore } from '@/stores/group'
    import axios from 'axios';

    const isModalOpen = ref(false);
    const groupItemCount = ref(0);

    const groupStore = useGroupStore();

    const props = defineProps(['group'])
    const emit = defineEmits(['delete'])

    function openModal() {
        isModalOpen.value = true;
    }

    function closeModal() {
        isModalOpen.value= false;
    }

    const name = ref();
    const color = ref();

    name.value     = props.group.name
    color.value    = props.group.color

    function updateGroup() {
        props.group.name    = name.value
        props.group.color   = color.value

        axios
            .post('api/task-manager/groups/update/'+props.group.id, {
                'name'    : name.value,
                'color'   : color.value
            })
            .then(response => {
                console.log('data', response.data);
                
                closeModal()
                groupStore.getAllGroups()

            })
            .catch(error => {
                console.log('error', error);
            })

        closeModal()
    }

    function deleteGroup() {
        emit('delete', props.group.id);

        axios
            .delete(`api/task-manager/groups/delete/`+props.group.id)
            .then(response => {
                console.log(response.data);
                groupStore.getAllGroups()
            })
            .catch(error => {
                console.log('error', error);
            })
    }

</script>