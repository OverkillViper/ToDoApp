<template>
    <div class="relative flex flex-grow h-full">
        <div class="m-auto w-full md:w-auto p-10">
            <div class="flex justify-center">
                <RouterLink to="/recover-password" class="text-white font-primary text-lg uppercase px-6 py-2 border-b-4 border-accent bg-secondary2">Reset Link Sent</RouterLink>
            </div>
            <div class="mt-10 font-primary text-white text-md md:text-xl max-w-md text-center">
                A password reset link has been sent to the provided email address. Please check your spam folder if you do not find the email.
            </div>
        </div>
    </div>
</template>

<script setup>

</script>