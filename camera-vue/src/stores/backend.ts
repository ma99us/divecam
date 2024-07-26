import {defineStore} from 'pinia'
import {api, API_URL} from "@/stores/api";
import type {GpioPin, PinAction, TimeAction} from "@/model/dtos";
import {FindPicturesAction, RebootAction} from "@/model/dtos";

export const useBackendStore = defineStore('backend', {
  state: () => {
    return {
      isBusy: false,
      statusText: '',
      isBackendUp: true,
      gpioAll: '',
      pins: [] as GpioPin[]
    }
  },
  getters: {
    isBadStatus: (state) => state.statusText != '' && state.statusText != 'Ready.' && state.statusText != 'Ok.',
  },
  actions: {
    async getString(prompt: String, timeout: number = 0): Promise<string> {
      try {
        this.isBusy = true;
        const response = await api.get<string>(API_URL + prompt, {timeout});
        return response.data ?? '';
      } catch (error) {
        console.error(error)
        return 'ERROR: ' + error;
      } finally {
        this.isBusy = false;
      }
    },

    async loadStatusText(timeout: number = 0) {
      this.statusText = await this.getString('status', timeout);
      this.isBackendUp = this.statusText && !this.statusText.startsWith("ERROR: ")
      return this.isBackendUp;
    },

    async postAction(path:string, action: any | null = null) {
      try {
        this.isBusy = true;
        const response = await api.post(API_URL + path, action);
        if (action?.refresh) {
          await this.loadStatusText();
        }
        return response.data;
      } catch (error) {
        console.error(error)
        throw error;
      } finally {
        this.isBusy = false;
      }
    },

    async pinRead(action: PinAction) {
      return await this.postAction('pin-read', action);
    },

    async pinWrite(action: PinAction) {
      return await this.postAction('pin-write', action);
    },

    async pinMode(action: PinAction) {
      return await this.postAction('pin-mode', action);
    },

    async pinBlink(action: PinAction) {
      return await this.postAction('pin-blink', action);
    },

    async pinStep(action: PinAction) {
      return await this.postAction('pin-step', action);
    },

    async startCamera() {
      return await this.postAction('start-camera-stream');
    },

    async stopCamera() {
      return await this.postAction('stop-camera-stream');
    },

    async goToSleep(action: TimeAction) {
      return await this.postAction('go-to-sleep', action);
    },

    async reboot(action: RebootAction) {
      return await this.postAction('reboot', action);
    },

    async findPictures(action: FindPicturesAction){
      return await this.postAction('find-pictures', action);
    },

    async picturesInfo(){
      return await this.postAction('pictures-info');
    }
  }
})
