import { fs } from "@tauri-apps/api";
import {
  QueueQueue,
  APIBkgRmResponse,
  ResponseErrorType,
  APIBkgRmErrorResponse,
} from "../schemas/schemas.js";

export class Queue {
  private LIMIT: number;

  constructor(
    private apiKey: string,
    private queue: QueueQueue[] = [],
    private processingCount = 0,
  ) {
    this.LIMIT = import.meta.env.VITE_QUEUE_LIMIT ?? 5;
  }

  public add(path: QueueQueue) {
    this.queue.push(path);
    this.check();
  }

  private async process() {
    this.processingCount++;
    const { path, fileName, callback } = this.queue.shift()!;
    try {
      const binary = await fs.readBinaryFile(path!);
      const form = new FormData();
      form.append("files", new Blob([binary]), fileName);
      const response = await fetch(import.meta.env.VITE_REMOVE_BACKGROUND_URL, {
        headers: {
          "x-api-key": this.apiKey,
          accept: "application/json",
        },
        method: "POST",
        body: form,
      });
      const results: APIBkgRmResponse[] = await response.json();
      const result = results[0];
      let error: APIBkgRmErrorResponse | {} = {};
      if (result.error) {
        error = {
          error: result.error,
          errorType: ResponseErrorType.ProcessingFailed,
        };
      }
      callback({
        path,
        fileName,
        ...result,
        ...error,
      });
    } catch (error) {
      callback({
        path,
        fileName,
        error: `${error}`,
        errorType: ResponseErrorType.ProcessingFailed,
      });
    } finally {
      this.processingCount--;
      this.check();
    }
  }

  private check() {
    if (this.queue.length && this.processingCount < this.LIMIT) {
      this.process();
    }
  }
}
