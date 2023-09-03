import { defineStore } from "pinia";
import axios from "axios";

export const useGroupStore = defineStore({
    id: 'group',

    state: () => ({
        groups: [],
    }),

    actions: {
        getAllGroups() {
            axios
            .get('/api/task-manager/groups/all/')
            .then(response => {
                // console.log('data', response.data);

                this.groups = response.data
                localStorage.setItem('groups', JSON.stringify(response.data))
            })
            .catch(error => {
                console.log('error', error);
            })
        },
        initStore() {
            this.groups = JSON.parse(localStorage.getItem('groups'))
        },
        getGroupItemCount() {
            this.tasks = JSON.parse(localStorage.getItem('tasks'))
            return this.tasks.title
        },
        getGroup(id) {
            let group = this.groups.filter(groups => groups.id === id)[0]
            return group
        }
    }
})