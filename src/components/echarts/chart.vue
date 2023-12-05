<script setup>
import { ref, toRaw } from 'vue'
import * as echarts from 'echarts'

const chart = ref()

const props = defineProps({
    data: Object
})

defineExpose({init})

function init() {
    if (props.data === undefined) {
        return
    }
    let searchResultRaw = toRaw(props.data)
    let searchResult = Array()
    for (let i = 0; i < searchResultRaw.length; i++) {
        searchResult.push(searchResultRaw[i]['_source'])
    }

    let myChart = echarts.init(chart.value);
    // window.addEventListener('resize', function () {
    //     myChart.resize();
    // });

    // authorSearch
    function getData_authorSearch(dic) {
        let lst = []
        for (var key in dic) {
            let flag = true
            for (var k = 0; k < lst.length; k++) {
                if (dic[key]["year"] == lst[k]) {
                    flag = false
                    break
                }
            }
            if (flag == true) {
                lst.push(dic[key]["year"])
            }
        }
        for (var j = 0; j < lst.length - 1; j++) {
            if (lst[j] > lst[j + 1]) {
                var tmp = lst[j + 1]
                lst[j + 1] = lst[j]
                lst[j] = tmp
            }
        }
        return lst
    }
    function changeToBar_authorSearch(dic) {
        let n = 0
        let lst = [[]]
        for (var key in dic) {
            lst.push([])
        }
        lst[0][0] = "product"
        lst[0][1] = "vloume"
        let i = 1
        let temp = {}
        for (var key in dic) {
            if (dic[key]["year"] in temp) {
                temp[dic[key]["year"]] += 1
            }
            else {
                temp[dic[key]["year"]] = 1
            }
        }
        let store = []
        for (var key in dic) {
            let flag = true
            for (var k = 0; k < lst.length; k++) {
                if (dic[key]["year"] == store[k]) {
                    flag = false
                    break
                }
            }
            if (flag == true) {
                lst[i][0] = dic[key]["year"]
                lst[i][1] = temp[dic[key]["year"]]
                store.push(dic[key]["year"])
                i = i + 1
            }
        }
        for (var m = 1; m < lst.length - 1; m++) {
            for (var j = 1; j < lst.length - 1; j++) {
                if (lst[j][0] > lst[j + 1][0]) {
                    var tmp = lst[j + 1]
                    lst[j + 1] = lst[j]
                    lst[j] = tmp
                }
            }
        }
        return lst
    }
    function getydata(dic) {
        let lst = changeToBar_authorSearch(dic)
        let lst_result = []
        for (var m = 1; m < lst.length; m++) {
            lst_result.push(lst[m][1])
        }
        return lst_result
    }
    function Bar_authorSearch(dic) {
        let lst_xdata = getData_authorSearch(dic)
        let lst_ydata = getydata(dic)
        let option = {
            color: ['#2a6fdb'],
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
                    // dataView: { show: true, readOnly: false },
                    magicType: { show: true, type: ['line', 'bar'] },
                    // restore: { show: true },
                    // saveAsImage: { show: true }
                },
                x: '75%',
            },
            legend: {
                data: ["year"]
            },
            title: {
                show: true,
                text: "Paper Count / Year"
            },
            xAxis: [
                {
                    type: 'category',
                    data: lst_xdata,
                    axisPointer: {
                        type: 'shadow'
                    },
                }
            ],
            yAxis: [
                {
                    type: 'value',
                    interval: 1,
                    axisLabel: {
                        formatter: '{value}'
                    }
                }
            ],
            series: [
                {
                    type: 'bar',
                    tooltip: {
                        valueFormatter: function (value) {
                            return value + '篇';
                        }
                    },
                    data: lst_ydata,
                }
            ],
            grid: [
                {
                    x: '8%',
                    x2: '5%',
                    y: '20%',
                    y2: '10%',
                }
            ],
            textStyle: {
                fontFamily: 'Helvetica',
            },
        }
        return option
    }
    let option = Bar_authorSearch(searchResult)
    myChart.setOption(option);
}
</script>

<template>
    <div ref="chart" class="chart"></div>
</template>