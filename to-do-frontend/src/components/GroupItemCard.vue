<template>
    <router-link :to="{ name: 'GroupDetails', params: { groupId: group.id } }" class="flex flex-row content-center justify-between text-white p-1">
        <div class="font-normal text-md p-2 flex flex-row content-center mr-7 hover:underline underline-offset-4 decoration-2"><div class="px-3 mr-3 rounded-full" :style="{ backgroundColor: group.color }"></div>{{ group.name}}</div>
        <div class="font-primary text-md text-accent py-2 px-3 rounded-lg content-center">{{ groupItemCount < 10 ? "0" + groupItemCount : groupItemCount }}</div>
    </router-link>
</template>

<script setup>
    import { ref } from 'vue'
    import { useGroupStore } from '@/stores/group'

    const groupItemCount = ref(0)

    const props = defineProps(['group'])
    const groupStore    = useGroupStore()

    // console.log("Task title: ", groupStore.getGroupItemCount())

</script>