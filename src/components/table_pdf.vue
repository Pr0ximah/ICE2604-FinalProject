<script setup>
import API from './axios_instance'
import { ref, onMounted } from 'vue'
import { ElLoading, ElPagination, ElTable, ElTableColumn } from 'element-plus';
const props = defineProps({
    paperid: Object
})
const show = ref(false)
const tables = ref()
const base = process.env.NODE_ENV === "development" ? "/data_proxy" : "/api"
let table_num = ref(0)

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
            show.value = true
            tables.value = e.data
            console.log(tables.value)
        } else {
            show.value = false
        }
    })
})

function convertTableHead(head) {
    if (String(head).startsWith("empty")) {
        return ""
    } else {
        return head
    }
}
</script>

<template>
    <div v-if="show" style="margin-left: 20px; margin-top: 20px; margin-right: 20px; align-items: center; max-width: 100%;">
        <span style="margin-left: 5px; margin-right: 5px; display: flex; margin-bottom: 0;">
            <span class="inflogo">
                Tables
            </span>
            <span class="cardtable"
                style="margin-left: 20px; margin-right: 15px; padding-left: 5px; padding-right: 5px; width: calc(100% - 110px);">
                <div>
                    <ElTable :data="tables[table_num].data" max-height="600px" style="max-width: 100%;">
                        <ElTableColumn v-for="headitem in tables[table_num].head" :prop="headitem" :label="convertTableHead(headitem)" />
                    </ElTable>
                </div>
            </span>
        </span>
        <div style="width: 100%; display: flex; justify-content: right;">
            <span style="justify-self: left; margin-left: 20px; margin-top: 15px; text-align: center; font-size: smaller; font-weight: 600; color: gray; display: flex; align-items: center;">
                table in page {{ tables[table_num].page_num }}
            </span>
            <ElPagination class="table" background style="margin-top: 15px; margin-right: 20px;" layout="prev, next" :page-count="tables.length"
                @current-change="(val) => { table_num = val - 1 }" />
        </div>
    </div>
</template>