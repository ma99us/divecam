<template>
  <div class="loading-comp">
    <h6 v-if="!isDone">Loading...</h6>
    <h6 v-if="isDone">Done. <a href="#" @click="scrollToTop"> - To top</a></h6>
  </div>
</template>

<script lang="ts">
export default {
  name: 'LoadingComp',
  props: {
    isDone: Boolean
  },
  methods: {
    scrollToTop() {
      window.scrollTo({top: 0, behavior: 'smooth'});
    }
  }
}
</script>

<style scoped>
.loading-comp {
  display: flex;
  vertical-align: center;
  text-align: center;
}
</style>