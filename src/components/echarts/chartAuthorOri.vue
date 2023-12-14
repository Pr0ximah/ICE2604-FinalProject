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
    <div>test</div>
</template>