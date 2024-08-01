<script lang="ts">
import {useBackendStore} from "@/stores/backend";
import {mapState, mapStores} from "pinia";
import ImageViewer from '@/components/imageViewer'
import {BASE_URL} from "@/stores/api";
import type {FindPicturesAction} from "@/model/dtos";
import LoadingComp from "@/components/LoadingComp.vue";

export default {
  data() {
    return {
      viewer: null as unknown as ImageViewer | null,
      pictures: [] as string[],
      picsLoaded: false,
      page: 0,
      limit: 20,
      isDone: false,
      isLoading: false,
      totalFiles: 0,
      totalSize: 0
    }
  },
  components: {
    LoadingComp
  },
  computed: {
    ...mapStores(useBackendStore),
    ...mapState(useBackendStore, ['statusText', 'isBusy']),
  },
  created() {
  },
  async mounted() {
    window.addEventListener("scroll", this.handleScroll);

    await this.loadPictures();

    this.handleScroll(null);
  },
  async unmounted() {
    window.removeEventListener("scroll", this.handleScroll)

    this.destroyPictureViewer();
  },
  methods: {
    async loadPictures() {
      try {
        const action = {
          offset: this.page * this.limit,
          limit: this.limit
        } as FindPicturesAction;
        this.isLoading = true;
        this.destroyPictureViewer();
        let pics = await this.backendStore.findPictures(action) ?? [];
        pics = pics.map((p: string) => (BASE_URL.length > 0 ? BASE_URL + '/' : '') + p);
        this.pictures.push(...pics);
        this.isDone = !pics.length;
        this.picsLoaded = !!pics.length;

        if (this.page == 0) {
          const res = await this.backendStore.picturesInfo() ?? {};
          this.totalFiles = res['files'] ?? 0
          this.totalSize = res['size'] ?? 0
        }

        return pics.length;
      } catch (error) {
        this.isDone = true;
      } finally {
        this.isLoading = false;
        this.initPictureViewer();
      }
    },

    async loadMorePictures() {
      this.page++;
      const loaded = await this.loadPictures();
      if (!loaded) {
        this.page--; // do not advance page if nothing loads
      }
      return loaded;
    },

    showPictureViewer(selectedPicture: number = 0) {
      if (!this.viewer) {
        return
      }

      this.viewer.selectImage(selectedPicture, true);

      if (!this.viewer.visible) {
        this.viewer.show();
      }
    },

    initPictureViewer() {
      this.destroyPictureViewer();

      this.viewer = new ImageViewer({
        // parentId: 'pictures',
        images: this.pictures.map(p => {
          return {'mainUrl': p}
        })
      });
    },

    destroyPictureViewer() {
      if (this.viewer) {
        this.viewer.destroy();
        this.viewer = null;
      }
    },

    async handleScroll(e: any) {
      const element = this.$refs.scrollComponent as HTMLElement;
      while (element.getBoundingClientRect().bottom < window.innerHeight && !this.isLoading && !this.isDone) {
        await this.loadMorePictures();
      }
    },

    formatBytes(bytes: number, decimals = 2) {
      if (!+bytes) return '0 Bytes'

      const k = 1024
      const dm = decimals < 0 ? 0 : decimals
      const sizes = ['Bytes', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']

      const i = Math.floor(Math.log(bytes) / Math.log(k))

      return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`
    }
  }
}

</script>

<template>
  <main>
    <div class="row">
      <div class="col-auto">
        <h3 class="bad-status" v-if="backendStore.isBadStatus">Device Status: {{ statusText }}</h3>
      </div>
      <div class="col pull-right" v-if="totalFiles">{{ formatBytes(totalSize) }} in {{ totalFiles }} files</div>
    </div>
    <div id="pictures" class="image-container" ref="scrollComponent">
      <img v-for="(image, index) in pictures"
           :key="index" :src="image" :alt="`Picture #${index+1}`"
           @click="showPictureViewer(index)">
    </div>
    <div class="pull-right" v-if="totalFiles">{{ formatBytes(totalSize) }} in {{ totalFiles }} files</div>
    <LoadingComp v-if="isLoading || isDone" :isDone="isDone"/>
  </main>
</template>

<style>
.bad-status {
  color: coral;
  font-size: small;
}

code {
  white-space: pre-wrap;
}

#pictures {
  background-color: lightgray;
}

.image-container {
  display: flex;
  flex-wrap: wrap;
}

.image-container img {
  width: 200px;
  height: 150px;
  margin: 10px;
  cursor: pointer;
  border: 1px solid black;
  background-image: url("@/assets/camera-empty.png");
  background-size: 200px
}

.pull-right {
  text-align: right;
}
</style>
