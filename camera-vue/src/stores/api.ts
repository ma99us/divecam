import axios from "axios";

export const BASE_URL = 'http://localhost:8000'  // dev    // TEST
// export const BASE_URL = 'http://192.168.2.21:8000'    // orangepi  // TEST
// export const BASE_URL = ''  // prod
export const API_URL = `${BASE_URL}/api/`;

export const api = axios.create({
  headers: {
    'Content-Type': 'application/json'
  }
});
