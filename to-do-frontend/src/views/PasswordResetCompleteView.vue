<template>
    <div class="relative flex flex-grow h-full">
        <div class="m-auto w-full md:w-auto p-10">
            <div class="flex justify-center">
                <RouterLink to="/recover-password" class="text-white font-primary text-lg uppercase px-6 py-2 border-b-4 border-accent bg-secondary2">Password Reset Complete</RouterLink>
            </div>
            <div class="mt-10 font-primary text-white text-md md:text-xl max-w-md text-center">
                Your password is successfully changed. Please <RouterLink to="/login" class="underline">Sign in</RouterLink> with your new password.
            </div>
        </div>
    </div>
</template>

<script setup>
import { RouterLink } from 'vue-router';


</script>