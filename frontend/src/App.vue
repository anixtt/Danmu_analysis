<template>
  <el-container id="app">
    <el-header id="bar">
  <!--<el-menu-item>-->
      <topMenu></topMenu>
    </el-header>
    <el-main>
      <danmu v-if="showflag"></danmu>
    </el-main>
  </el-container>

</template>

<script>
  import Vue from 'vue'
import axios from 'axios'
  import Showdata from "./components/showdata";
  import topMenu from './components/topMenu'
  import danmu from "./components/danmu"
  // Vue.config.delimiters = ["{[", "]}"];
export default {
  name: 'app',
  components: {danmu, topMenu},
  delimiters:['[[', ']]'],
  data:function(){
    return{
       live_flag:'',
      roomimgUrl:'',
      showflag: false
        // activeIndex2: '1'
    }

  },
  // methods: {
  //   function() {
  //     if (this.$route.path == 'http://127.0.0.1:8080/danmu') {
  //       this.showflag = true;
  //       console.log(123123)
  //     }
  //   }
  // },
  created:function() {
    axios.post('http://127.0.0.1:8000/room/', {})
      .then(result => {
        var roominf = result['data'];
        // console.log(roominf['room_status']
        // console.log(this)
        this.live_flag = roominf['room_status']
        this.roomimgUrl = roominf['owner_image']
        console.log(this.roomimgUrl)


      });
  }
  // },
  // methods: {
  //   handleSelect(key, keyPath) {
  //       console.log(key, keyPath);
  //     }
  //   }
}

</script>
<!-- css格式 -->
<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 10px;
}
#bar{
  width: 100%;
  height: 50px;
  /*float: left;*/
  background-color: #545c64;
  color: #fff;
  /*display: table;*/
}
  .live{
    width: 15%;
    height: 50px;
    display: inline-block;
  }
  .route{
    width: 80%;
    height: 50px;
    display: inline-block;
  }
  ul{
    height: 40px;
  }
  li{
    list-style: none;
    float: right;
    margin-right: 2%;
  }
  a{
    text-decoration: none;
  }
  .live_on{
    background-color: mediumaquamarine;
  }
  .live_on:hover{
    background-color: springgreen;
  }
  .live_off{
    background-color: #F0FFF0;
  }
  .live_off{
    background-color: gainsboro;
  }
  #wheather_live{
    border: 0.5px solid white;
  }
</style>
