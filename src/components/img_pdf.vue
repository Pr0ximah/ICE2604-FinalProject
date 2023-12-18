<script setup>
import API from './axios_instance'
import { ref, onMounted } from 'vue'
import { ElLoading } from 'element-plus';
const props = defineProps({
    paperid: Object
})
const show = ref(false)
const images = ref()
const base = process.env.NODE_ENV === "development" ? "/data_proxy" : "/api"

onMounted(() => {
    const loading = ElLoading.service({
        lock: true,
        background: 'rgba(0, 0, 0, 0.15)',
    })
    const id = props.paperid
    API({
        url: base + `/get_img`,
        method: 'post',
        data: {
            id: id,
        }
    }).then((e) => {
        loading.close()
        if (e.data) {
            console.log(e.data)
            show.value = true
            images.value = e.data
        } else {
            show.value = false
        }
    })
})

function openImg(file) {
    window.open(file, "_blank")
}
</script>

<template>
    <div v-if="show" style="margin-left: 20px; margin-top: 20px; margin-right: 20px; align-items: center;">
        <span style="margin-left: 5px; margin-right: 5px; display: flex;">
            <span class="inflogo">
                Images
            </span>
            <span
                style="margin-left: 5px; margin-right: 5px; font-size: smaller; line-height: 1.5em; padding-left: 5px; padding-right: 5px; width: 100%;">
                <div class="scroll" style="height: 240px; display: flex; flex-direction: row; overflow-x: auto;">
                    <ElImage class="card-pdf-img" v-for="image in images" :src="base + image" fit="contain"
                        style="margin: 6px; margin-top: 0; margin-bottom: 6px; max-width: 100%; max-height: 100%; width: auto; height: auto; flex:none;"
                        :preview-src-list="[base + image]" :close-on-press-escape="true" :hide-on-click-modal="true" />
                </div>
            </span>
        </span>
    </div>
</template>