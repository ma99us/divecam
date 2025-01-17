<script lang="ts">
import {useBackendStore} from "@/stores/backend";
import {mapState, mapStores} from "pinia";
import type {PinAction, RebootAction, TimeAction} from "@/model/dtos";
import {CAMERA_URL} from "@/stores/api";

export default {
  data() {
    return {
      rotatePin: 3,  // TODO: should not be hardcoded. It should be retrieved from BE config
      lightPin: 6,  // TODO: should not be hardcoded. It should be retrieved from BE config
      sleepMinutes: 1,  // TODO: should not be hardcoded or come from local storage. It should be retrieved from BE config
      isCamLoaded: false,
      camRetry: 0,
      pollInterval: 0
    }
  },
  components: {},
  computed: {
    ...mapStores(useBackendStore),
    ...mapState(useBackendStore, ['statusText', 'isBusy']),
    streamHref() {
      return CAMERA_URL + "&r=" + this.camRetry;
    }
  },
  async mounted() {
    this.sleepMinutes = Number(localStorage.getItem('sleepMinutes')) || 1;
    await this.backendStore.startCamera();  // FIXME: this will mess up multiple users watching the stream
    this.pollInterval = setInterval(async () => !this.isCamLoaded ? this.camRetry++ : this.camRetry = 0, 1000);
  },
  async unmounted() {
    await this.backendStore.stopCamera();  // FIXME: this will mess up multiple users watching the stream
    if (this.pollInterval) {
      clearInterval(this.pollInterval);
    }
  },
  methods: {
    onSleepMinutesChange(){
      localStorage.setItem('sleepMinutes', String(this.sleepMinutes));
    },
    onPinWrite(wPi: number, isHigh: boolean) {
      const action = {wPi, isHigh} as PinAction;
      this.backendStore.pinWrite(action);
    },
    onPinBlink(wPi: number, durationMs: number = 100) {
      const action = {wPi, durationMs} as PinAction;
      this.backendStore.pinBlink(action);
    },
    onStep(wPi: number, forward:boolean = true) {
      const action = {wPi, forward, durationMs: 1000} as PinAction;
      this.backendStore.pinStep(action);
    },
    onSleepMinutes(minutes: number) {
      const action = {minutes} as TimeAction;
      this.backendStore.goToSleep(action);
    },
    onReboot(mode: string) {
      const action = {mode} as RebootAction;
      this.backendStore.reboot(action);
    },
    onCamLoaded() {
      this.isCamLoaded = true;
    },
    errorHandler(event: Event) {
      this.isCamLoaded = false;
      const imgEl: any = event.target;
      console.log('error loading', imgEl.src);
      // imgEl.src = require("@/assets/camera-empty.png");
    },
    async onTakePicture() {
      let wasCamLoaded = this.isCamLoaded;
      if (this.isCamLoaded) {
        await this.backendStore.stopCamera();
      }

      await this.backendStore.takePicture();

      if (wasCamLoaded) {
        await this.backendStore.startCamera();
      }
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
      <div class="col pull-right"></div>
    </div>
    <div class="toolbar row">
      <div class="col-8">
        <!--      Pin wPi: {{ rotatePin }}: &nbsp;-->
        <button @click="onPinBlink(rotatePin)">Rotate</button>
        <button @click="onPinBlink(rotatePin, 1400)">Stop</button>&nbsp;
        <br>
        <button @click="onStep(rotatePin, true)">Next Step</button>
        <button @click="onStep(rotatePin, false)">Reverse Step</button>
        <br>
        <button @click="onPinWrite(lightPin, true)">Light On</button>
        <button @click="onPinWrite(lightPin, false)">Light Off</button>&nbsp;
        <br>
        <snap>
          <button @click="onSleepMinutes(sleepMinutes)">Set sleep</button> for <input type="number" style="width:3rem" size="3" maxlength = "3" min="1" max="60" v-model="sleepMinutes"  v-on:change="onSleepMinutesChange"/> minutes
        </snap>
        <br>
      </div>
      <div class="col-4 pull-right">
        <button @click="onReboot('normal')">Reboot to Dev</button><br>
        <button @click="onReboot('hotspot')">Reboot to HotSpot</button><br>
        <button @click="onReboot('wake')">Reboot to Camera cycle</button><br>
      </div>
      <div style="text-align: center; max-width: 800px;">
        <button @click="onTakePicture()">Take a Picture</button>&nbsp;
      </div>
    </div>
    <div>
<!--      <h4>Camera MJPEG stream:</h4>-->
      <img alt="camera" class="stream-view img-flipped" :src="streamHref" @load="onCamLoaded" @error="errorHandler" v-show="isCamLoaded"/>
      <img alt="no camera" class="stream-view" src="@/assets/camera-empty.png" v-show="!isCamLoaded"/>
    </div>
  </main>
</template>

<style>
.bad-status {
  color: coral;
  font-size: small;
}

.toolbar {
  margin-bottom: 1rem;
  display: flex;
  max-width: 800px;
}

.stream-view {
  width: 100%;
  max-width: 800px;
  background-color: #f2f2f2;
  border: 2px solid #2c3e50;
}

.img-flipped {
  transform: scaleY(-1) scaleX(-1);
}

.pull-right {
  flex: 1 0;
  text-align: right;
}

button {
  margin: 3px;
}
</style>
