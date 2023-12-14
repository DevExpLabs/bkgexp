import React, { createContext, useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { fetch, Body } from "@tauri-apps/api/http";
import { getStoreKey, setStoreKey, removeStoreKey } from "../utils/store.js";

export interface AuthContextType {
  apiKey: string;
  login: (api_key: string, target?: string) => Promise<boolean>;
  logout: () => void;
}

let AuthContext = createContext<AuthContextType>(null!);

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }: React.PropsWithChildren) => {
  const [apiKey, setApiKey] = useState<string>("");
  const navigate = useNavigate();

  const setInitApiKey = async () => {
    const api_key: any = await getStoreKey("api_key");
    if (api_key && api_key.value) {
      setApiKey(api_key.value);
    } else {
      setApiKey("");
    }
  };

  useEffect(() => {
    setInitApiKey();
  }, []);

  const isKeyValid = async (api_key: string) => {
    const result = await fetch(import.meta.env.VITE_AUTH_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: Body.json({
        api_key,
      }),
    });
    return result.status === 200;
  };

  const login = async (api_key: string, target = "/") => {
    // -----------------FOR LOCAL DEVELOPMENT-----------------
    // setStoreKey("api_key", api_key);
    // setApiKey(api_key);
    // return new Promise<boolean>((resolve, reject) =>
    //   setTimeout(() => {
    //     resolve(true);
    //     navigate(target);
    //   }, 100),
    // );
    // -----------------FOR LOCAL DEVELOPMENT-----------------
    const valid = await isKeyValid(api_key);
    if (!valid) {
      return false;
    }
    setStoreKey("api_key", api_key);
    setApiKey(api_key);
    navigate(target);
    return true;
  };

  const logout = async () => {
    await removeStoreKey("api_key");
    setApiKey("");
    navigate("/login");
  };

  const value = { apiKey, login, logout };
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
