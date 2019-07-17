<template>
    <div class="getDanmu">
      <div id="danmu" ref="danmu" @scroll="danmu_scroll_func">
        <div v-for="(it, i) in form" :key="i" style="width: 100%;height: 30px">
          <span style="float: left">{{it.user_level}}</span>
          <img :src="it.royal_level" alt="" v-if="it.royal_level" style="margin-left: 10px;float: left">
          <span :class="it.fans_back" v-if="it.fans_level" style="margin-left: 10px;float: left">{{it.fans_level}}</span>
          <span style="margin-left: 10px;float: left">{{it.user_name}}</span>
          <span :class="it.danmu_color" style="float: left">{{it.user_danmu}}</span>
          <span style="margin-left: 30px;float: left">{{it.danmu_time}}</span>
        </div>
      </div>
      <div id="segment">
        <div v-if="hotword.length!=0">
          <div>热词:
            <el-tag v-for="(it, i) of hotword" :key="i" style="margin-left: 20px">{{it}}</el-tag>
          </div>
          <div>
            <el-tag>不符合语义相似度:{{hotword_dosnt_match}}</el-tag>
          </div>
        </div>
        <div v-if="jieba_hotword.length!=0">
          <div>jieba热词:
            <el-tag v-for="(it, i) of jieba_hotword" :key="i" style="margin-left: 20px">{{it}}</el-tag>
          </div>
          <div>
            <el-tag>不符合语义相似度:{{jieba_hotword_dosnt_match}}</el-tag>
          </div>
        </div>
        <div v-if="user_name_arr.length!=0">
          <div>高频重复发言:
            <span v-for="(it, i) of user_name_arr" :key="i" style="margin-left: 20px">{{it}}</span>
          </div>
          <!--<span>bufuhe:{{jieba_hotword_dosnt_match}}</span>-->
        </div>
        <div v-if="suggestarray.length!=0">
          建议禁言:
          <div v-for="(it, i) of suggestarray" :key="i" style="margin-left: 20px">
            <span style="float: left">{{it.user_level}}</span>
          <img :src="it.royal_level" alt="" v-if="it.royal_level" style="margin-left: 10px;float: left">
          <span :class="it.fans_back" v-if="it.fans_level" style="margin-left: 10px;float: left">{{it.fans_level}}</span>
          <span style="margin-left: 10px;float: left">{{it.user_name}}</span>
          <span :class="it.danmu_color" style="float: left">{{it.user_danmu}}</span>
          <span style="margin-left: 30px;float: left">{{it.danmu_time}}</span>
          </div>
        </div>

      </div>
      <el-row>
        <el-button type='primary' @click="initWebSocket">连接弹幕</el-button>
        <el-button type='info' @click="websocketclose">关闭弹幕</el-button>
      </el-row>
    </div>
</template>

<script>
      import jquery from 'jquery'

    export default {
        name: "danmu",
      created(){
           //页面刚进入时开启长连接
           //  this.initWebSocket()
       },
　　　　destroyed: function() {
　　　　//页面销毁时关闭长连接
// 　　　　　　this.websocketclose();
　　　　},
      data(){
          return{
            websock:null,
            form:[],
            scrollflag:true,
            danmus:'',
            danmu_jieba:'',
            danmu_jieba_num:0,
            hotword:[],
            hotword_dosnt_match:'',
            jieba_hotword:[],
            jieba_hotword_dosnt_match:'',
            user_name_arr:[],
            user_dict:[],
            user_id_dict:{},
            user_num:{},
            user_name_id:{},
            timeout:0,
            suggestban:false,
            suggestarray:[],
            ii:0,
            times:(new Date()).getTime()
          }
      },
      methods: {


          getUserInf(){

          },

　　　　　　initWebSocket(){ //初始化weosocket
　　　　　　　
　　　　　　　　const wsuri =  'ws://127.0.0.1:8000/danmu/';//ws地址
　　　　　　　　this.websock = new WebSocket(wsuri);
　　　　　　　　this.websock.onopen = this.websocketonopen;

　　　　　　　　this.websock.onerror = this.websocketonerror;

　　　　　　　　this.websock.onmessage = this.websocketonmessage;
　　　　　　　　this.websock.onclose = this.websocketclose;

　　　　   },
          danmu_scroll_func(){
          // console.log(this.$refs.danmu.scrollHeight - this.$refs.danmu.scrollTop);
        // if (this.$refs.danmu.scrollTop != this.$refs.danmu.scrollHeight - 630 ){
            if(this.$refs.danmu.scrollHeight - this.$refs.danmu.scrollTop > 674){
                this.scrollflag = false
            }
            else{
            // if (this.$refs.danmu.scrollTop == this.$refs.danmu.scrollHeight - 630){
                this.scrollflag = true
            //
            }
          },
　　　　　　websocketonopen() {
　　　　　　　　console.log("WebSocket连接成功");
            this.websocketsend(JSON.stringify({
                              'message': 'Start'
                            }))
　　　　　　},
　　　　　　websocketonerror(e) { //错误
 　　　　　　 console.log("WebSocket连接发生错误");
　　　　　　},
　　　　　　websocketonmessage(e){ //数据接收
　　　　　　　　const redatas = JSON.parse(e.data);

              let redata = redatas['message'];
              // if(redata[])
                let kk = {};
                if(this.form.findIndex(it => it.id == redata['_id']) != -1) return -1;
                kk.id = redata['_id'];

                kk.user_level = '等级：' + redata['等级'];
                switch (redata['贵族']) {
                  case '无':
                    kk.royal_level = false;
                    break;
                  case '游侠':
                    kk.royal_level = "/static/img/游侠.png";
                    break;
                  case '骑士':
                    kk.royal_level = "/static/img/骑士.png";
                    break;
                  case '子爵':
                    kk.royal_level = "/static/img/子爵.png";
                    break;
                  case '伯爵':
                    kk.royal_level = "/static/img/伯爵.png";
                    break;
                  case '公爵':
                    kk.royal_level = "/static/img/公爵.png";
                    break;
                  case '国王':
                    kk.royal_level = "/static/img/国王.png";
                    break;
                  case '皇帝':
                    kk.royal_level = "/static/img/皇帝.png";
                    break;
                }
                if (redata['粉丝牌名字'] == '无') {
                  kk.fans_level =false
                }
                else {
                  kk.fans_level = redata['粉丝牌名字'] + ' ' + redata['粉丝牌等级'];
                  if (parseInt(redata['粉丝牌等级']) >= 1 && parseInt(redata['粉丝牌等级']) < 6) {
                    kk.fans_back = 'c1'
                  }
                  if (parseInt(redata['粉丝牌等级']) >= 6 && parseInt(redata['粉丝牌等级']) < 11) {
                    kk.fans_back = 'c2'
                  }
                  if (parseInt(redata['粉丝牌等级']) >= 11 && parseInt(redata['粉丝牌等级']) < 16) {
                    kk.fans_back = 'c3'
                  }
                  if (parseInt(redata['粉丝牌等级']) >= 16 && parseInt(redata['粉丝牌等级']) < 21) {
                    kk.fans_back = 'c4'
                  }
                  if (parseInt(redata['粉丝牌等级']) >= 21 && parseInt(redata['粉丝牌等级']) < 26) {
                    kk.fans_back = 'c5'
                  }
                  if (parseInt(redata['粉丝牌等级']) >= 26 && parseInt(redata['粉丝牌等级']) < 30) {
                    kk.fans_back = 'c6'
                  }
                  if (parseInt(redata['粉丝牌等级']) >= 30) {
                    kk.fans_back = 'c7'
                  }
                }
                if (redata['弹幕颜色'] == '无'){
                  kk.danmu_color = false;
                }
                else {
                  if (redata['弹幕颜色'] == '蓝色') {
                      kk.danmu_color = 'd1';
                  }
                  if (redata['弹幕颜色'] == '绿色') {
                      kk.danmu_color = 'd2';
                  }
                  if (redata['弹幕颜色'] == '粉色') {
                      kk.danmu_color = 'd3';
                  }
                  if (redata['弹幕颜色'] == '橙色') {
                      kk.danmu_color = 'd4';
                  }
                  if (redata['弹幕颜色'] == '紫色') {
                      kk.danmu_color = 'd5';
                  }
                  if (redata['弹幕颜色'] == '红色') {
                      kk.danmu_color = 'd6';
                  }
                }
                kk.user_name = redata['昵称'];
                kk.user_danmu = ':  ' + redata['弹幕内容'];
                // user_name.style.color = '#3A8CFD';
                kk.danmu_time = redata['发送弹幕时间'];
                if(this.form.length > 150){
                  this.form.splice(0,1)
                }
              this.form.push(kk);

              $.ajax({
                    url: 'http://127.0.0.1:8000/danmu/suggestban',
                  type: 'POST',
                  data: {
                    'danmu_jieba': kk.user_danmu
                  },
                    success: e => {
                      if(e === 'no'){
                        this.suggestarray.push(kk)
                      }
                  }
                  });
              if (this.scrollflag){
                  this.$refs.danmu.scrollTop = this.$refs.danmu.scrollHeight ;
              }

              [this.danmus, this.danmu_jieba, this.danmu_jieba_num] =
                [this.danmus+redata['弹幕内容']+' ', this.danmu_jieba+redata['弹幕内容']+'\r\n', this.danmu_jieba_num++]
              if (this.danmus.length > 300 && (this.danmu_jieba.length - this.danmu_jieba_num * 2) > 300) {
                // ooo = JSON.parse(ooo)
                $.ajax({
                  url: 'http://127.0.0.1:8000/danmu/analyse',
                  type: 'POST',
                  data: {
                    'danmus': this.danmus
                  },
                  success: e => {
                    this.hotword = e.split('!@##$$$%%%^^^&&&***(((*&)^')[0].split();
                    this.hotword_dosnt_match = e.split('!@##$$$%%%^^^&&&***(((*&)^')[1]
                  }
                });
                  $.ajax({
                    url: 'http://127.0.0.1:8000/danmu/jiebaanalyse',
                  type: 'POST',
                  data: {
                    'danmu_jieba': this.danmu_jieba
                  },
                    success: e => {
                      this.jieba_hotword = e.split('!@##$$$%%%^^^&&&***(((*&)^')[0].split();
                      this.jieba_hotword_dosnt_match = e.split('!@##$$$%%%^^^&&&***(((*&)^')[1]
                  }
                  });
                  this.danmus = '';
                  this.danmu_jieba = '';
                  this.danmu_jieba_num = 0;
                };
                let current_time = (new Date()).getTime();
        //         console.log(current_time)
        // console.log('121'+this.times)
                if (current_time < this.times + 5000){
                  if(this.user_num.hasOwnProperty(redata['用户ID'])){
                      this.user_num[redata['用户ID']] += 1;
                  }
                  else {
                    this.user_num[redata['用户ID']] = 1;
                    this.user_name_id[redata['用户ID']] = redata['昵称'];
                  }
                }
                else {
                  for (let hhh in this.user_num){
                    if (this.user_num[hhh] >= 3){
                      this.user_name_arr.push(this.user_name_id[hhh]);
                    }
                  }
                  this.user_num = {};
                  this.user_name_id ={};
                  this.times = current_time;
                  this.user_name_arr = Array.from(new Set(this.user_name_arr));
                  console.log(this.user_name_arr)
                }
                // if(this.ii = 0) {
                //   this.timeout = times
                //   this.ii++
                //   this.arr.push(redata['用户ID'])
                // }else if(this.timeout + 5000 >= times) {
                //   this.arr.push(redata['用户ID'])
                // }else{
                //   this.
                // }
　　　　　　　},

　　　　　　　websocketsend(agentData){//数据发送
　　　　　　　　    this.websock.send(agentData);
　　　　　　},

　　　　　 websocketclose(e){ //关闭
　　　　　　　　console.log("connection closed (" + e.code + ")");
              this.websocketsend(JSON.stringify({
                  'message': 'End'
                }))
　　　　　},
　　　},
    }

</script>

<style scoped>
  .c1{
    background: #4C98FA;
  }
  .c2{
    background: #44B0A7;
  }
  .c3{
    background: #F5A80C;
  }
  .c4{
    background: #FD6F13;
  }
  .c5{
    background: #E92150;
  }
  .c3{
    background: #8135DF;
  }
  .c4{
    background: #7B2AF0;
  }
  .d1{
    color: #1B6FEB;
  }
  .d2{
    color: #6DC33F;
  }
  .d3{
    color: #FB4CA4;
  }
  .d4{
    color: #FC6906;
  }
  .d5{
    color: #880EF1;
  }
  .d6{
    color: #FC0005;
  }
  ul li{
      list-style: none;
  }
  #danmu{
      width: 70%;
      height: 630px;
      overflow: scroll;
  }
  #segment{
      position: absolute;
      width: 28%;
      height: 630px;
      left: 71%;
      top: 5%;
  }
.getDanmu{
  position: absolute;
  width: 100%;
  height: 630px;
  margin-top: 5%;
  color: black;
}
</style>
