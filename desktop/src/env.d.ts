/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_BASE_URL: string;
  readonly VITE_API_URL: string;
  readonly VITE_REMOVE_BACKGROUND_URL: string;
  readonly VITE_AUTH_URL: string;
  readonly VITE_QUEUE_LIMIT?: number;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
