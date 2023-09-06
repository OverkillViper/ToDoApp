<script setup>
    import { useUserStore } from '@/stores/user'
    import { useTaskStore } from '@/stores/task'
    import { RouterLink } from 'vue-router';
    import router from '../router';
    import { ref } from 'vue';
    import axios from 'axios';

    const userStore = useUserStore()
    const taskStore = useTaskStore()

    userStore.initStore();
    taskStore.initStore();

    function calculateDaysRemaining(deadline) {
        const today = new Date();
        const deadlineDate = new Date(deadline);
        const timeDifference = deadlineDate.getTime() - today.getTime();
        const daysRemaining = Math.ceil(timeDifference / (1000 * 60 * 60 * 24));

        return daysRemaining >= 0 ? daysRemaining : 0;
    }

    let missedTasksCount = 0;
    let pendingTaskCount = 0;
    
    const errors = ref([])
    const avatarErrors = ref([])
    const isDeleteModalOpen = ref(false);
    const isAvatarModalOpen = ref(false);
    const showUsernameEdit = ref(false)
    const imgsrc = ref()
    const avatar = ref()
    const username = ref()

    username.value = userStore.user.name

    if(userStore.user.avatar === null) {
        imgsrc.value = '/user.png'
    }
    else {
        imgsrc.value = userStore.user.avatar
    }

    let validAvatarTypes = ['image/png', 'image/jpg', 'image/jpeg', 'image/gif']

    function imageSelected(event) {
        avatarErrors.value = []
        if (event.target.files[0].size > 2097152) {
            avatarErrors.value.push('Image size exceeded 2MB limit')
        }
        if (!validAvatarTypes.includes(event.target.files[0].type)) {
            avatarErrors.value.push('Invalid image type. Valid types are: .png, .jpg, .jpeg & .gif')
        }

        if (avatarErrors.value.length == 0) {
            imgsrc.value = URL.createObjectURL(event.target.files[0])

            avatar.value = event.target.files[0]

        }
    }

    async function changeAvatar() {
        let formData = new FormData()
        formData.append('avatar', avatar.value)

        await axios
            .post('/api/auth/upload-avatar/', formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                }
            })
            .then(response => {
                if (response.data.status === 'success') {
                    userStore.setUserInfo({
                        id:     userStore.user.id,
                        name:   userStore.user.name,
                        email:  userStore.user.email,
                        avatar: response.data.user.get_avatar
                    });
                    avatar.value = response.data.user.get_avatar
                    userStore.initStore()
                    closeAvatarModal()
                }
                else {
                    errors.value.push(response.data.error)
                }
            })
            .catch(error => {
                errors.value.push(error)
            })
    }

    async function changeUsername() {
        await axios
            .post('/api/auth/change-username/', {
                'name' : username.value
            })
            .then(response => {
                if (response.data.status === 'success') {
                    userStore.setUserInfo({
                        id:     userStore.user.id,
                        name:   username.value,
                        email:  userStore.user.email,
                        avatar: userStore.user.avatar
                    });
                    userStore.initStore()
                    hideUsernameEditor()
                }
                else {
                    errors.value.push(response.data.error)
                }
            })
            .catch(error => {
                errors.value.push(error)
            })
    }
    
    function showUsernameEditor() {
        showUsernameEdit.value = true
    }

    function hideUsernameEditor() {
        showUsernameEdit.value = false
    }

    function openDeleteModal() {
        isDeleteModalOpen.value = true;
    }

    function closeDeleteModal() {
        isDeleteModalOpen.value= false;
    }

    function openAvatarModal() {
        isAvatarModalOpen.value = true;
    }

    function closeAvatarModal() {
        isAvatarModalOpen.value= false;
    }

    for (let i = 0; i < taskStore.tasks.length; i++) {
        if((calculateDaysRemaining(taskStore.tasks[i].deadline) == 0) && (taskStore.tasks[i].status == 'pending')) {
            missedTasksCount++;
        }
        if((calculateDaysRemaining(taskStore.tasks[i].deadline) != 0) && (taskStore.tasks[i].status == 'pending')) {
            pendingTaskCount++;
        }
    }

    function logout() {
        console.log('Log out')

        userStore.removeToken()

        router.push('/')
    }

    async function deleteAccount() {
        errors.value = []
        await axios
            .delete('/api/auth/delete-user/')
            .then(response => {
                if (response.data.status === 'User deleted successfully') {
                    console.log(response.data.status);
                    userStore.removeToken()
                    router.push('/register')
                }
                else {
                    console.log(response.data.error);
                    errors.value.push(response.data.error)
                }
            })
            .catch(error => {
                errors.value.push(error.response.data.detail)
            })
    }
</script>

<template>
    <div class="mx-auto mt-10 w-full md:w-3/4 2xl:w-2/3 px-10">
        <!-- Avatar modal -->
        <!-- <div class="fixed top-0 bottom-0 left-0 right-0 bg-primary  flex justify-center content-center" v-if="isAvatarModalOpen">
            <div class="bg-secondary shadow-2xl rounded-2xl p-10 text-white w-4/5 md:w-2/5 m-auto z-40 ">
                <div class="flex flex-row justify-between content-center">
                    <div class="font-primary text-2xl mb-4 flex content-center">Change Avatar</div>
                    <div>
                        <span class="material-icons text-white cursor-pointer" id="close" @click="closeAvatarModal">close</span>
                    </div>
                </div>

                
                <form action="" v-on:submit.prevent="changeAvatar">
                    <div class="md:flex">
                        <input type="file" ref="file" @change="imageSelected" class="inputfile" id="avatar" accept="image/*">
                        <label for="avatar" class="bg-accent font-primary px-4 py-2 text-black rounded-md flex content-center cursor-pointer">
                            <span class="material-icons mr-2 text-md">upload</span>Choose Avatar
                        </label>
                    </div>

                    <div v-for="error in avatarErrors" :key="error" class="flex content-center text-sm my-1 text-red-400 mt-4 font-normal">
                        <span class="material-icons text-sm mx-3">error_outline</span>{{ error }}
                    </div>

                    <div class="flex justify-center mt-6 w-4/5 mx-auto">
                        <div style="overflow: hidden;" class="rounded-full aspect-square object-cover">
                            <img :src="imgsrc" alt="avatar preview">
                        </div>
                    </div>
                    <div class="flex mt-6 justify-center md:justify-end">
                        <button class="bg-ternary px-4 py-2 font-primary text-black text-md flex content-center rounded-md mx-2 cursor-pointer" type="submit">
                            <span class="material-icons mr-2 text-md">check</span>Save
                        </button>
                    </div>
                </form>

                
            </div>
        </div> -->

        <!-- Delete modal -->
        <div class="fixed top-0 bottom-0 left-0 right-0 bg-primary  flex justify-center content-center" v-if="isDeleteModalOpen">
            <div class="bg-secondary shadow-2xl rounded-2xl p-10 text-white w-4/5 md:w-2/5 m-auto z-40 ">
                <div class="flex flex-row justify-between content-center">
                    <div class="font-primary text-2xl mb-4 flex content-center">Delete account</div>
                    <div>
                        <span class="material-icons text-white cursor-pointer" id="close" @click="closeDeleteModal">close</span>
                    </div>
                </div>

                <div class="font-normal">
                    Are you sure want to delete your account?
                </div>
                <div class="flex content-center mt-4 font-normal">
                    <span class="material-icons mr-3 text-md">warning</span> This action is irreversable.
                </div>
                <div v-for="error in errors" :key="error" class="flex content-center text-sm my-1 text-red-400 font-normal">
                    <span class="material-icons text-sm mx-3">error_outline</span>{{ error }}
                </div>
                <div class="flex mt-6 justify-center md:justify-end">
                    <div class="bg-secondary2 px-4 py-2 font-primary text-white text-md flex content-center rounded-md mx-2 cursor-pointer" @click="closeDeleteModal">
                        <span class="material-icons mr-2 text-md">close</span>Cancel
                    </div>
                    <div class="bg-red-300 px-4 py-2 font-primary text-black text-md flex content-center rounded-md mx-2 cursor-pointer" @click="deleteAccount">
                        <span class="material-icons mr-2 text-md">delete</span>Delete
                    </div>
                </div>
            </div>
        </div>

        <!-- Main content -->
        <div class="grid grid-cols-1 md:grid-cols-3 md:gap-6">
            <div class="col-span-1">
                <!-- <div class="flex justify-center">
                    <div class="rounded-full" style="overflow: hidden;">
                        <img :src="userStore.user.avatar" alt="user_dp" class="w-32 p-0 m-0 aspect-square object-cover">
                    </div>
                </div>
                <div class="w-auto flex justify-center">
                    <div class="rounded-full py-2 px-4 bg-secondary2 text-sm text-ternary flex mt-5 font-normal" @click="openAvatarModal">
                        <span class="material-icons text-sm mr-3">edit</span>Change photo
                    </div>
                </div> -->
                <div class="text-sm font-normal text-ternary mt-6 ext-left">Welcome</div>
                <form action="" v-on:submit.prevent="changeUsername" v-if="showUsernameEdit" class="grid grid-cols-4">
                    <div class="col-span-3">
                        <input type="text" name="username" id="username" v-model="username" class="font-primary text-xl md:text-2xl 2xl:text-4x1 text-white py-1 border-ternary border-b-2 bg-primary w-full outline-none">
                    </div>
                    <div class="flex justify-center py-2 col-span-1 gap-x-1">
                        <div class="bg-secondary2 text-white px-2 py-1 grid content-center rounded-md cursor-pointer" @click="hideUsernameEditor">
                            <span class="material-icons text-sm">close</span>
                        </div>
                        <button class="bg-secondary2 text-white px-2 py-1 grid content-center rounded-md cursor-pointer" type="submit">
                            <span class="material-icons text-sm">check</span>
                        </button>
                    </div>
                </form>
                <div class="grid grid-cols-4" v-else>
                    <div class="font-primary text-xl md:text-2xl 2xl:text-4x1 text-white text-left col-span-3 py-1">
                        {{ username }}
                    </div>
                    
                    <div class="flex justify-center py-2 col-span-1">
                        <div class="bg-secondary2 text-white px-2 py-1 grid content-center rounded-md cursor-pointer" @click="showUsernameEditor">
                            <span class="material-icons text-sm">edit</span>
                        </div>
                    </div>
                </div>

                <div class="text-accent text-left">
                    {{ userStore.user.email }}
                </div>

                <div class="w-auto flex justify-center md:mt-10">
                    <div class="rounded-full py-2 px-4 bg-secondary2 text-sm text-ternary flex mt-5 font-normal cursor-pointer" @click="logout">
                        <span class="material-icons text-sm mr-3">power_settings_new</span>Sign Out
                    </div>
                </div>
            </div>
            <div class="col-span-2 rounded-md bg-secondary p-8 mt-10 md:mt-0 text-white">
                <!-- Task Statistics -->
                <div class="font-primary text-xl">Task Statistics</div>
                <div class="font-normal text-center my-4 md:my-2"><span class="text-ternary font-primary mr-2">{{ taskStore.tasks.length < 10 ? "0" + taskStore.tasks.length : taskStore.tasks.length }}</span>Total Tasks</div>
                <div class="md:flex rounded-md mt-2 hidden" style="overflow: hidden;">
                    <div class="text-center text-black font-primary bg-accent"      :style="{width: taskStore.completedTasks.length != 0 ? ( taskStore.completedTasks.length / taskStore.tasks.length )*100+'%' : 33.33+'%'}">{{ taskStore.completedTasks.length }}</div>
                    <div class="text-center text-white font-primary bg-secondary2"  :style="{width: pendingTaskCount != 0 ? ( pendingTaskCount / taskStore.tasks.length )*100+'%' : 33.33+'%'}">{{ pendingTaskCount }}</div>
                    <div class="text-center text-black font-primary bg-red-300"     :style="{width: missedTasksCount != 0 ? ( missedTasksCount / taskStore.tasks.length )*100+'%' : 33.33+'%'}">{{ missedTasksCount }}</div>
                </div>
                <div class="md:flex rounded-md mt-2 hidden" style="overflow: hidden;">
                    <div class="text-center text-white font-normal text-sm" :style="{width: taskStore.completedTasks.length != 0 ? ( taskStore.completedTasks.length / taskStore.tasks.length )*100+'%' : 33.33+'%'}">Completed Tasks</div>
                    <div class="text-center text-white font-normal text-sm" :style="{width: pendingTaskCount != 0 ? ( pendingTaskCount / taskStore.tasks.length )*100+'%' : 33.33+'%'}">Pending Tasks</div>
                    <div class="text-center text-white font-normal text-sm" :style="{width: missedTasksCount != 0 ? ( missedTasksCount / taskStore.tasks.length )*100+'%' : 33.33+'%'}">Missed Tasks</div>
                </div>
                <div class="py-2 px-4 bg-accent rounded-md md:hidden font-primary text-black mb-4">
                    {{ taskStore.completedTasks.length }} Completed Tasks
                </div>
                <div class="py-2 px-4 bg-secondary2 rounded-md md:hidden font-primary text-white mb-4">
                    {{ pendingTaskCount }} Pending Tasks
                </div>
                <div class="py-2 px-4 bg-red-300 rounded-md md:hidden font-primary text-black mb-4">
                    {{ missedTasksCount }} Missed Tasks
                </div>

                <!-- change password -->
                <hr class="my-4 border-ternary">
                <div class="grid grid-cols-1 md:flex justify-between font-normal py-2">
                    <div>Dont like your password?</div>
                    <div class="mt-6 md:mt-0">
                        <RouterLink to="/change-password" class="bg-secondary2 px-6 py-3 rounded-md shadow-md text-sm font-primary">Change Password</RouterLink>
                    </div>
                </div>

                <!-- Delete account -->
                <hr class="my-4 border-ternary">
                <div class="grid grid-cols-1 md:flex justify-between font-normal py-2">
                    <div>Getting Bored?</div>
                    <div class="mt-6 md:mt-0">
                        <div @click="openDeleteModal" class="bg-red-300 text-black px-6 py-3 rounded-md shadow-md text-sm font-primary cursor-pointer">Delete Account</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
    .inputfile {
        width: 0.1px;
        height: 0.1px;
        opacity: 0;
        overflow: hidden;
        position: absolute;
        z-index: -1;
    }
    /* .inputfile + label {
        font-size: 1.25em;
        font-weight: 700;
        color: white;
        background-color: black;
        display: inline-block;
    }

    .inputfile:focus + label,
    .inputfile + label:hover {
        background-color: red;
    } */
</style>
