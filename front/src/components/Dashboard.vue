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
const BASE_URL = 'https://api.krbdn.com'
const selectedType = ref(localStorage.getItem('SelectedType') || 'mp4');
const infoVisible = ref(true);

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

watch(selectedType, (newType) => {
  localStorage.setItem('SelectedType', newType);
});

async function downloadVideo() {
  if (!videoUrl.value) {
    errorMessage.value = 'URL cannot be empty';
    return;
  }
  infoVisible.value = false;
  loading.value = true;
  const token = localStorage.getItem('token');
  const formData = new FormData();
  formData.append('format', selectedType.value);
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
    errorMessage.value = 'Oups! Sorry we could not download the video!';
    console.error(error);
    loading.value = false;
  }
  videoUrl.value = '';
}


</script>

<template>
  <div class="flex flex-col items-center justify-center lg:mx-8 my-6">
    <div class="flex flex-col items-center justify-center">
      <h1 class="text-5xl font-bold">Video Downloader</h1>
    </div>
  </div>
  <div class="flex items-center justify-center lg:mx-12">
    <input v-model="videoUrl" type="text"  placeholder="Ex : https://www.youtube.com/watch?v=dQw4w9WgXcQ" class="input input-bordered input-primary w-1/2" />
    <select v-model="selectedType" class="select select-bordered select-primary font-bold">
      <option disabled selected>Format</option>
      <option>mp4</option>
      <option>mp3</option>
      <option>wav</option>
      <option>flac</option>
    </select>
    <button  @click="downloadVideo" class="btn btn-primary">Go!</button>
  </div>
  <div class="flex items-center justify-center mt-4">
   <p class="text-red-500">{{ errorMessage }}</p>
  </div>
  <div v-if="loading" class="flex flex-col items-center justify-center mt-4">
    <span class="loading loading-spinner loading-lg"></span>
    <h2 class="text-lg font-bold">It might take a minute 😅</h2>
  </div>
  <infoText v-if="!videoData && infoVisible" />
  <videoDownloader v-if="videoData && !loading" :data="videoData" />
</template>

<style scoped>
</style>