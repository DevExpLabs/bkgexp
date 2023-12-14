import React, { useEffect, useMemo, useRef, useState } from "react";
import { fs } from "@tauri-apps/api";
import { Queue } from "../queue/queue.js";
import { open } from "@tauri-apps/api/dialog";
import { homeDir } from "@tauri-apps/api/path";
import { useAuth } from "../auth/AuthProvider.jsx";
import { UnlistenFn } from "@tauri-apps/api/event.js";
import { Stats } from "../components/stats/Stats.jsx";
import { QueueCB, File, ResponseErrorType } from "../schemas/schemas.js";
import { downloadFile } from "../utils/downloadFile.js";
import { SUPPORTED_EXTENSIONS } from "../constants/constants.js";
import { DebouncedEvent, watch } from "tauri-plugin-fs-watch-api";
import { type } from "@tauri-apps/api/os";

export const Main = () => {
  const { logout, apiKey } = useAuth();
  const [queue] = useState(() => new Queue(apiKey));
  const [sourceDir, setSourceDir] = useState<string | null>();
  const [targetDir, setTargetDir] = useState<string | null>();
  const [running, setRunning] = useState(false);
  const [processingFiles, setProcessingFiles] = useState<string[]>([]);
  const [results, setResults] = useState<QueueCB[]>([]);
  const watchDirRef = useRef<Promise<UnlistenFn> | null>(null);
  const watchModeRef = useRef<HTMLInputElement>(null);

  const failed = useMemo(() => {
    return results.filter(
      (res) =>
        res.error &&
        res.errorType !== ResponseErrorType.UnsupportedFileExtension,
    );
  }, [results]);

  // handle START/STOP
  useEffect(() => {
    // START
    if (running && sourceDir && targetDir) {
      if (!watchModeRef.current?.checked) {
        processDir();
      }
      startWatchMode();
      // STOP
    } else {
      if (watchDirRef.current) {
        watchDirRef.current.then((stop) => stop());
      }
    }
    return () => {
      watchDirRef.current &&
        watchDirRef.current.then((stop) => {
          stop();
        });
    };
  }, [running]);

  const removeProcessingFile = (fileName: QueueCB["fileName"]) => {
    setProcessingFiles((prevState) => {
      const newArr = [...prevState];
      const index = newArr.indexOf(fileName);
      if (index !== -1) {
        newArr.splice(index, 1);
      }
      return newArr;
    });
  };

  const addProcessingFile = (fileName: QueueCB["fileName"]) => {
    setProcessingFiles((prevState) => [...prevState, fileName]);
  };

  const addToResults = (result: QueueCB) => {
    setResults((prevState) => {
      const newArr = [...prevState];
      const index = newArr.findIndex((el) => el.path === result.path);
      if (index !== -1) {
        newArr[index] = result;
      } else {
        newArr.push(result);
      }
      return newArr;
    });
  };

  const addUnsupportedExtension = (file: File, extension: string) => {
    addToResults({
      ...file,
      error: `Unsupported file extension: ${extension}`,
      errorType: ResponseErrorType.UnsupportedFileExtension,
    });
  };

  const addToQueue = (file: File) => {
    queue.add({
      ...file,
      callback: (result) => {
        removeProcessingFile(result.fileName);
        addToResults(result);
        if (result.output) {
          downloadFile(result.output.imageUrl, targetDir!, result.fileName);
        }
      },
    });
  };

  const process = (file: File) => {
    addProcessingFile(file.fileName);
    addToQueue(file);
  };

  const processDir = async () => {
    const targetFiles = await fs.readDir(targetDir!);
    const targetFileNames = new Set(
      targetFiles.map((file) => file.name).filter((fileName) => fileName),
    );
    fs.readDir(sourceDir!).then((files) => {
      files
        .filter((file) => file.name && !targetFileNames.has(file.name))
        .forEach((file) => {
          const fileName = file.name!;
          const extension = fileName.split(".").at(-1)!;
          if (SUPPORTED_EXTENSIONS.includes(extension)) {
            process({
              fileName,
              path: file.path,
            });
          } else {
            addUnsupportedExtension(
              {
                fileName,
                path: file.path,
              },
              extension,
            );
          }
        });
    });
  };

  const startWatchMode = () => {
    watchDirRef.current = watch(sourceDir!, async (e: DebouncedEvent) => {
      const osType = await type();
      const slash = osType === "Windows_NT" ? "\\" : "/";
      const filtered: File[] = [];
      for (const event of e as unknown as DebouncedEvent[]) {
        const fileName = event.path.split(slash).at(-1)!;
        const extension = fileName.split(".").at(-1)!;
        if (!SUPPORTED_EXTENSIONS.includes(extension)) {
          addUnsupportedExtension(
            {
              fileName,
              path: event.path,
            },
            extension,
          );
          continue;
        }
        const isAnyKind = event.kind.toLowerCase() === "any";
        try {
          const fileExists = await fs.exists(event.path);
          if (isAnyKind && fileExists) {
            filtered.push({ fileName, path: event.path });
          }
        } catch (e) {
          continue;
        }
      }

      filtered.forEach((f) => process(f));
    });
  };

  const getSelectedDir = async () => {
    const selected = await open({
      directory: true,
      multiple: false,
      defaultPath: await homeDir(),
    });
    if (!Array.isArray(selected)) {
      return selected;
    }
    return null;
  };

  const sourceDirHandler = () => {
    setRunning(false);
    getSelectedDir().then((dir) => {
      setSourceDir(dir);
    });
  };

  const targetDirHandler = () => {
    setRunning(false);
    getSelectedDir().then((dir) => setTargetDir(dir));
  };

  const handleRerunFailed = () => {
    for (const f of failed) {
      if (f.errorType === ResponseErrorType.UnsupportedFileExtension) {
        continue;
      }
      process(f);
    }
  };

  return (
    <>
      <section className="grid grid-cols-12 justify-items-stretch gap-4 p-8">
        <div className="col-span-12 text-center">
          <h1 className="text-3xl font-bold">AiShoot</h1>
        </div>
        <div className="col-span-2 col-end-13">
          <button className="btn btn-outline" onClick={logout}>
            Log out
          </button>
        </div>
        {/* DIR BUTTONS */}
        <div className="dirs-container col-span-full flex flex-col gap-4">
          {/* SOURCE DIR BUTTON */}
          <div className="flex flex-row items-center justify-start gap-4">
            <button className="btn btn-secondary" onClick={sourceDirHandler}>
              Source
            </button>
            <span>Source: {sourceDir ?? "Not selected"}</span>
          </div>
          {/* TARGET DIR BUTTON */}
          <div className="flex flex-row items-center justify-start gap-4">
            <button className="btn btn-secondary" onClick={targetDirHandler}>
              Target
            </button>
            <span>Source: {targetDir ?? "Not selected"}</span>
          </div>
        </div>
        <div className="start-container col-span-full justify-self-center">
          {/* START/STOP BUTTON */}
          <button
            className={`btn btn-lg w-full ${
              running ? "btn-error" : "btn-success"
            }`}
            onClick={() => setRunning(!running)}
          >
            {running ? "Stop" : "Start"}
          </button>
          <button
            className={`btn ${
              !failed.length && "btn-disabled"
            } btn-secondary btn-outline btn-md mt-2 w-full`}
            onClick={handleRerunFailed}
          >
            Rerun failed ({failed.length})
          </button>
          {/* WATCH MODE CHECKBOX */}
          <div className="form-control">
            <label className="label cursor-pointer gap-4">
              <span className="label-text">Watch mode only</span>
              <input
                type="checkbox"
                className="checkbox-info checkbox"
                ref={watchModeRef}
                onChange={() => setRunning(false)}
              />
            </label>
          </div>
        </div>
        {/* PROCESSING FILES */}
        <div className="progress-container col-span-full text-end">
          <h4 className="text-l font-bold underline">
            Currently processing files:
          </h4>
          <p>{processingFiles.length ? processingFiles.join(", ") : "None"}</p>
        </div>
      </section>
      <div className="divider"></div>
      {/* STATISTICS TABLE */}
      <section>
        <Stats rows={results} />
      </section>
    </>
  );
};
