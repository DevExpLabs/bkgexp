import { Store } from "tauri-plugin-store-api";
const STORE_PATH = ".settings.dat";

const getStore = () => new Store(STORE_PATH);

export const getStoreKey = async (key: string) => {
  const store = getStore();
  return await store.get(key);
};

export const setStoreKey = async (key: string, value: string) => {
  const store = getStore();
  await store.set(key, { value });
  await store.save();
};

export const removeStoreKey = async (key: string) => {
  const store = getStore();
  await store.delete(key);
  await store.save();
};
