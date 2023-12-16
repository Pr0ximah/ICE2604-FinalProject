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

var diction = {
    "elsevier_05cbcb9ef5629bc25e84df43572f9d1eddb9a35f": {
        "date": "1981-12-01T00:00:00",
        "ref_paper": [],
        "conference": "",
        "keywords": [],
        "year": 1981,
        "author": {
            "affiliation": [
                "Chemistry Department, B-017, University of California at San Diego, La Jolla, CA 92093 U.S.A.",
                "Chemistry Department, B-017, University of California at San Diego, La Jolla, CA 92093 U.S.A."
            ],
            "name": [
                "zwz",
                "hac"
            ]
        },
        "last_page": 8,
        "link": "https://www.sciencedirect.com/science/article/abs/pii/0012821X81901126",
        "abstract": "Pristine samples from the lunar highlands potentially offer important information bearing on the nature of early crustal development on all the terrestrial planets. One apparently unique sample of this group of lunar crustal rocks, the feldspathic lherzolite 67667, was studied utilizing the Sm-Nd radiometric system in an attempt to define its age and the implications of that age for the evolution of the lunar highlands. Data for 67667 precisely define an isochron corresponding to an age of 4.18\u00b10.07 AE. The observed lack of disturbance of the Sm-Nd system of this sample may suggest that this time marks its crystallization at shallow depth in the lunar crust. However, the possibility that this age, as well as those of other highland rocks, indicate the time of their impact-induced excavation from regions deep enough in the lunar crust to allow subsolidus isotopic equilibrium to be produced or maintained between their constituent minerals is also considered. Taken together, bulk rock Sm-Nd data for four \u201chigh-Mg\u201d rocks, including 67667, indicate that the chemical characteristics of all their source materials were established 4.33\u00b10.08 AE ago and were intimately associated with the parent materials of KREEP. This finding provides more support for the concept of a large-scale differentiation episode early in lunar history. The possible roles of the crystallization of a global magma ocean, endogenous igneous activity, and of planetesimal impact, in producing the observed geochemical and chronological aspects of lunar highland rocks are discussed.",
        "title": "Sm-Nd age of lherzolite 67667: implications for the processes involved in lunar crustal formation",
        "paper_id": "elsevier_05cbcb9ef5629bc25e84df43572f9d1eddb9a35f",
        "volume": 56,
        "update_time": "2022-07-16T14:06:08.117141",
        "journal": "Earth and Planetary Science Letters",
        "issn": "0012-821X",
        "first_page": 1,
        "publisher": "elsevier",
        "doi": "10.1016/0012-821X(81)90112-6"
    },
    "elsevier_0d8e1fc979302d36e57072865329cbb30781292d": {
        "date": "2011-12-01T00:00:00",
        "ref_paper": [],
        "conference": "",
        "keywords": [
            "jjs",
            "hac",
            "myb",
            "hbj",
            "zwz",
            "climate change"
        ],
        "year": 100,
        "author": {
            "affiliation": [
                "Institute of Geography and Geology, University of Copenhagen, \u00d8ster Voldgade 10, 1350 Copenhagen, Denmark$$$Nordic Center for Earth evolution, NordCEE, University of Copenhagen, Denmark",
                "Departemento de Geolog\u00eda, Facultat de Ciencias, Igu\u00e1 4225, 11400 Montevideo, Uruguay",
                "Institute of Geography and Geology, University of Copenhagen, \u00d8ster Voldgade 10, 1350 Copenhagen, Denmark$$$Nordic Center for Earth evolution, NordCEE, University of Copenhagen, Denmark",
                "NEG-LABISE, Departemento de Geologia, Universidade Federal de Pernambuco, Brazil"
            ],
            "name": [
                "zwz",
                "hac",
                "myb",
                "hbj",
            ]
        },
        "last_page": 125,
        "link": "https://www.sciencedirect.com/science/article/pii/S0012821X11005966",
        "abstract": "Strontium and carbon isotopes of marine carbonates are routinely applied for chemostratigraphic cross correlations of time-equivalent sedimentary sequences and for calibration of the compositional evolution of seawater throughout Earth's history, mainly for the purpose of reconstructing ancient climatic changes. We here present results of a new isotopic tracer system \u2013 stable chromium isotopes \u2013 applied to a late Ediacaran marine carbonate sequence exposed in the Calera de Recalde syncline, Arroyo del Soldado Group, Uruguay. The aim was to compare Cr isotope signatures directly to \u03b4C, Sr/Sr and Nd/Nd fluctuations in a well defined stratigraphic profile comprising sediments that were deposited during cold\u2013warm periods accompanied by sea-level changes in response to glaciation\u2013deglaciation at higher latitudes. The studied section is characterized by a pronounced negative (down to \u2212 3.3\u2030) \u03b4C excursion in carbonates paralleled by a decrease of Sr/Sr values. Chromium isotope signatures over this section also show a correlated decrease in \u03b4Cr (\u03b4Cr = [((Cr/Cr) / (Cr/Cr)) \u2212 1] \u00d7 1000) values from ~+0.29 to \u2212 0.17\u2030 which mirrors a decrease in positively fractioned seawater signatures to slightly negative values characteristic of high-temperature magmatic sources. Linear correlations between \u03b4Cr and \u03b5Nd(570 Ma), Sr/Sr and Cr concentrations can be explained by mixing between two major input sources of Cr, Nd and Sr into the shallow seawater: 1) a source characterized by negative \u03b4Cr values of ~\u22120.2\u2030 , low Sr/Sr values of ~ 0.707, and elevated Sm/Nd values of ~ 0.13, recognized as a subaqueous hydrothermal dominated input source, and 2) a source characterized by positively fractionated \u03b4Cr values of ~+0.2\u2030, higher Sr/Sr values of ~ 0.708, and lower Sm/Nd values of ~ 0.11, a source which is strongly affected by continentally derived input. Chromium isotopes provide a powerful tool for reconstructing the redox state of ancient seawater since positive values indicate that, at least locally, Neoproterozoic shallow ocean waters were sufficiently oxidized to fractionate chromium and/or that oxygen levels of the atmosphere were sufficient to transform Cr(III) into the more mobile hexavalent Cr(VI) formed during weathering processes on land.The fact that Sr/Sr values, despite \u03b4C fluctuations, remain low (indicative of a strong hydrothermal input into the basin at his time) implies that CO limitation was the cause of negative \u03b4C and \u03b4Cr excursions in otherwise nutrient rich late Neoproterozoic basins, and that glaciation is only one more consequence of a tectonically driven, biologically mediated system. In such a scenario, glaciation acts as an amplifier of \u03b4Cr signals. These signals in marine carbonates are a sensitive tracer for redox processes in the ocean and/or on land and have the potential to contribute significantly, in combination with the other commonly used isotopic tracers, to the reconstruction of climatic changes, particularly those that are associated with major glaciation periods in Earth's history.\u25ba Systematic Cr isotope record over a Late Ediacaran negative \u03b4C excursion. \u25ba Covariations between Sr, Nd and Cr isotopes imply a two source mixing. \u25ba Mirroring of the \u03b4C excursion by \u03b4Cr reflects changes in bioproductivity. \u25ba Cr isotopes in marine carbonates potentially monitor atmospheric fluctuations.",
        "title": "Chromium isotopes in carbonates \u2014 A tracer for climate change and for reconstructing the redox state of ancient seawater",
        "paper_id": "elsevier_0d8e1fc979302d36e57072865329cbb30781292d",
        "volume": 312,
        "update_time": "2021-12-12T01:15:43.331000",
        "journal": "Earth and Planetary Science Letters",
        "issn": "0012-821X",
        "first_page": 114,
        "publisher": "elsevier",
        "doi": "10.1016/J.EPSL.2011.10.009"
    },
    "elsevier_0d8e1fc979302d36e57072865329cbb30781292": {
        "date": "2011-12-01T00:00:00",
        "ref_paper": [],
        "conference": "",
        "keywords": [
            "zwz",
            "hac",
            "myb",
            "hbj",
        ],
        "year": 100,
        "author": {
            "affiliation": [
                "Institute of Geography and Geology, University of Copenhagen, \u00d8ster Voldgade 10, 1350 Copenhagen, Denmark$$$Nordic Center for Earth evolution, NordCEE, University of Copenhagen, Denmark",
                "Departemento de Geolog\u00eda, Facultat de Ciencias, Igu\u00e1 4225, 11400 Montevideo, Uruguay",
                "Institute of Geography and Geology, University of Copenhagen, \u00d8ster Voldgade 10, 1350 Copenhagen, Denmark$$$Nordic Center for Earth evolution, NordCEE, University of Copenhagen, Denmark",
                "NEG-LABISE, Departemento de Geologia, Universidade Federal de Pernambuco, Brazil"
            ],
            "name": [
                "zwz",
                "hac",
                "L.N. D\u00f8ssing",
                "jjc"
            ]
        },
        "last_page": 125,
        "link": "https://www.sciencedirect.com/science/article/pii/S0012821X11005966",
        "abstract": "Strontium and carbon isotopes of marine carbonates are routinely applied for chemostratigraphic cross correlations of time-equivalent sedimentary sequences and for calibration of the compositional evolution of seawater throughout Earth's history, mainly for the purpose of reconstructing ancient climatic changes. We here present results of a new isotopic tracer system \u2013 stable chromium isotopes \u2013 applied to a late Ediacaran marine carbonate sequence exposed in the Calera de Recalde syncline, Arroyo del Soldado Group, Uruguay. The aim was to compare Cr isotope signatures directly to \u03b4C, Sr/Sr and Nd/Nd fluctuations in a well defined stratigraphic profile comprising sediments that were deposited during cold\u2013warm periods accompanied by sea-level changes in response to glaciation\u2013deglaciation at higher latitudes. The studied section is characterized by a pronounced negative (down to \u2212 3.3\u2030) \u03b4C excursion in carbonates paralleled by a decrease of Sr/Sr values. Chromium isotope signatures over this section also show a correlated decrease in \u03b4Cr (\u03b4Cr = [((Cr/Cr) / (Cr/Cr)) \u2212 1] \u00d7 1000) values from ~+0.29 to \u2212 0.17\u2030 which mirrors a decrease in positively fractioned seawater signatures to slightly negative values characteristic of high-temperature magmatic sources. Linear correlations between \u03b4Cr and \u03b5Nd(570 Ma), Sr/Sr and Cr concentrations can be explained by mixing between two major input sources of Cr, Nd and Sr into the shallow seawater: 1) a source characterized by negative \u03b4Cr values of ~\u22120.2\u2030 , low Sr/Sr values of ~ 0.707, and elevated Sm/Nd values of ~ 0.13, recognized as a subaqueous hydrothermal dominated input source, and 2) a source characterized by positively fractionated \u03b4Cr values of ~+0.2\u2030, higher Sr/Sr values of ~ 0.708, and lower Sm/Nd values of ~ 0.11, a source which is strongly affected by continentally derived input. Chromium isotopes provide a powerful tool for reconstructing the redox state of ancient seawater since positive values indicate that, at least locally, Neoproterozoic shallow ocean waters were sufficiently oxidized to fractionate chromium and/or that oxygen levels of the atmosphere were sufficient to transform Cr(III) into the more mobile hexavalent Cr(VI) formed during weathering processes on land.The fact that Sr/Sr values, despite \u03b4C fluctuations, remain low (indicative of a strong hydrothermal input into the basin at his time) implies that CO limitation was the cause of negative \u03b4C and \u03b4Cr excursions in otherwise nutrient rich late Neoproterozoic basins, and that glaciation is only one more consequence of a tectonically driven, biologically mediated system. In such a scenario, glaciation acts as an amplifier of \u03b4Cr signals. These signals in marine carbonates are a sensitive tracer for redox processes in the ocean and/or on land and have the potential to contribute significantly, in combination with the other commonly used isotopic tracers, to the reconstruction of climatic changes, particularly those that are associated with major glaciation periods in Earth's history.\u25ba Systematic Cr isotope record over a Late Ediacaran negative \u03b4C excursion. \u25ba Covariations between Sr, Nd and Cr isotopes imply a two source mixing. \u25ba Mirroring of the \u03b4C excursion by \u03b4Cr reflects changes in bioproductivity. \u25ba Cr isotopes in marine carbonates potentially monitor atmospheric fluctuations.",
        "title": "Chromium isotopes in carbonates \u2014 A tracer for climate change and for reconstructing the redox state of ancient seawater",
        "paper_id": "elsevier_0d8e1fc979302d36e57072865329cbb30781292d",
        "volume": 312,
        "update_time": "2021-12-12T01:15:43.331000",
        "journal": "Earth and Planetary Science Letters",
        "issn": "0012-821X",
        "first_page": 114,
        "publisher": "elsevier",
        "doi": "10.1016/J.EPSL.2011.10.009"
    }
}

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

// function refreshChart() {
//     let searchResultRaw = toRaw(props.data)
//     let searchResult = Array()
//     for (let i = 0; i < searchResultRaw.length; i++) {
//         searchResult.push(searchResultRaw[i]['_source'])
//     }

//     let option = Bar_authorSearch(searchResult)
//     // chart.value.setAttribute('_echarts_instance_', '')
//     // myChart = echarts.init(chart.value);
//     myChart.setOption(option, true, true);
// }

function resizeChart() {
    if (myChart) {
        myChart.resize()
    }
}
</script>

<template>
    <div ref="chart" class="chartYearOri" id="1"></div>
</template>