<script setup>
import { ref, toRaw, watch } from 'vue'
import * as echarts from 'echarts'

const chart = ref()
let myChart = null;

const props = defineProps({
    data: Object
})

watch(props, () => {
    setTimeout(() => {
        refreshChart()
    }, 200);
})
defineExpose({ init, refreshChart, resizeChart })

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
    // for (var j = 0; j < lst.length - 1; j++) {
    //     if (lst[j] > lst[j + 1]) {
    //         var tmp = lst[j + 1]
    //         lst[j + 1] = lst[j]
    //         lst[j] = tmp
    //     }
    // }
    lst.sort(function (a, b) { return a - b })
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
        // for (var j = 1; j < lst.length - 1; j++) {
        //     if (lst[j][0] > lst[j + 1][0]) {
        //         var tmp = lst[j + 1]
        //         lst[j + 1] = lst[j]
        //         lst[j] = tmp
        //     }
        // }
        lst.sort(function (a, b) { return a[0] - b[0] })
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
    let y_max = lst_ydata[0]
    for (let i = 1; i < lst_ydata.length; i++) {
        if (y_max < lst_ydata[i]) { y_max = lst_ydata[i] }
    }
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
            show: lst_xdata.length > 0,
            feature: {
                // dataView: { show: true, readOnly: false },
                magicType: { show: true, type: ['line', 'bar'] },
                // restore: { show: true },
                // saveAsImage: { show: true }
            },
            right: '0',
        },
        title: {
            show: lst_xdata.length > 0,
            text: "Count / Year",
        },
        xAxis: [
            {
                show: lst_xdata.length > 0,
                type: 'category',
                data: lst_xdata,
                axisPointer: {
                    type: 'shadow'
                },
                invisible: lst_xdata.length === 0,
            }
        ],
        yAxis: [
            {
                type: 'value',
                interval: 1,
                max: y_max + 1,
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
                animationDuration: 500,
                animationEasing: "cubicInOut",
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
        graphic: {
            type: 'text',
            left: 'center',
            top: 'middle',
            silent: true,
            invisible: lst_xdata.length > 0,
            style: {
                fill: '#9d9d9d',
                fontWeight: 'bold',
                text: 'No data',
                // fontFamily: 'Microsoft YaHei',
                fontSize: '25px'
            }
        }
    }
    return option
}

function init() {
    if (props.data === undefined) {
        return
    }
    let searchResultRaw = toRaw(props.data)
    let searchResult = Array()
    for (let i = 0; i < searchResultRaw.length; i++) {
        searchResult.push(searchResultRaw[i]['_source'])
    }

    myChart = echarts.init(chart.value);
    let option = Bar_authorSearch(searchResult)
    myChart.setOption(option);
}

function refreshChart() {
    let searchResultRaw = toRaw(props.data)
    let searchResult = Array()
    for (let i = 0; i < searchResultRaw.length; i++) {
        searchResult.push(searchResultRaw[i]['_source'])
    }

    let option = Bar_authorSearch(searchResult)
    // chart.value.setAttribute('_echarts_instance_', '')
    // myChart = echarts.init(chart.value);
    myChart.setOption(option, true, true);
}

function resizeChart() {
    if (myChart) {
        myChart.resize()
    }
}
</script>

<template>
    <div ref="chart" class="chartYearOri" id="1"></div>
</template>