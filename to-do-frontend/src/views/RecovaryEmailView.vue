<template>
    <div class="relative flex flex-grow h-full">
        <div class="m-auto w-full md:w-auto p-10">
            <div class="flex justify-center">
                <RouterLink to="/recover-password" class="text-white font-primary text-lg uppercase px-6 py-2 border-b-4 border-accent bg-secondary2">Recover Password</RouterLink>
            </div>
            <form action="" class="p-6 bg-secondary mt-4 rounded-md shadow-xl" @submit.prevent="sendRecoveryEmail">
                <div class="text-accent font-primary">Recovery Email</div>
                <input type="email"     v-model="email" class="bg-secondary2 outline-none p-2 font-primary text-white rounded-md mt-2 w-full md:w-96" placeholder="Enter your email">
                <div class="text-red-400 mt-4 font-normal" v-if="errors.length">
                    The following error(s) are encountered
                    <div v-for="error in errors" :key="error" class="flex content-center text-sm my-1">
                        <span class="material-icons text-sm mx-3">error_outline</span>{{ error }}
                    </div>
                </div>
                <div class="flex justify-center mt-4">
                    <button type="submit" class="mt-4 px-6 py-2 text-ternary font-primary uppercase text-lg bg-secondary2 rounded-md hover:bg-accent hover:text-primary transition hover:shadow-lg">Send Email</button>
                </div>               
            </form>
        </div>
    </div>
</template>

<script setup>
    import axios from 'axios';
    // import { useUserStore } from '@/stores/user'
    import { ref } from 'vue';
    import router from '../router';

    // const userStore = useUserStore()
    
    const email = ref()
    const errors = ref([])

    async function sendRecoveryEmail() {
        errors.value = []

        if (email.value == undefined || email.value == '' ) {
            errors.value.push('Recovery email is empty')
        }
        if (errors.value.length == 0) {
            await axios
                .post('/api/auth/password-recover/', {'email' : email.value})
                .then(response => {
                    if (response.data.status === 'success') {
                        router.push('/reset-link-sent')
                    }
                    else {
                        errors.value.push(response.data.status)
                    }
                })
                .catch(error => {
                    console.log('error', error)
                })
        }
    }

</script>