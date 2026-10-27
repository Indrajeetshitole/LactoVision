import {createContext,useContext,useEffect,useMemo,useState} from "react";
import {getCurrentUser,loginUser,logoutUser,registerUser} from "../services/api";
const AuthContext=createContext(null); const KEY="lactovision_access_token";
export function AuthProvider({children}){const [user,setUser]=useState(null);const [loading,setLoading]=useState(true);
useEffect(()=>{(async()=>{const t=localStorage.getItem(KEY);if(!t){setLoading(false);return}try{setUser(await getCurrentUser())}catch{localStorage.removeItem(KEY)}finally{setLoading(false)}})()},[]);
async function login(x){const d=await loginUser(x);localStorage.setItem(KEY,d.access_token);setUser(d.user)}
async function register(x){const d=await registerUser(x);localStorage.setItem(KEY,d.access_token);setUser(d.user)}
async function logout(){try{await logoutUser()}catch{}localStorage.removeItem(KEY);setUser(null)}
return <AuthContext.Provider value={useMemo(()=>({user,loading,login,register,logout}),[user,loading])}>{children}</AuthContext.Provider>}
export function useAuth(){return useContext(AuthContext)}
