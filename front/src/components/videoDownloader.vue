<template>
  <div class="flex flex-col items-center justify-center">
    <h1 class="font-bold text-lg lg:text-4xl lg:mx-12" v-if="data.title  != ''">{{ data.title }}</h1>
    <p class="text-xl lg:text-3xl" v-if="data.view_count  != ''">{{ formatNumber(data.view_count) }} views</p>
    <h2 class="text-lg lg:text-2xl" v-if="data.uploader  != ''">Uploaded by: {{ data.uploader }}</h2>
    <div class="my-2">
        <button @click="downloadVideoFile" class="btn btn-xl btn-primary">Download</button>
    </div>
    <div class="card shadow-xl">
         <video class="max-h-96" v-if="data.filepath  != '' && data.ext == 'mp4' " controls :src="data.filepath"></video>
    </div>
    <audio v-if="data.filepath  != '' && data.ext != 'mp4'" controls :src="data.filepath"></audio>
    <div  class="flex flex-col items-center justify-center mx-16 lg:m-6">
      <p class="text-lg lg:text-md" v-if="data.like_count  != '' && data.like_count == '-1'  ">Likes: {{ formatNumber(data.like_count) }}</p>
      <p class="text-lg lg:text-md" v-if="data.dislike_count  != ''">Dislikes: {{ formatNumber(data.dislike_count) }}</p>
      <p class="text-sm lg:text-md" v-if="data.channel_id  != ''">Channel ID: {{ data.channel_id }}</p>
      <p class="text-sm lg:text-md" v-if="data.uploader_id  != ''">Uploader ID: {{ data.uploader_id }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps } from 'vue';

const props = defineProps({
  data: {
    type: Object,
    required: true
  }
});

const data = ref(props.data);

const sanitizeFilename = (filename) => {
  return filename.replace(/[/\\?%*:|"<>]/g, '_');
};


const downloadVideoFile = async () => {
  if (!props.data.filepath) return;
  const response = await fetch(props.data.filepath);
  const blob = await response.blob();
  const url = URL.createObjectURL(blob);
  const filename = sanitizeFilename(props.data.title+'_KRDBN' || 'KRBDN-DOWNLOAD');
  const fileExtension = props.data.ext || 'mp4';
  const link = document.createElement('a');
  link.href = url;
  link.download = `${filename}.${fileExtension}`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

const formatNumber = (num) => {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
};
</script>

<style scoped>
video {
  max-width: 100%;
  height: auto;
}
</style>