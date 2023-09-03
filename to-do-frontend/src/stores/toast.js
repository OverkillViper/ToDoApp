import { defineStore } from 'pinia'

export const useToastStore = defineStore({
    id: 'toast',

    state: () => ({
        ms          : 0,
        message     : '',
        classes     : '',
        isVisible   : false,
        type        : 'error'
    }),

    actions: {
        showToast(ms, message, type) {
            this.ms         = parseInt(ms)
            this.message    = message
            this.isVisible  = true
            this.type       = type

            if (type == 'warning') {
                this.classes += 'text-ternary'
            }
            else if (type == 'error') {
                this.classes += 'text-red-400'
            }
            else if (type == 'info') {
                this.classes += 'text-accent'
            }

            setTimeout(() => {
                this.classes += ' -translate-y-28'
            }, 10)

            setTimeout(() => {
                this.classes = this.classes.replace('-translate-y-28', '')
            }, this.ms - 500)

            setTimeout(() => {
                this.isVisible = false
            }, this.ms)
        }
    }
})