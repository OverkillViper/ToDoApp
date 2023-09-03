<template>
    <div class="fixed top-0 bottom-0 left-0 right-0 bg-primary  flex justify-center content-center">
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
                        <input type="text" name="name" id="name"  v-model="groupName" autocomplete="off" class="bg-secondary2 p-3 rounded-sm border-b-4 border-accent font-primary outline-none w-full" placeholder="Enter group name">
                    </div>
                    <div class="mt-3">
                        <div class="font-primary text-white mb-2">Group Color</div>
                        <div class="text-center">
                            <color-input v-model="groupColor" />
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

</template>


<script>
import axios from 'axios'
import ColorInput from 'vue-color-input'

const api_root = import.meta.env.VITE_ROOT_API

export default {
    components: {
        ColorInput
    },
    methods: {
        closeModal() {
            this.$emit('close');
        },
        async updateGroup() {
            try {
                const response = await axios.put(`http://${api_root}/api/groups/update/${this.group.id}/`, {
                    name: this.groupName,
                    color: this.groupColor
                });
                
                console.log("Group updated successfully", response.data);
                this.closeModal()
                // window.location.href = '/groups'
            } catch (error) {
                console.error("Error updating group", error);
            }
        }
    },
    data() {
        return {
            groupName: this.group.name,
            groupColor: this.group.color
        }
    },
    props: {
        group: Object,
    }
}
</script>
  