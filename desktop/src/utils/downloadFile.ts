import { fs } from "@tauri-apps/api";

export const downloadFile = (
  url: string,
  targetDir: string,
  fileName: string,
) => {
  fetch(url)
    .then((response) => response.blob())
    .then((blob) => blob.arrayBuffer())
    .then((buffer) => {
      fs.writeBinaryFile(`${targetDir}/${fileName}`, buffer);
    });
};
