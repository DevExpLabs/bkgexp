export interface File {
  path: string;
  fileName: string;
}
interface APITimings {
  ort_session_time: number;
  matting_time: number;
  main_operation_time: number;
  image_download_time: number;
}
interface APIOutput {
  imageUrl: string;
  timings: APITimings;
}

export enum ResponseErrorType {
  ProcessingFailed,
  UnsupportedFileExtension,
}

export interface APIBkgRmErrorResponse {
  error?: string;
  errorType?: ResponseErrorType;
}

export interface APIBkgRmResponse extends APIBkgRmErrorResponse {
  output?: APIOutput;
}

export interface QueueCB extends File, APIBkgRmResponse {}

export interface QueueQueue extends File {
  callback: (result: QueueCB) => void;
}
