<template>
  <div class="danmu_data_analyse">
    <div class="danmu_roll">
      <el-tag style="font-size: 18px;margin-right: 21%">{{danmu_date}}</el-tag>
       <el-date-picker
         v-model="value1"
      type="date"
      placeholder="选择日期"
       value-format="yyyy-MM-dd"
         :clearable=false
      :picker-options="pickerOptions" style="float: left;margin-top: 5%;margin-left: 5%">
    </el-date-picker>
      <div style="width: 640px;margin-left: 27%;margin-top: 2%" class="num_roll">
        <DigitRoll
          ref='digitroll'
          :rollDigits='digits'
          :flipStra = "flipStra3"
          easeFn=""
        />
      </div>
    </div>
    <div id="danmunum_chart" style="width: 1400px;height: 480px;float: left" ref="danmunum_chart"></div>
    <div v-if="wordclflag">
      <el-image :src="wcloud" style="float: left;width: 400px;height: 400px;margin-left: 2%"></el-image>
      <el-tag v-for="(it, i) of danmuhotword" :key="i" style="width: 120px;float: left;margin-left: 40px;margin-top: 50px;" :class="it.tagbgcolor">
        {{it.word}}
      </el-tag>
      <div id="user_chart" style="width: 1400px;height: 480px;float: left" ref="user_chart"></div>
    </div>
  </div>
</template>

<script>
import DigitRoll from '@huoyu/vue-digitroll';
import echarts from 'echarts'
import axios from 'axios';
import jquery from 'jquery';
export default {
    name: "showdata",
    components: { DigitRoll },
    data:function(){
      return {
        pickerOptions: {
          disabledDate(time) {
            return time.getTime() > Date.now();
          }
        },
        value1: this.getNowFormatDate(),
        digits: '000000',
        digits_after: '',
        danmu_date: this.getNowFormatDate(),
        charts: null,
        usercharts: null,
        fans_danmu_num: [],
        normal_danmu_num: [],
        danmu_num_all: [],
        bgcolorclass: ['tb1', 'tb2', 'tb3', 'tb4', 'tb5', 'tb6', 'tb7', 'tb8', 'tb9', 'tb10',
        'tb11', 'tb12', 'tb13', 'tb14', 'tb15', 'tb16', 'tb17', 'tb18', 'tb19', 'tb20'],
        interval_danmu: null,
        interval_data: null,
        interval_time: null,
        danmuhotword: [],
        daytopusername: [],
        wordclflag: false,
        wcloud: '',
        user_name_data:[],
        user_num_data:[],
        user_hotword_data:[],
        // time: this.getDanmuTime(),
        time_hour: ['00:00', '00:30', '01:00', '01:30', '02:00', '02:30', '03:00', '03:30',
        '04:00', '04:30', '05:00', '05:30', '06:00', '06:30', '07:00', '07:30', '08:00', '08:30',
        '09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30',
        '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30',
        '19:00', '19:30', '20:00', '20:30', '21:00', '21:30', '22:00', '22:30', '23:00', '23:30']
      }
    },
  watch:{
    value1(){
      if (this.value1 == this.getNowFormatDate()){
        this.danmu_date = this.value1;
        this.interval_danmu = setInterval(e => {
        axios.post('http://127.0.0.1:8000/room/nowtimeroomdata/', {})
        .then(result => {
          let danmunumall = result['data'];
          this.digits_after = danmunumall['danmu_num'];
          for (var i=0;i<(6-this.digits_after.length)+1;i++){
            this.digits_after = '0'+this.digits_after
          }
          this.flipStra3(this.digits, this.digits_after);
          this.digits = this.digits_after;
          this.wordclflag = false;
        })
      }, 950);
      this.interval_data = setInterval(e => {
        // axios.post('http://127.0.0.1:8000/room/danmu_num_data/', {"time": this.time, "yesterdaynum": this.time_delete.length})
        this.getChartdata();
      }, 1800000);
      this.getChartdata();
      }
      else {
        this.danmuhotword = [];
        $.ajax(
          {
            url: 'http://127.0.0.1:8000/room/pasttimeroomdata/',
            type: 'POST',
            data: {
              'searchdate': JSON.stringify(this.value1)
            },
            success: result => {
              let pasttimedata = JSON.parse(result);
              this.wcloud = '/static/wc/'+this.value1+'词云.jpg';
              this.danmu_num_all = pasttimedata['dmnum'];
              this.normal_danmu_num = pasttimedata['ndmnum'];
              this.fans_danmu_num = pasttimedata['fdmnum'];
              this.digits_after = pasttimedata['allnum'];
              for (var i = 0; i < (6 - this.digits_after.length); i++) {
                this.digits_after = '0' + this.digits_after
              }
              console.log(this.digits_after);
              clearInterval(this.interval_danmu);
              clearInterval(this.interval_data);
              clearInterval(this.interval_time);
              this.interval_danmu = null;
              this.interval_data = null;
              this.interval_time = null;
              this.danmu_date = this.value1;
              this.flipStra3(this.digits, this.digits_after);
              this.digits = this.digits_after;
              if (parseInt(this.digits) == 0){
                this.wordclflag = false;
              }
              else {
                this.wordclflag = true;
              }
              this.charts.setOption({
                xAxis: {
                  data: this.time_hour
                },
                series: [{
                  // 根据名字对应到相应的系列
                  name: '弹幕数目',
                  data: this.danmu_num_all
                },
                  {
                    // 根据名字对应到相应的系列
                    name: '粉丝弹幕',
                    data: this.fans_danmu_num
                  },
                  {
                    // 根据名字对应到相应的系列
                    name: '普通弹幕',
                    data: this.normal_danmu_num
                  }]
              })
            }
        });
        $.ajax(
          {
            url: 'http://127.0.0.1:8000/room/userdata/',
            type: 'POST',
            data: {
              'searchdate': JSON.stringify(this.value1)
            },
            success: result => {
              let dd = JSON.parse(result);
              let gg = {};
              for (var i=0;i<dd['热词前二十'].length;i++){
                gg.word = dd['热词前二十'][i];
                gg.tagbgcolor = this.bgcolorclass[i];
                this.danmuhotword.push(gg);
                gg = {};
              }
              // let danmuusernumtop = dd['弹幕数前十'];
              // let kk = {};
              // for(var i=0;i<danmuusernumtop.length;i++){
              //   this.user_name_data.push(un);
              //   this.user_num_data.push(danmuusernumtop[i]['count']);
              //   kk.danmuusernumtop[i]['用户名'] = danmuusernumtop[i]['热词前十'];
              //   this.user_hotword_data.push(kk);
              // }
            }
        })
      }
    }
  },
    methods: {
      getChartdata(){
        axios.post('http://127.0.0.1:8000/room/danmu_num_data/', {})
        .then(result => {
          let danmudata = result['data'];
          // fans_danmu_num: [],
          //   normal_danmu_num: [],
          //   danmu_num_all: [],
          this.danmu_num_all = danmudata['dmnum'];
          this.normal_danmu_num = danmudata['ndmnum'];
          this.fans_danmu_num = danmudata['fdmnum'];
          this.charts.setOption({
            xAxis: {
            data: this.time_hour
        },
        series: [{
            // 根据名字对应到相应的系列
            name: '弹幕数目',
            data: this.danmu_num_all
        },
        {
            // 根据名字对应到相应的系列
            name: '粉丝弹幕',
            data: this.fans_danmu_num
        },
        {
            // 根据名字对应到相应的系列
            name: '普通弹幕',
            data: this.normal_danmu_num
        }]
          })
        })
      },
      flipStra3(before, next) {
        if (next > before) {
          return true;
        }
        return false;
      },
      getNowFormatDate() {
            var date = new Date();
          var seperator1 = "-";
          var seperator2 = ":";
          var month = date.getMonth() + 1;
          var strDate = date.getDate();
          if (month >= 1 && month <= 9) {
              month = "0" + month;
          }
          if (strDate >= 0 && strDate <= 9) {
              strDate = "0" + strDate;
          }
          var currentdate = date.getFullYear() + seperator1 + month + seperator1 + strDate;
          return currentdate;
      },
      drawChart() {
        this.charts = echarts.init(document.getElementById('danmunum_chart'));
        this.charts.setOption({
        tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'cross',
              crossStyle: {
                color: '#999'
              }
            }
          },
          toolbox: {
            feature: {
              dataView: {show: true, readOnly: false},
              magicType: {show: true, type: ['line', 'bar']},
              restore: {show: true},
              saveAsImage: {show: true}
            }
          },
          legend: {
            data: ['弹幕数量', '粉丝弹幕', '普通弹幕']
          },
    xAxis: [
            {
              type: 'category',
              data: [],
              axisPointer: {
                type: 'shadow'
              },
              axisLabel:{rotate:30,interval:0}
            }
          ],
    yAxis: {},
    series: [
      {
        name: '弹幕数目',
        type: 'line',
        data: this.danmu_num_all
      },
      {
        name: '粉丝弹幕',
        type: 'bar',
        data: this.fans_danmu_num
      },
      {
        name: '普通弹幕',
        type: 'bar',
        data: this.normal_danmu_num
      },
    ]
});
      },
      drawUserChart(){
        this.usercharts = echarts.init(document.getElementById('user_chart'));
        this.usercharts.setOption({
          title: {
        text: '发弹幕数前十'
          },
          tooltip: {},
          xAxis: {
              data: this.user_name_data
          },
          yAxis: {},
          series: [{
              name: '弹幕数',
              type: 'bar',
              data: this.user_num_data
          }]
        })
      }
    },
    created: function () {
      this.wcloud = '/static/wc/'+this.getNowFormatDate()+'词云.jpg';
      console.log(this.wcloud);
      this.interval_danmu = setInterval(e => {
        axios.post('http://127.0.0.1:8000/room/nowtimeroomdata/', {})
        .then(result => {
          let danmunumall = result['data'];
          this.digits_after = danmunumall['danmu_num'];
          for (var i=0;i<(6-this.digits_after.length)+1;i++){
            this.digits_after = '0'+this.digits_after
          }
          this.flipStra3(this.digits, this.digits_after);
          this.digits = this.digits_after;
        })
      }, 950);
      this.interval_data = setInterval(e => {
        // axios.post('http://127.0.0.1:8000/room/danmu_num_data/', {"time": this.time, "yesterdaynum": this.time_delete.length})
        axios.post('http://127.0.0.1:8000/room/danmu_num_data/', {})
        .then(result => {
          let danmudata = result['data'];
          // fans_danmu_num: [],
          //   normal_danmu_num: [],
          //   danmu_num_all: [],
          this.danmu_num_all = danmudata['dmnum'];
          this.normal_danmu_num = danmudata['ndmnum'];
          this.fans_danmu_num = danmudata['fdmnum']
          this.charts.setOption({
            xAxis: {
            data: this.time_hour
        },
        series: [{
            // 根据名字对应到相应的系列
            name: '弹幕数目',
            data: this.danmu_num_all
        },
        {
            // 根据名字对应到相应的系列
            name: '粉丝弹幕',
            data: this.fans_danmu_num
        },
        {
            // 根据名字对应到相应的系列
            name: '普通弹幕',
            data: this.normal_danmu_num
        }]
          })
        })
      }, 1800000);
      this.interval_time = setInterval(e => {
        if (this.getNowFormatDate() != this.danmu_date){
          this.danmu_date = this.getNowFormatDate();
          this.value1 = this.getNowFormatDate();
          this.getChartdata();
          axios.post('http://127.0.0.1:8000/room/makecloudword/', {})
        }
      }, 1000);
      this.getChartdata();
      $.ajax(
          {
            url: 'http://127.0.0.1:8000/room/userdata/',
            type: 'POST',
            data: {
              'searchdate': JSON.stringify(this.value1)
            },
            success: result => {
              let dd = JSON.parse(result);
              let danmuusernumtop = dd['弹幕数前十'];
              let kk = {};
              for(var i=0;i<danmuusernumtop.length;i++){
                this.user_name_data.push(un);
                this.user_num_data.push(danmuusernumtop[i]['count']);
                kk.danmuusernumtop[i]['用户名'] = danmuusernumtop[i]['热词前十'];
                this.user_hotword_data.push(kk);
              }
              this.usercharts.setOption({
                xAxis: {
                    data: this.user_name_data
                },
                yAxis: {},
                series: [{
                    name: '弹幕数',
                    type: 'bar',
                    data: this.user_num_data
                }]
              })
            }
        })
    },
  mounted:function () {
        this.drawChart();
        this.drawUserChart();
  },

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.danmu_data_analyse{
  position: absolute;
  width: 100%;
  margin-top: 5%;
  color: black;
}
.num_roll{
  background-color: #888888;
  height: 70px;
  line-height: 70px;
  border: 1px solid;
  font-size: 22px;
}
.tb1{
  background-color: #4B0082;
  color: white;
}
  .tb2{
  background-color: #9400D3;
    color: white;
}
  .tb3{
  background-color: #8A2BE2;
    color: white;
}.tb4{
  background-color: #9932CC;
  color: white;
}
  .tb5{
  background-color: #9370DB;
    color: black
}.tb6{
  background-color: #6A5ACD;
  color: black
}.tb7{
  background-color: #4169E1;
  color: black
}.tb8{
  background-color: #6495ED;
  color: black
}.tb9{
  background-color: #1E90FF;
  color: black
}.tb10{
  background-color: #87CEFA;
  color: black
}
  .tb11{
  background-color: #87CEEB;
    color: black
}
  .tb12{
  background-color: #40E0D0;
    color: black
}
.tb13{
  background-color: #00FA9A;
  color: black
}
.tb14{
  background-color: #7FFF00;
  color: black
}
  .tb15{
  background-color: #7CFC00;
    color: black
}
  .tb16{
  background-color: #ADFF2F;
    color: black
}
  .tb17{
  background-color: #FFFACD;
    color: black
}
  .tb18{
  background-color: #FAFAD2;
    color: black
}
  .tb19{
  background-color: #FFFFF0;
    color: black
}
  .tb20{
  background-color: #FFFFE0;
    color: black
}











</style>
