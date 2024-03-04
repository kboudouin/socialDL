<script setup>
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';
import infoText from './infoText.vue';
import videoDownloader from './videoDownloader.vue';

const videoUrl = ref('');
const videoData = ref(null);
const token = ref('');
const errorMessage = ref('');
const loading = ref(false);
const BASE_URL = 'http://api.krbdn.com'

onMounted(async () => {
  try {
    const response = await axios.post(`${BASE_URL}/api/generate-token`);
    if (response.data && response.data.token) {
      token.value = response.data.token;
      localStorage.setItem('token', token.value);
    }
  } catch (error) {
    console.error(error);
  }
});

async function downloadVideo() {
  if (!videoUrl.value) {
    errorMessage.value = 'URL cannot be empty';
    return;
  }
  loading.value = true;
  const token = localStorage.getItem('token');
  const formData = new FormData();
  formData.append('url', videoUrl.value);
  try {
    const response = await axios.post(`${BASE_URL}/api/download-video`, formData, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'multipart/form-data'
      }
    });
    if (response.data) {
      videoData.value = response.data;
    }
    loading.value = false;
  } catch (error) {
    console.error(error);
    loading.value = false;
  }
  videoUrl.value = '';
}


</script>

<template>
  <div class="flex flex-col items-center justify-center lg:mx-8 my-4">
    <div class="flex flex-col items-center justify-center">
      <h1 class="text-5xl font-bold">Video Downloader</h1>
      <p class="text-2xl font-bold">Youtube, Tiktok, Instagram Reels, </p>
    </div>
  </div>
  <div class="flex items-center justify-center lg:mx-12">
    <input v-model="videoUrl" type="text"  placeholder="Ex : https://www.youtube.com/watch?v=dQw4w9WgXcQ" class="input input-bordered input-primary w-1/2" />
    <button  @click="downloadVideo" class="btn btn-primary">Go!</button>
  </div>
  <div class="flex items-center justify-center mt-4">
   <p class="text-red-500">{{ errorMessage }}</p>
  </div>
  <!-- <infoText v-if="!videoData" /> -->
  <div v-if="loading" class="flex items-center justify-center mt-4">
   <span class="loading loading-spinner loading-lg"></span>
  </div>

  <videoDownloader v-if="videoData && !loading" :data="videoData" />
</template>

<style scoped>
</style>