import axios from "axios";

// export const HOST = 'localhost';  // dev    // TEST
// export const HOST = '192.168.2.21';    // orangepi-hotspot  // TEST
// export const HOST = '192.168.2.130';   // orangepi-lan  // TEST
export const HOST = window.location.hostname; // window.location.protocol + "//" + window.location.hostname  // prod

export const BASE_URL = `http://${HOST}:8000`;    // orangepi-lan  // TEST
export const API_URL = `${BASE_URL}/api/`;

export const CAMERA_URL = `http://${HOST}:8081/?action=stream`;    // orangepi-lan  // TEST

export const api = axios.create({
  headers: {
    'Content-Type': 'application/json'
  }
});
