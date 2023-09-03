<template>
    <div class="relative flex flex-grow h-full">
        <div class="m-auto w-full md:w-auto p-10">
            <div class="flex justify-center">
                <RouterLink to="/reset-password" class="text-white font-primary text-lg uppercase px-6 py-2 border-b-4 border-accent bg-secondary2">Reset Password</RouterLink>
            </div>
            <form action="" class="p-6 bg-secondary mt-4 rounded-md shadow-xl" @submit.prevent="ResetPassword">
                <input type="hidden" v-model="token">
                <div class="text-accent font-primary">New Password</div>
                <input type="password"     v-model="password1" class="bg-secondary2 outline-none p-2 font-primary text-white rounded-md mt-2 w-full md:w-96 md:min-w-full" placeholder="Enter your new password">
                <div class="text-accent font-primary mt-4">Confirm Password</div>
                <input type="password"     v-model="password2" class="bg-secondary2 outline-none p-2 font-primary text-white rounded-md mt-2 w-full md:w-96 md:min-w-full" placeholder="Confirm your new password">
                <div class="text-red-400 mt-4 font-normal" v-if="errors.length">
                    The following error(s) are encountered
                    <div v-for="error in errors" :key="error" class="flex content-center text-sm my-1">
                        <span class="material-icons text-sm mx-3">error_outline</span>{{ error }}
                    </div>
                </div>
                <div class="flex justify-center mt-4">
                    <button type="submit" class="mt-4 px-6 py-2 text-ternary font-primary uppercase text-lg bg-secondary2 rounded-md hover:bg-accent hover:text-primary transition hover:shadow-lg">Change Password</button>
                </div>               
            </form>
        </div>
    </div>
</template>

<script setup>
    import axios from 'axios';
    import { ref } from 'vue';
    import { useRoute } from 'vue-router'
    import router from '../router';

    const route = useRoute()
    
    const password1 = ref()
    const password2 = ref()
    const token = ref()
    token.value = route.query.token;
    const errors = ref([])

    async function ResetPassword() {
        errors.value = []

        if (password1.value == undefined || password1.value == '' ) {
            errors.value.push('New password is empty')
        }
        else if (password2.value == undefined || password2.value == '' ) {
            errors.value.push('Confirm password is empty')
        }
        else if (password1.value.length < 8 || password2.value.length < 8 ) {
            errors.value.push('Password must be 8 charecter long')
        }
        else if (password1.value !== password2.value ) {
            errors.value.push('Passwords did not match')
        }
        
        if (errors.value.length === 0) {
            await axios
            .post('/api/auth/password-reset/', {
                'token'     : token.value,
                'password'  : password1.value
            })
            .then(response => {
                if (response.data.status === 'success') {
                    console.log(response.data.status);
                    router.push('/reset-complete')
                }
                else {
                    errors.value.push(response.data.error)
                }
            })
            .catch(error => {
                console.log('error', error)
            })
        }

    }

</script>