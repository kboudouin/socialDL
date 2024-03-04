<template>
  <div class="flex flex-col items-center justify-center">
    <h1 class="font-bold text-4xl lg:mx-12" v-if="data.title  != ''">{{ data.title }}</h1>
    <p class="text-3xl" v-if="data.view_count  != ''">{{ formatNumber(data.view_count) }} views</p>
    <h2 v-if="data.uploade  != ''">Uploaded by: {{ data.uploader }}</h2>
    <div class="my-2">
        <button @click="downloadVideoFile" class="btn btn-xl btn-primary">Download</button>
    </div>
    <!-- <img v-if="data.thumbnail  != ''" :src="data.thumbnail" alt="Thumbnail"> -->
    <div class="lg:w-1/2 card shadow-xl">
         <video class="" v-if="data.filepath  != ''" controls :src="data.filepath"></video>
    </div>
    <p v-if="data.like_count  != '' && data.like_count == '-1'  ">Likes: {{ formatNumber(data.like_count) }}</p>
    <p v-if="data.dislike_count  != ''">Dislikes: {{ formatNumber(data.dislike_count) }}</p>
    <p v-if="data.channel_id  != ''">Channel ID: {{ data.channel_id }}</p>
    <p v-if="data.uploader_id  != ''">Uploader ID: {{ data.uploader_id }}</p>

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

const downloadVideoFile = async () => {
  const response = await fetch(props.data.filepath);
  const blob = await response.blob();
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = '';
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