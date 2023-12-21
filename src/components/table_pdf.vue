<script setup>
import API from './axios_instance'
import { ref, onMounted } from 'vue'
import { ElLoading, ElTable, ElTableColumn } from 'element-plus';
const props = defineProps({
    paperid: Object
})
const show = ref(false)
const tables = ref()
const base = process.env.NODE_ENV === "development" ? "/data_proxy" : "/api"

onMounted(() => {
    const loading = ElLoading.service({
        lock: true,
        background: 'rgba(0, 0, 0, 0.15)',
    })
    const id = props.paperid
    API({
        url: base + `/get_table`,
        method: 'post',
        data: {
            id: id,
        }
    }).then((e) => {
        loading.close()
        if (e.data) {
            console.log(e.data)
            show.value = true
            tables.value = e.data
        } else {
            show.value = false
        }
    })
})
</script>

<template>
    <div v-if="show" v-for="table in tables" style="margin-left: 20px; margin-top: 20px; margin-right: 20px; align-items: center;">
        <span style="margin-left: 5px; margin-right: 5px; display: flex;">
            <span class="inflogo">
                Tables
            </span>
            <span class="cardtable"
                style="margin-left: 20px; margin-right: 15px; padding-left: 5px; padding-right: 5px; width: 100%;">
                <div>
                    <ElTable :data="table.data" table-layout="auto">
                        <ElTableColumn v-for="headitem in table.head" :prop="headitem" :label="headitem"/>
                    </ElTable>
                </div>
            </span>
        </span>
    </div>
</template>