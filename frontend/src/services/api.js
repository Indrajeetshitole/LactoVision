import axios from "axios";
const api=axios.create({baseURL:import.meta.env.VITE_API_URL||"http://localhost:8000/api",timeout:7000,headers:{"Content-Type":"application/json"}});
api.interceptors.request.use(c=>{const t=localStorage.getItem("lactovision_access_token");if(t)c.headers.Authorization=`Bearer ${t}`;return c});
export const getApiHealth=async()=> (await api.get("/health")).data; export const getDatabaseHealth=async()=> (await api.get("/database/health")).data;
export const registerUser=async p=>(await api.post("/auth/register",p)).data; export const loginUser=async p=>(await api.post("/auth/login",p)).data; export const getCurrentUser=async()=>(await api.get("/auth/me")).data; export const logoutUser=async()=>(await api.post("/auth/logout")).data;
export const getFarms=async()=>(await api.get("/farms")).data; export const createFarm=async p=>(await api.post("/farms",p)).data; export const updateFarm=async(id,p)=>(await api.put(`/farms/${id}`,p)).data;
export const getCows=async params=>(await api.get("/cows",{params})).data; export const createCow=async p=>(await api.post("/cows",p)).data; export const updateCow=async(id,p)=>(await api.put(`/cows/${id}`,p)).data; export const deleteCow=async id=>(await api.delete(`/cows/${id}`)).data;
export const createTestRecord=async message=>(await api.post("/system/test-record",{message})).data; export const getTestRecords=async()=>(await api.get("/system/test-records")).data; export default api;

export async function createMilk(payload) {
  const response = await api.post("/milk", payload);
  return response.data;
}
export async function getMilk(cowId) {
  const response = await api.get(cowId ? `/milk/${cowId}` : "/milk");
  return response.data;
}
export async function createFeed(payload) {
  const response = await api.post("/feed", payload);
  return response.data;
}
export async function getFeed(cowId) {
  const response = await api.get(cowId ? `/feed/${cowId}` : "/feed");
  return response.data;
}
export async function createHealth(payload) {
  const response = await api.post("/health", payload);
  return response.data;
}
export async function getHealth(cowId) {
  const response = await api.get(`/health/${cowId}`);
  return response.data;
}
export async function createEnvironment(payload) {
  const response = await api.post("/environment", payload);
  return response.data;
}
export async function getEnvironment() {
  const response = await api.get("/environment");
  return response.data;
}
