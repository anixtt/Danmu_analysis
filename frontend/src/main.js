// 导入vue实例
import Vue from 'vue'
//导入 App 组件
import App from './App'
import axios from 'axios'
//导入 vue router
import VueRouter from 'vue-router'
import ElementUI from 'element-ui'
import echarts from 'echarts'
Vue.use(echarts);
Vue.prototype.$echarts = echarts;
import {Message} from 'element-ui'
import store from './store/store'
import 'element-ui/lib/theme-chalk/index.css'
import Vuex from 'vuex'
Vue.use(Vuex);
//告诉vue使用vue-router路由组件
Vue.use(VueRouter);
Vue.use(ElementUI);

// Vue.use(Message);
// Vue.prototype.$message = Message;
//导入Hello组件
import showdata from './components/showdata'
import jjj from './components/jjj'
//导入Aboiut组件
import danmu from './components/danmu'
// Vue.config.delimiters = ["{[", "]}"];
//定义路由表
const routes = [
//对应Hello组件的路由地址
{
  path: '/',
  component: showdata,
  meta: {
    isLogin: false,
    authority: false,
  }
},

  {
    path: '/danmu',
    component: danmu,
    meta: {
      isLogin: true,
      authority: true,
    }
  }
  // { path: '/jjj', component: jjj }
];

// 创建路由器实例，并且传入`routes`变量作为路由。
// 你还可以传入别的参数，不过在这里尽量简单化就可以了
const router = new VueRouter({
  routes,
  mode: 'history'
});
router.beforeEach((to, from, next) => {

  //获取用户登录成功后储存的登录标志
  let getFlag = localStorage.getItem("Flag");
  let getAuthority = localStorage.getItem("userauthority");

  if (getAuthority === "房管" || getAuthority === "房主"){
    this.authority = true;
    next();
  }
  else {
    if(to.meta.authority) {
      Vue.prototype.$message({
        message: '没有查看权限',
        type: 'warning'
      });
      next({
        path: '/'
      });
    }
    else {
      next();
    }
  }

  //如果登录标志存在且为isLogin，即用户已登录
  if(getFlag === "isLogin"){

    //设置vuex登录状态为已登录
    this.isLogin = true;
    next();

    // //如果已登录，还想想进入登录注册界面，则定向回首页
    // if (!to.meta.isLogin) {
    //    //iViewUi友好提示
    //   iView.Message.error('请先退出登录')
    //   next({
    //     path: '/home'
    //   })
    // }

  //如果登录标志不存在，即未登录
  }else{

    //用户想进入需要登录的页面，则定向回登录界面
    if(to.meta.isLogin){
      //iViewUi友好提示
      Vue.prototype.$message({
        message: '请先登录',
        type: 'warning'
      })
    //用户进入无需登录的界面，则跳转继续
    }else{
      next()
    }

  }

});
//实例化Vue实例
new Vue({
  //定义Vue绑定的跟元素
  el: '#app',
  delimiters:['[[', ']]'],
  //用<App/>代替根元素
  template: '<App/>',
  //声明App组件，这样上面的<App/>元素就可以生效
  components: { App },
  //将上面声明的路由器传递到根Vue实例
  router
}).$mount('#app')//将这个实例挂载到id=app的根元素上
