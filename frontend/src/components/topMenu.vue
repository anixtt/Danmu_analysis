<template>
  <el-menu
      :default-active="onRoutes"
   class="el-menu-demo"
  mode="horizontal"
  background-color="#545c64"
  text-color="#fff"
  active-text-color="#ffd04b" style="width: 100%;height: 100%;float: left">
    <el-row style="width: 18%;height: 100%;float: left;margin-left: 8%">
    <el-col :span="4" style="margin: 20px auto;display: inline-block">
      <a href="http://www.douyu.com/9999" title="打开直播间" target="_blank">
        <div :class="[live_flag == '直播中'?'live_on':'live_off']"
          id="wheather_live" style="height: 15px;width: 40px;font-size: 10px">
          {{live_flag}}
        </div>
      </a>
    </el-col>
    <el-col :span="6" style="margin: 10px auto;">
      <a href="https://yuba.douyu.com/api/dy/anchor/anchorTopic?room_id=9999"
         title="鱼吧" target="_blank">
        <span style="width: 40px;height: 40px;border-radius: 40px;">
        <el-image :src="roomimgUrl"
                        style="width: 40px;height: 40px;border-radius: 40px;"></el-image>
        </span>
      </a>
    </el-col>
      <el-col v-if="live_flag == '直播中'" :span="12" style="margin: 20px auto;font-size: 14px">
        {{roomName}}
      </el-col>
      <el-col v-if="live_flag == '直播中'" :span="8" style="position: absolute;margin-left: 220px;margin-bottom: 80px">
        <el-tag size="small" style="background-color: forestgreen;color: black">{{hot}}</el-tag>
      </el-col>
    </el-row>
    <router-link v-bind:to="'/'" tag="div" style="float: left;margin-left: 35%">
      <a><el-menu-item index="'/'">数据分析</el-menu-item></a>
    </router-link>
    <router-link v-bind:to="'/danmu'" tag="div" style="float: left;">
      <a><el-menu-item index="'/danmu'">弹幕显示  </el-menu-item></a>
    </router-link>
    <router-view></router-view>
    <el-submenu style="float: right;margin-right: 2%" v-if="loginFlag_no">
      <template slot="title">
        <i class="el-icon-user"></i><span>未登录</span>
      </template>
      <el-menu-item @click="loginInf = true">
        <i class="el-icon-arrow-right"></i><span>我要登录</span>
      </el-menu-item>
    </el-submenu>
    <el-submenu style="float: right;margin-right: 2%" v-if="loginFlag_yes">
      <template slot="title">
        <el-image :src="userImageUrl" style="margin-top: 6px;"></el-image>
        <span>{{userName}}</span>
      </template>
      <el-menu-item @click="showUserInf" style="width: 100%">
        <i class="el-icon-user-solid"></i><span>个人信息</span>
      </el-menu-item>
      <el-menu-item @click="logOut = true" style="width: 100%">
        <i class="el-icon-switch-button"></i><span>注销登录</span>
      </el-menu-item>
    </el-submenu>


    <!--登录Dialog-->
    <el-dialog
        :visible.sync="loginInf"
        :modal=false
        width="30%" :center=false style="float: left;margin-right: 20px">
          <!--:before-close="handleClose">-->
          <div slot="title" style="color: #696969;float: left;font-size: 18px">
            <strong>用户登录</strong>
          </div>
          <div style="border-top: 1px solid grey;border-bottom: 1px solid grey;padding-bottom: 120px;padding-top: 30px;font-size: 15px">
            <span style="float: left;margin-bottom: 3px">本网站主要是对弹幕进行分析，找出其中带节奏的(水军)及机器人，并对部分数据可视化</span>
            <i class="el-icon-info" style="float: left;margin-left: 5%;padding-top: 20px"></i>
            <span style="float: left;padding-top: 20px;padding-left: 2px;margin-left: 3px"><strong>本网站采用直播间弹幕登录,不涉及密码。</strong></span>
            <br><br>
            <span style="float: left;margin-left: 8%;padding-top: 20px"><strong>继续登录请按确定登录按钮</strong></span>
          </div>
          <el-dialog
          :visible.sync="loginCode"
          :modal=false
          width="30%" :center=false append-to-body>
          <div slot="title" style="color: #696969;float: left;font-size: 18px">
            <strong>用户登录</strong>
          </div>
          <div style="border-top: 1px solid grey;border-bottom: 1px solid grey;padding-bottom: 60px;padding-top: 40px;font-size: 15px">
            <span>登录请求已发送，单击复制下列代码并发送至直播间</span><br><br>
            <el-button type="info" plain @click="copy" class="getCode" data-clipboard-target=".getCode" :data-clipboard-text="checkcode" style="width: 300px;height: 80px">{{checkcode}}</el-button>
            <br><br><br><br>
            <span style="font-size: 32px"><strong>暂不支持IE浏览器</strong></span>
          </div>
          <span slot="footer" class="dialog-footer">
            <el-button @click="loginCode = false" style="margin-right: 22%">取消</el-button>
            <el-button type="primary" @click="loginCode = false" :loading="true" style="margin-right: 14%">登录中</el-button>
          </span>
        </el-dialog>
          <span slot="footer" class="dialog-footer">
            <el-button @click="loginInf = false" style="margin-right: 22%">取消</el-button>
            <el-button type="primary" @click="createCode" style="margin-right: 14%">确定登录</el-button>
          </span>
        </el-dialog>

    <!--个人信息Dialog-->
    <el-dialog
      :visible.sync="userInf"
      width="40%">
      <div slot="title" style="color: #696969;float: left;font-size: 18px;width: 20%">
        <i class="el-icon-info" style="color: dodgerblue"></i>
        <strong style="margin-left: 2%">个人信息</strong>
      </div>
      <div style="margin-top: 1%;float: left;margin-left: 2%;">
        <el-image :src="userImageUrl" style="width: 100px;height: 100px;float: left;"></el-image>
        <div style="width: 80%;height: 18px;float: left">用户名：{{userName}}</div>
        <div v-if="ufl" style="width: 80%;height: 30px;float: left;">粉丝牌： <el-tag>{{userFansLevel}}</el-tag>
          <span>等级： {{userLevel}}</span>
        </div>
        <div style="width: 80%;height: 18px;float: left;">
        <span>共发弹幕数量： {{userDanMuNum}}</span>
        <span>常说词： </span><span v-for="(it, i) of userDanMuNumHotWord" :key="i" style="margin-left: 2%">{{it}}</span>
          </div>
        <div style="width: 100%;height: 18px;float: left;">活跃时间段： <span v-for="(inf, f) of userAcitveTime" :key="f" style="margin-left: 2%">{{inf}}</span>
        </div>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="userInf = false" style="margin-right: 20%">关闭</el-button>
      </span>
    </el-dialog>


    <!--注销登录Dialog-->
    <el-dialog
      :visible.sync="logOut"
      width="30%">
      <div slot="title" style="color: #696969;float: left;font-size: 18px">
        <i class="el-icon-question" style="color: #F66A1B"></i>
        <strong>注销登录</strong>
      </div>
      <div style="border-top: 1px solid grey;border-bottom: 1px solid grey;padding-bottom: 60px;padding-top: 40px;font-size: 16px">
        <strong><b>确定要注销登录吗</b></strong>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="logOut = false" style="margin-right: 6%">再想想，再想想</el-button>
        <el-button type="primary" @click="userLogOut" style="margin-right: 4%">不用想了，直接注销</el-button>
      </span>
    </el-dialog>



  </el-menu>

            <!--</el-breadcrumb>-->
        <!--<router-link v-bind:to="'/'" tag="div"><a>数据分析</a></router-link>-->
        <!--<router-link v-bind:to="'/danmu'" tag="div"><a>弹幕显示</a></router-link>-->
</template>

<script>
  import Vue from 'vue'
  import axios from 'axios'
  import jquery from 'jquery'
  import Clipboard from 'clipboard'
    export default {
        name: "topMenu",
      data:function(){
    return{
       live_flag:'',
      roomimgUrl:'',
      roomName:'',
      hot: '',
      checkcode:'',
      ufl:false,
      userFansLevel:'',
      userLevel:'',
      userRoyalUrl:'',
      userDanMuNum:'',
      userBlackNum:'',
      userAcitveTime:'',
      userDanMuNumHotWord:[],
      loginCode:false,
      loginInf:false,
      copyBtn: null,
      websock:null,
      userImageUrl: '',
      loginFlag_no: true,
      loginFlag_yes: false,
      logOut:false,
      userInf:false,
      userName: '',
      websocketflag: false
      // username: '',
        // activeIndex2: '1'
    }

  },
      methods: {
        showUserInf(){
          this.userInf = true;
          $.ajax({
                url: 'http://127.0.0.1:8000/room/getDetailedInf/',
                type: 'POST',
                data: {
                  'searchdate': localStorage.getItem("userid")
              },success: result => {
                  let udi = JSON.parse(result);
                  this.userDanMuNum = udi['弹幕数'];
                  this.userDanMuNumHotWord = udi['常说词'];
                  this.userAcitveTime = udi['发弹幕时间'];
                }
              });
        },
        copy() {
          /*这是点击按钮触发的点击事件，关于clipboard的使用就不再赘述了，上面介绍时已经讲述过，并且使用方法在官方文档上有*/
          var clipboard = new Clipboard('.getCode');
          clipboard.on('success', e => {
            this.$message({
              /*这是使用了element-UI的信息弹框*/
              message: '复制成功！',
              type: 'success'
            });
          });
          clipboard.on('error', e => {
            this.$message({
              message: '复制失败，请手动选择复制！',
              type: 'error'
            });
          });
        },
        userLogOut(){
          this.logOut = false;
          localStorage.removeItem('Flag');
          localStorage.removeItem('username');
          localStorage.removeItem('userImage');
          localStorage.removeItem('userid');
          localStorage.removeItem('userauthority');
          this.loginFlag_no = true;
          this.loginFlag_yes = false;
          this.$router.push('/')
        },
        createCode() {
          this.loginInf = false;
          this.loginCode = true;
          const wsuri = 'ws://127.0.0.1:8000/danmu/';//ws地址
          this.$message({
            message: '请在一分钟内复制登录',
            type: 'warning'
          });
          var code = "";
          var codeLength = 8;
          var randomNum = new Array(0, 1, 2, 3, 4, 5, 6, 7, 8, 9);
          var randomAlp = new Array('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
            's', 't', 'u', 'v', 'w', 'x', 'y', 'z');//随机数
          for (var i = 0; i < codeLength; i++) {
            var wheatherAlpNum = Math.floor(Math.random() * 2);
            if (wheatherAlpNum == 0) {
              var elemNumIndex = Math.floor(Math.random() * 10);
              code += randomNum[elemNumIndex];
            }
            else {
              var elemAlpIndex = Math.floor(Math.random() * 26);
              code += randomAlp[elemAlpIndex];
            }
          }
          this.checkcode = '#登录:' + code;//把code值赋给验证码
　　　　　　this.websock = new WebSocket(wsuri);
　　　　　　this.websock.onopen = this.websocketonopen;
          this.websock.onerror = this.websocketonerror;
          this.websock.onmessage = this.websocketonmessage;
　　　　　　this.websock.onclose = this.websocketclose;
        },

        websocketonopen() {
　　　　　　　　console.log("WebSocket连接成功");
            this.websocketsend(JSON.stringify({
                              'message': 'Start'
                            }));
            this.websocketflag = true;
               setTimeout(e => {
                if ((localStorage.getItem("Flag") !== 'isLogin') && this.websocketflag) {
                  this.websocketclose();
                  this.$message({
                    message: '已超时，请重新登录',
                    type: 'error'
                  });
                  this.loginCode = false;
                }
              }, 60000);
　　　　　　　},
　　　　　　websocketonerror(e) { //错误
 　　　　　　 console.log("WebSocket连接发生错误");
　　　　　　},
　　　　　　websocketonmessage(e) { //数据接收
          const redatas = JSON.parse(e.data);
            let redata = redatas['message'];
            let idurl = redata['用户ID'];
            if (redata['弹幕内容'] == this.checkcode) {
              this.websocketclose();
              // this.$store.dispatch("userLogin", true);
              localStorage.setItem("Flag", "isLogin");
              localStorage.setItem("username", redata['昵称']);
              localStorage.setItem("userid", redata['用户ID']);
              if (redata["粉丝牌名字"] !== '无') {
                this.ufl = true;
                localStorage.setItem("userfanslevel", redata['粉丝牌名字'] + " " + redata['粉丝牌等级']);
              }
              localStorage.setItem("userlevel", redata['等级']);
              if (redata['用户ID'] == '19470003'){
                localStorage.setItem("userauthority", "房管");
              }
              else {
                localStorage.setItem("userauthority", redata['权限']);
              }
              if (redata['用户ID'].length <= 9){
                for(var i = 0;i < 9 - redata['用户ID'].length;i++){
                  idurl = '0' + idurl;
                }
              }
              localStorage.setItem("userImage", "https://apic.douyucdn.cn/upload/avatar/"+idurl.slice(0, 3)+"/"+
                idurl.slice(3, 5)+"/"+ idurl.slice(5, 7)+"/"+idurl.slice(7, 9)+"_avatar_small.jpg");
              this.userImageUrl = localStorage.getItem('userImage');
              this.userName = localStorage.getItem('username');
              this.userFansLevel = localStorage.getItem('userfanslevel');
              this.userLevel = localStorage.getItem('userlevel');
              this.loginCode = false;
              this.loginFlag_no = false;
              this.loginFlag_yes = true;
              this.websocketflag = false;
              this.$message({
                message: '登录成功',
                type: 'success'
              });
              this.$router.push({
                path: '/'
              });
            }
      },


        websocketsend(agentData){//数据发送
　　　　　　　　    this.websock.send(agentData);
　　　　　　},
        websocketclose(e){ //关闭
              this.websocketsend(JSON.stringify({
                  'message': 'End'
                }))
　　　　　},
      },
  created:function() {
    setInterval(e => {
      axios.post('http://127.0.0.1:8000/room/', {})
        .then(result => {
          var roominf = result['data'];
          // console.log(roominf['room_status']
          // console.log(this)
          this.live_flag = roominf['room_status'];
          this.roomimgUrl = roominf['owner_image'];
          this.roomName = roominf['room_name'];
          this.hot = roominf['hot'];
        });
      }, 5000);
      if (localStorage.getItem('Flag') === 'isLogin') {
        this.loginFlag_no = false;
        this.loginFlag_yes = true;
        this.userImageUrl = localStorage.getItem('userImage');
        this.userName = localStorage.getItem('username');
        if (localStorage.getItem('userfanslevel').length > 3) {
          this.ufl = true;
          this.userFansLevel = localStorage.getItem('userfanslevel');
        }
        this.userLevel = localStorage.getItem('userlevel');
      }
  },
      // mounted(){
      //     this.copyBtn = new Clipboard(this.$refs.copy);
      // },
      computed: {
        onRoutes () {
      // 当前激活菜单的 index
      let index = this.$route.path.replace('/', '');
      // let title = this.$route.meta.title;
      // 改变浏览器title
      // document.title = title;
      return index
        }
      }
    }
</script>

<style scoped>
</style>
