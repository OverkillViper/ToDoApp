import { createRouter, createWebHistory } from 'vue-router'
import LandingPageView                    from '../views/LandingPageView.vue'
import PendingTasksView                   from '../views/PendingTasksView.vue'
import CompletedTasksView                 from '../views/CompletedTasksView.vue'
import TodaysTasksView                    from '../views/TodaysTasksView.vue'
import AllTasksView                       from '../views/AllTasksView.vue'
import TaskGroupView                      from '../views/TaskGroupView.vue'
import GroupDetailsView                   from '../views/GroupDetailsView.vue'
import LoginView                          from '../views/LoginView.vue'
import RegisterView                       from '../views/RegisterView.vue'
import ProfileView                        from '../views/ProfileView.vue'
import RecovaryEmailView                  from '../views/RecovaryEmailView.vue'
import ResetPasswordView                 from '../views/ResetPasswordView.vue'
import RecovaryEmailSentView              from '../views/RecovaryEmailSentView.vue'
import PasswordResetCompleteView          from '../views/PasswordResetCompleteView.vue'
import ChangePasswordView                 from '../views/ChangePasswordView.vue'

import { useUserStore } from '@/stores/user'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'Home',
            component: LandingPageView
        },
        {
            path: '/tasks',
            name: 'Tasks',
            component: AllTasksView,
            meta: {
                requiresAuth: true
            }   
        },
        {
            path: '/pending-tasks',
            name: 'PendingTasks',
            component: PendingTasksView
        },
        {
            path: '/completed-tasks',
            name: 'CompletedTask',
            component: CompletedTasksView
        },
        {
            path: '/todays-tasks',
            name: 'TodaysTask',
            component: TodaysTasksView
        },
        {
            path: '/groups',
            name: 'Groups',
            component: TaskGroupView
        },
        {
            path: '/groups-details/:groupId',
            name: 'GroupDetails',
            component: GroupDetailsView,
            props: true
        },
        {
            path: '/login',
            name: 'Login',
            component: LoginView
        },
        {
            path: '/register',
            name: 'Register',
            component: RegisterView
        },
        {
            path: '/profile',
            name: 'Profile',
            component: ProfileView
        },
        {
            path: '/recover-password',
            name: 'ForgotPassword',
            component: RecovaryEmailView
        },
        {
            path: '/reset-password/',
            name: 'ResetPassword',
            component: ResetPasswordView,
            props: true
        },
        {
            path: '/reset-link-sent',
            name: 'ResetLinkSent',
            component: RecovaryEmailSentView
        },
        {
            path: '/reset-complete',
            name: 'PasswordResetComplete',
            component: PasswordResetCompleteView
        },
        {
            path: '/change-password',
            name: 'ChangePassword',
            component: ChangePasswordView
        }

    ]
})

router.beforeEach(async (to) => {
    // redirect to login page if not logged in and trying to access a restricted page
    const publicPages = ['/', '/login', '/register', '/recover-password', '/reset-link-sent', '/reset-complete'];
    const isPublicPage = publicPages.includes(to.path) || to.path.startsWith('/reset-password/');
    const authRequired = !isPublicPage
    const userStore = useUserStore();

    if (authRequired && !userStore.user.isAuthenticated) {
        userStore.returnUrl = to.fullPath;
        return '/login';
    }

});

export default router
