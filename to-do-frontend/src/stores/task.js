import { defineStore } from 'pinia'
import axios from 'axios'

export const useTaskStore = defineStore({
    id: 'task',

    state: () => ({
        tasks: [],
        pendingTasks: [],
        completedTasks: [],
        todaysTasks: [],
        groupTasks: []
    }),

    actions: {
        getAllTasks() {
            axios
            .get('/api/task-manager/tasks/all/')
            .then(response => {
                // console.log('data', response.data);

                localStorage.setItem('tasks', JSON.stringify(response.data))
            })
            .catch(error => {
                console.log('error', error);
            })
        },

        getPendingTasks() {
            axios
            .get('/api/task-manager/tasks/pending/')
            .then(response => {
                // console.log('data', response.data);

                localStorage.setItem('pendingTasks', JSON.stringify(response.data))
            })
            .catch(error => {
                console.log('error', error);
            })
        },

        getCompletedTasks() {
            axios
            .get('/api/task-manager/tasks/complete/')
            .then(response => {
                // console.log('data', response.data);

                localStorage.setItem('completedTasks', JSON.stringify(response.data))
            })
            .catch(error => {
                console.log('error', error);
            })
        },

        getTodaysTasks() {
            axios
            .get('/api/task-manager/tasks/today/')
            .then(response => {
                // console.log('data', response.data);

                localStorage.setItem('todaysTasks', JSON.stringify(response.data))
            })
            .catch(error => {
                console.log('error', error);
            })
        },

        initStore() {
            this.tasks          = JSON.parse(localStorage.getItem('tasks'))
            this.pendingTasks   = JSON.parse(localStorage.getItem('pendingTasks'))
            this.completedTasks = JSON.parse(localStorage.getItem('completedTasks'))
            this.todaysTasks    = JSON.parse(localStorage.getItem('todaysTasks'))

            // return this.tasks
        },

        getGroupTasks(id) {
            this.groupTasks = this.tasks.filter(tasks => tasks.group.id === id)
        }
    }
})