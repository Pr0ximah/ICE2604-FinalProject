<script setup>
import { ref, toRaw, watch } from 'vue'
import * as echarts from 'echarts'
import { theme as roma_theme } from './roma'
import { theme as macarons_theme } from './macarons'

const chart = ref()
let myChart = null;
const props = defineProps({
    data: Object
})

function itemInDict(item, dict) {
    let flag = false
    for (let key in dict) {
        if (item === dict[key]) {
            flag = true
            break
        }
    }
    return flag
}

function getNodesAndLinks(dic, authorname) {
    let big_lst = []
    let lst_nodes = []
    let lst_links = []
    let store = []
    let i = 1
    store.push(authorname)
    let newDic = {}
    newDic["id"] = 0
    newDic["category"] = 0
    newDic["name"] = authorname
    newDic["symbolSize"] = 80
    newDic.ignore = false
    newDic.flag = true
    lst_nodes.push(newDic)
    let f = {}
    f[authorname] = 0
    let leavesStyle = {
        borderWidth: 2,
        color: '#c1f1ef',
    }
    for (var key in dic) {
        if (!(itemInDict(authorname, dic[key]['_source']["authors"]))) {
            continue
        }
        for (var j = 0; j < dic[key]['_source']["authors"].length; j++) {
            let au = "I"
            let flag_1 = true
            for (var m = 0; m < store.length; m++) {
                if (dic[key]['_source']["authors"][j] == store[m]) {
                    flag_1 = false
                    au = store[m]
                }
            }
            if (flag_1) {
                store.push(dic[key]['_source']["authors"][j])
                f[dic[key]['_source']["authors"][j]] = i
                let newDicAuthor = {}
                newDicAuthor["id"] = i
                i++
                newDicAuthor["category"] = 1
                newDicAuthor["name"] = dic[key]['_source']["authors"][j]
                newDicAuthor["symbolSize"] = 80
                newDicAuthor.ignore = true
                newDicAuthor.flag = true
                lst_nodes.push(newDicAuthor)

                let newDicTitle = {}
                newDicTitle["id"] = i
                i++
                newDicTitle["category"] = 2
                newDicTitle["name"] = dic[key]['_source']["title"]
                newDicTitle["symbolSize"] = 60
                newDicTitle["itemStyle"] = leavesStyle
                newDicTitle["emphasis"] = { scale: 'false', itemStyle: { color: '#c1f1ef' } }
                newDicTitle.ignore = true
                newDicTitle.flag = true
                lst_nodes.push(newDicTitle)

                let newLink_1 = {}
                newLink_1["source"] = newDicAuthor["id"]
                newLink_1["target"] = 0

                let newLink_2 = {}
                newLink_2["source"] = newDicTitle["id"]
                newLink_2["target"] = newDicAuthor["id"]
                lst_links.push(newLink_1)
                lst_links.push(newLink_2)
                continue
            }
            else {
                if (au == authorname) {
                    continue
                }
                let newDicTitle = {}
                newDicTitle["id"] = i
                i++
                newDicTitle["category"] = 2
                newDicTitle["name"] = dic[key]['_source']["title"]
                newDicTitle["symbolSize"] = 60
                newDicTitle["itemStyle"] = leavesStyle
                newDicTitle["emphasis"] = { scale: 'false', itemStyle: { color: '#c1f1ef' } }
                newDicTitle.ignore = true
                newDicTitle.flag = true
                lst_nodes.push(newDicTitle)

                let newLink_2 = {}
                newLink_2["source"] = newDicTitle["id"]
                newLink_2["target"] = f[au]
                lst_links.push(newLink_2)
                continue
            }
        }
    }
    for (let i = 0; i < lst_nodes.length; i++) {
        lst_nodes[i]["id"] = String(lst_nodes[i]["id"])
    }
    for (let i = 0; i < lst_links.length; i++) {
        lst_links[i]["source"] = String(lst_links[i]["source"])
        lst_links[i]["target"] = String(lst_links[i]["target"])
    }
    big_lst.push(lst_nodes)
    big_lst.push(lst_links)
    return big_lst
}

function openOrFold(param) {
    var option = myChart.getOption();
    var nodesOption = option.nodes_ori;
    var linksOption = option.series[0].links;
    var data = param.data;
    var linksNodes = [];

    var categoryLength = option.series[0].categories.length;

    if (data != null && data != undefined) {
        if (data.flag) {
            for (var m in linksOption) {
                if (linksOption[m].target == data.id) {
                    linksNodes.push(linksOption[m].source);
                }
            }
            if (linksNodes != null && linksNodes != undefined) {
                for (var p in linksNodes) {
                    nodesOption[linksNodes[p]].ignore = false;
                    nodesOption[linksNodes[p]].flag = true;
                }
            }
            nodesOption[data.id].flag = false;
            let nodes_filtered = refreshOption(option.nodes_ori)
            option.series[0].nodes = nodes_filtered
            myChart.setOption(option);
        } else {
            for (var m in linksOption) {
                if (linksOption[m].target == data.id) {
                    linksNodes.push(linksOption[m].source);
                }
                if (linksNodes != null && linksNodes != undefined) {
                    for (var n in linksNodes) {
                        if (linksOption[m].target == linksNodes[n]) {
                            linksNodes.push(linksOption[m].source);
                        }
                    }
                }
            }
            if (linksNodes != null && linksNodes != undefined) {
                for (var p in linksNodes) {
                    nodesOption[linksNodes[p]].ignore = true;
                    nodesOption[linksNodes[p]].flag = true;
                }
            }
            nodesOption[data.id].flag = true;
            let nodes_filtered = refreshOption(option.nodes_ori)
            option.series[0].nodes = nodes_filtered
            myChart.setOption(option);
        }
    }
}

watch(props, () => {
    setTimeout(() => {
        refreshChart()
    }, 200);
})
// defineExpose({ init, refreshChart, resizeChart })
defineExpose({ init, resizeChart })

function init(data, author) {
    echarts.registerTheme('roma', macarons_theme)
    var big_lst = getNodesAndLinks(data, author)
    let nodes_filtered = refreshOption(big_lst[0])
    var option = {
        nodes_ori: big_lst[0],
        tooltip: {
            show: false
        },
        animation: true,
        animationDuration: 500,
        // title: {
        //     text: "Authors Force Graph",
        //     textStyle: {
        //         color: '#2160c4',
        //         fontSize: '25',
        //     }
        // },
        series: [{
            focusNodeAdjacency: true,
            type: 'graph',
            zoom: 0.8,
            layout: 'force',
            roam: true,
            labelLayout: {
                // hideOverlap: 'true',
            },
            emphasis: {
                scale: 1.05,
                itemStyle: {
                    label: {
                        show: true,
                        textStyle: {
                            fontSize: 16,
                            position: 'inside',
                            fontWeight: 600,
                            color: '#1636b6',
                        },
                        ellipsis: '...',
                        width: '50px',
                        overflow: 'break',
                    },
                    borderWidth: '3',
                    borderColor: '#bdd2f4',
                    borderType: 'solid',
                    color: '#e1ebf9',
                }
            },
            animationEasing: 'cubicInOut',
            itemStyle: {
                normal: {
                    label: {
                        show: true,
                        textStyle: {
                            fontSize: 16,
                            position: 'inside',
                            fontWeight: 600,
                            color: '#1636b6',
                        },
                        ellipsis: '...',
                    },
                    borderWidth: '3',
                    borderColor: '#e1ebf9',
                    borderType: 'solid',
                    color: '#f0f7ff',
                },
            },
            lineStyle: {
                normal: {
                    color: '#142f9f',
                    width: 4,
                    type: 'solid',
                    curveness: 0,
                }
            },
            // symbol: 'roundRect',
            symbol: 'circle',
            categories: [{
                name: 'main_author'
            }, {
                name: 'co_author'
            }, {
                name: 'title'
            }],
            draggable: true,
            nodes: nodes_filtered,
            links: big_lst[1],
            force: {
                initLayout: 'circular',
                edgeLength: 120,
                repulsion: 800,
                friction: 0.6,
            },
        }],
    };
    myChart = echarts.init(chart.value, 'roma');
    myChart.setOption(option);
    myChart.on('click', openOrFold);
}

function refreshOption(nodes) {
    let filterList = []
    for (let i = 0; i < nodes.length; i++) {
        if (nodes[i].ignore == false) {
            filterList.push(nodes[i])
        }
    }
    return filterList
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