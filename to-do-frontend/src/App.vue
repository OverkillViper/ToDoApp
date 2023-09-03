<template>
    <Navbar/>
    <Toast />
    <div class="flex flex-col flex-grow">
        <RouterView :key='$route.path'/>
    </div>
</template>

<script setup>
    import { RouterLink, RouterView } from 'vue-router'
    import Navbar from './components/Navbar.vue'
    import Toast from '@/components/Toast.vue'

</script>

<style scoped>

</style>
