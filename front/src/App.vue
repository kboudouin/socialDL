<script setup>
import navBar from './components/navBar.vue';
</script>

<template>
  <div class="h-screen flex flex-col">
    <navBar />
    <router-view class="overflow-auto" />
  </div>
</template>

<style scoped>
.h-screen {
  height: 100vh;
}

.overflow-auto {
  overflow: auto;
}
</style>