import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SearchBar from '../components/SearchBar.vue'
import MultiFilter from '../components/MultiFilter.vue'


Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component : HomeView,
  },
  {
    path: '/search',
    name: 'search',
    component : SearchBar
  },
  {
    path: '/filter',
    name: 'filter',
    component : MultiFilter
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
