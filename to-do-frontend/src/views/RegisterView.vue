<template>
    <div class="relative flex flex-grow h-full">
        <div class="m-auto w-full md:w-auto p-10">
            <div class="flex justify-center">
                <router-link to="/login" class="text-white font-primary text-lg uppercase px-6 py-2">Sign In</router-link>
                <router-link to="/register" class="text-white font-primary text-lg uppercase px-6 py-2  border-b-4 border-accent bg-secondary2">Sign up</router-link>
            </div>
            <form action="" class="p-6 bg-secondary mt-4 rounded-md shadow-xl" @submit.prevent="signup">
                <div class="text-accent font-primary">Email</div>
                <input type="text"         v-model="form.email" class="bg-secondary2 outline-none p-2 font-primary text-white rounded-md mt-2 w-full md:w-96" placeholder="Enter a valid email">
                <div class="text-accent font-primary mt-4">Username</div>
                <input type="text"          v-model="form.name" class="bg-secondary2 outline-none p-2 font-primary text-white rounded-md mt-2 w-full md:w-96" placeholder="Enter your name">
                <div class="text-accent font-primary mt-4">Password</div>
                <input type="password"      v-model="form.password1" class="bg-secondary2 outline-none p-2 font-primary text-white rounded-md mt-2 w-full md:w-96" placeholder="Must be 8 charecter long">
                <div class="text-accent font-primary mt-4">Confirm Password</div>
                <input type="password"      v-model="form.password2"    class="bg-secondary2 outline-none p-2 font-primary text-white rounded-md mt-2 w-full md:w-96" placeholder="Must match with original">
                <div class="text-red-400 mt-4 font-normal" v-if="errors.length">
                    The following error(s) are encountered
                    <div v-for="error in this.errors" :key="error" class="flex content-center text-sm my-1">
                        <span class="material-icons text-sm mx-3">error_outline</span>{{ error }}
                    </div>
                </div>
                <div class="flex justify-center mt-4">
                    <button type="submit" class="mt-4 px-6 py-2 text-ternary font-primary uppercase text-lg bg-secondary2 rounded-md hover:bg-accent hover:text-primary transition hover:shadow-lg">Sign Up</button>
                </div>
                <div class="font-normal text-white flex justify-center mt-4">
                    <div class="mr-2">Already have an account?</div>
                    <RouterLink class="underline font-primary" to="/login">Sign In</RouterLink>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { useToastStore } from '@/stores/toast'

export default {
    setup() {
        const toastStore = useToastStore()

        return {
            toastStore
        }
    },
    data() {
        return {
            form: {
                email       : '',
                name        : '',
                password1   : '',
                password2   : ''
            },
            errors: [],
        }
    },

    methods: {
        signup() {
            this.errors = []

            if (this.form.email === '') {
                this.errors.push('The email is empty')
            }

            if(this.form.name === '') {
                this.errors.push('The name is empty')
            }

            
            if (this.form.password1 === '') {
                this.errors.push('Password is empty')
            }

            if (this.form.password1.length < 8) {
                this.errors.push('Password must be 8 charecter long')
            }

            if (this.form.password1 !== this.form.password2) {
                this.errors.push('The passwords does not match')
            }

            if (this.errors.length === 0) {
                axios
                    .post('/api/auth/signup/', this.form)
                    .then(response => {
                        if (response.data.message === 'success') {
                            this.toastStore.showToast(5000, 'The user is registered. Please log in', 'info')
                            console.log('The user is registered. Please log in')

                            this.form.email = ''
                            this.form.name = ''
                            this.form.password1 = ''
                            this.form.password2 = ''
                        } else {
                            this.toastStore.showToast(5000, 'Something went wrong. Please try again', 'error')
                            for(let i = 0; i < response.data.error.password2.length; i++) {
                                this.errors.push(response.data.error.password2[i])
                            }
                        }
                    })
                    .catch(error => {
                        console.log('error', error)
                    })
            }
        }
    }
}


</script>