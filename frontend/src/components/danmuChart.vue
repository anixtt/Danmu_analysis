<template>
  <div id="danmunum_chart" style="width: 720px;height: 480px;" ref="danmunum_chart"></div>
</template>

<script>
    export default {
        name: "danmuChart",
        data(){
          return{
            charts: null,
            fans_danmu_num: [],
            normal_danmu_num: [],
            danmu_num_all: [],
            // time: this.getDanmuTime(),
            time_hour: ['00:00', '00:30', '01:00', '01:30', '02:00', '02:30', '03:00', '03:30',
            '04:00', '04:30', '05:00', '05:30', '06:00', '06:30', '07:00', '07:30', '08:00', '08:30',
            '09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30',
            '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30',
            '19:00', '19:30', '20:00', '20:30', '21:00', '21:30', '22:00', '22:30', '23:00', '23:30']
            // time_delete: [],
            // time_exist: [],
          }
        },
        methods:{
          drawChart(){
            this.charts = this.$echarts.init(this.$refs.danmunum_chart);
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
                  data:['弹幕数量','粉丝弹幕','普通弹幕']
              },
              xAxis: [
                  {
                      type: 'category',
                      data: this.time,
                      axisPointer: {
                          type: 'shadow'
                      }
                  }
              ],
              yAxis: [
                  {
                      type: 'value',
                      name: '分时弹幕',
                      min: 0,
                      max: 10000,
                      interval: 1000,
                      axisLabel: {
                          formatter: '{value} 条'
                      }
                  }
              ],
              series: [
                  {
                      name:'粉丝弹幕',
                      type:'bar',
                      data:this.fans_danmu_num,
                  },
                  {
                      name:'普通弹幕',
                      type:'bar',
                      data:this.normal_danmu_num
                  },
                  {
                      name:'弹幕数目',
                      type:'line',
                      yAxisIndex: 1,
                      data:this.danmu_num_all
                  }]
            })
          },
        //   getDanmuTime(){
        //   let dtime = [];
        //   this.time_exist = this.time_hour;
        //   let nowtimedate = new Date();
        //   let nowtimedate_hour = nowtimedate.getHours();
        //   let nowtimedate_minute = nowtimedate.getMinutes();
        //   nowtimedate_minute = parseInt(nowtimedate_minute / 10) * 10;
        //   let nexttimedate_minute = nowtimedate_minute + 30;
        //   if (nexttimedate_minute >= 60){
        //     nexttimedate_minute = (nexttimedate_minute - 60).toString()
        //   }
        //   if (nowtimedate_minute == 0){
        //     nowtimedate_minute = '00'
        //   }
        //   for(var i=0;i<this,time_hour.length;i++){
        //     if (this.time_hour[i] > nowtimedate_hour){
        //       this.time_delete.push(this.time_hour[i]);
        //       this.time_exist.splice(i, 1)
        //     }
        //   }
        //   dtime = this.time_delete.concat(this.time_exist);
        //   for(var i in dtime){
        //     if (i >= 0 && i<=9){
        //       if (nowtimedate_minute < nexttimedate_minute) {
        //         this.time.push('0' + i + ':' + nowtimedate_minute);
        //         this.time.push('0' + i + ':' + nexttimedate_minute);
        //       }
        //       else{
        //         this.time.push('0' + i + ':' + nexttimedate_minute);
        //         this.time.push('0' + i + ':' + nowtimedate_minute);
        //       }
        //     }
        //     else{
        //       if (nowtimedate_minute < nexttimedate_minute) {
        //         this.time.push(i + ':' + nowtimedate_minute);
        //         this.time.push(i + ':' + nexttimedate_minute);
        //       }
        //       else{
        //         this.time.push(i + ':' + nexttimedate_minute);
        //         this.time.push(i + ':' + nowtimedate_minute);
        //       }
        //     }
        //   }
        // }
      },
      created: function () {
      setInterval(e => {
        // axios.post('http://127.0.0.1:8000/room/danmu_num_data/', {"time": this.time, "yesterdaynum": this.time_delete.length})
        axios.post('http://127.0.0.1:8000/room/danmu_num_data/', {"time_hour": this.time_hour})
        .then(result => {
          let danmudata = result['data'];
          // fans_danmu_num: [],
          //   normal_danmu_num: [],
          //   danmu_num_all: [],
          this.danmu_num_all = danmudata['dmnum'];
          this.normal_danmu_num = danmudata['ndmnum'];
          this.fans_danmu_num = danmudata['fdmnum']
        })
      }, 1800000)
    },
      mounted(){
            this.drawChart()
      },
    }
</script>

<style scoped>

</style>
