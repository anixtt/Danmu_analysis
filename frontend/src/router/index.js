import Vue from 'vue'
import Router from 'vue-router'
import showdata from '@/components/showdata'
import danmu from '@/components/danmu'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'showdata',
      component: showdata
    },
    {
      path: '/danmu',
      name: 'danmu',
      component: danmu
    }
  ]
})
