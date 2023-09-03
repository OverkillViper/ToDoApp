<script setup>
import { useToastStore } from '@/stores/toast'

const store = useToastStore()
</script>

<template>
    <div
        v-if="store.isVisible"
        class="transition ease-in-out delay-500 duration-500 px-3 py-3 fixed right-8 top-full bg-secondary2 rounded-lg shadow-xl font-primary flex content-center"
        :class="store.classes"
    >
        <span class="material-icons text-red-400 mr-3" v-if="store.type == 'error'">error_outline</span>
        <span class="material-icons text-ternary mr-3" v-if="store.type == 'warning'">report_problem</span>
        <span class="material-icons text-accent mr-3"  v-if="store.type == 'info'">lightbulb</span>
        {{ store.message }}
    </div>
</template>