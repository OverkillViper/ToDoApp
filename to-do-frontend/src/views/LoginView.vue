<template>
    <div class="relative flex flex-grow h-full">
        <div class="m-auto w-full md:w-auto p-10">
            <div class="flex justify-center">
                <RouterLink to="/login" class="text-white font-primary text-lg uppercase px-6 py-2 border-b-4 border-accent bg-secondary2">Sign In</RouterLink>
                <RouterLink to="/register" class="text-white font-primary text-lg uppercase px-6 py-2 ">Sign up</RouterLink>
            </div>
            <form action="" class="p-6 bg-secondary mt-4 rounded-md shadow-xl" @submit.prevent="signin">
                <div class="text-accent font-primary">Email</div>
                <input type="email"     v-model="form.email" class="bg-secondary2 outline-none p-2 font-primary text-white rounded-md mt-2 w-full md:w-96" placeholder="Enter your email">
                <div class="text-accent font-primary mt-4">Password</div>
                <input type="password"  v-model="form.password" class="bg-secondary2 outline-none p-2 font-primary text-white rounded-md mt-2 w-full md:w-96" placeholder="Enter your password">
                <div class="text-red-400 mt-4 font-normal" v-if="errors.length">
                    The following error(s) are encountered
                    <div v-for="error in this.errors" :key="error" class="flex content-center text-sm my-1">
                        <span class="material-icons text-sm mx-3">error_outline</span>{{ error }}
                    </div>
                </div>
                <div class="flex justify-center mt-4">
                    <button type="submit" class="mt-4 px-6 py-2 text-ternary font-primary uppercase text-lg bg-secondary2 rounded-md hover:bg-accent hover:text-primary transition hover:shadow-lg">Sign In</button>
                </div>
                <div class="font-normal text-white mt-6 flex justify-center">
                    <div class="mr-2">Forgot your password?</div>
                    <RouterLink class="underline font-primary" to="/recover-password">Recover It!</RouterLink>
                </div>
                <div class="text-center font-primary text-ternary">OR</div>
                <div class="font-normal text-white flex justify-center">
                    <div class="mr-2">Don't have an account?</div>
                    <RouterLink class="underline font-primary" to="/register">Create One</RouterLink>
                </div>

                
            </form>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import { useUserStore } from '@/stores/user'

    export default {
        setup() {
            const userStore = useUserStore()

            return {
                userStore
            }
        },
        data() {
            return {
                form: {
                    email   : '',
                    password: ''
                },
                errors: [],
            }
        },
        methods: {
            async signin() {
                this.errors = []

                if (this.form.email === '') {
                    this.errors.push('The email is empty')
                }
                if (this.form.password === '') {
                    this.errors.push('Password is empty')
                }
                if (this.errors.length === 0) {
                    await axios
                        .post('/api/auth/login/', this.form)
                        .then(response => {
                            this.userStore.setToken(response.data)
                            axios.defaults.headers.common["Authorization"] = "Bearer " + response.data.access;
                        })
                        .catch(error => {
                            console.log('error', error)
                            this.errors.push('The email or password is incorrect!')
                            this.errors.push('Or the user may not exist!')
                        })

                    await axios
                        .get('/api/auth/me/')
                        .then(response => {
                            console.log(response.data);
                            this.userStore.setUserInfo(response.data)

                            this.$router.push(this.userStore.returnUrl || '/')
                        })
                        .catch(error => {
                            console.log('error', error)
                        })
                }
            }
        }
    }
</script>