<script lang="ts">
import {ref} from 'vue'
import {RouterLink, RouterView} from 'vue-router'
import PromptModal from '@/components/PromptModal.vue'
import {mapState, mapStores} from "pinia";
import {useBackendStore} from "@/stores/backend";

export default {
  components: {
    RouterLink,
    RouterView,
    PromptModal
  },
  data() {
    return {
      modalActive: ref(false),
      pollInterval: 0
    }
  },
  computed: {
    ...mapStores(useBackendStore),
    ...mapState(useBackendStore, ['statusText', 'isBackendUp', 'isBusy']),
  },
  mounted() {
    // this.pollInterval = setInterval(async () => await this.backendStore.loadStatusText(3000), 10000);  // TEST
    this.pollInterval = setInterval(async () => await this.backendStore.loadStatusText(3000), 10000);
  },
  unmounted() {
    if (this.pollInterval) {
      clearInterval(this.pollInterval);
    }
  },
  methods: {}
}
</script>

<template>
  <header>
    <img alt="App logo" class="logo" src="@/assets/divecam-logo.png" height="42"/>
    <h6 class="title">DIVECAM</h6>
    <div class="wrapper">
      <nav>
        <RouterLink to="/">Pictures</RouterLink>
        <RouterLink to="/camera">Camera</RouterLink>
        <div class="last-right">
          <RouterLink to="/about">?</RouterLink>
        </div>
      </nav>
    </div>
  </header>
  <RouterView/>

  <div id="event-modal-outer">
    <PromptModal :modalActive="!isBackendUp" :doTimer="true">
      <div class="modal-content">
        <div>
          <h2>Waiting for device </h2>
            <img src="@/assets/divecam-squashed.png" height="60"/>
          <h2>...</h2>
        </div>
      </div>
    </PromptModal>
  </div>

</template>

<style scoped>
header {
  display: flex;
  place-items: center;
  margin-bottom: 1rem;
}

header .wrapper {
  display: flex;
  flex: 1;
  place-items: flex-start;
  flex-wrap: wrap;
}

.logo {
  margin: 0 0 0 0;
  vertical-align: top;
}

.title {
  font-family: "Trebuchet MS";
  color: #858585;
  margin-top: 0.3rem;
  margin-bottom: 0;
  font-size: x-large;
}

nav {
  display: flex;
  flex: 1;
}

nav a {
  color: var(--color-text);
  padding: 1rem 0.5rem 1rem 0.5rem;
  font-size: larger;
  font-weight: bold;
}

nav a.router-link-exact-active {
  text-decoration: none;
  color: hsla(160, 100%, 37%, 1);
  transition: 0.4s;
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  text-align: left;
  margin-left: 1rem;
}

nav a:first-of-type {
  border: 0;
}

nav .last-right {
  padding-top: 1rem;
  padding-bottom: 1rem;
  height: 100%;
  flex: 1;
  text-align: right;
}

.modal-content {
  display: flex;
  flex-direction: column;
  text-align: center;
  align-items:center;
}

.modal-content img {
  display: inline-block;
  vertical-align: middle;
}

.modal-content h2 {
  display: inline-block;
  margin-bottom: 0;
  vertical-align: middle;
}
</style>
