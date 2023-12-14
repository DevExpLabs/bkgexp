import React from "react";
import { QueueCB } from "../../schemas/schemas.js";

export const Stats = ({ rows }: { rows: QueueCB[] }) => {
  return (
    <div className="max-h-96 overflow-x-auto">
      <h1 className="my-4 text-center text-xl font-bold">Statistics</h1>
      <table className="table table-pin-rows table-pin-cols table-xs">
        <thead>
          <tr>
            <th></th>
            <td>File Name</td>
            <td>Status</td>
            <td>Error</td>
            <td>ORT Session Time [s]</td>
            <td>Matting Time [s]</td>
            <td>Image Download Time [s]</td>
            <td>Overall Operation Time [s]</td>
          </tr>
        </thead>
        <tbody>
          {rows &&
            rows.map((row, index) => (
              <tr key={`${row.fileName}_${index}`}>
                <th>{index + 1}</th>
                <th>{row.fileName}</th>
                <td>
                  {row.error ? (
                    <span className="text-red-600">{"Fail"}</span>
                  ) : (
                    <span className="text-green-600">{"Success"}</span>
                  )}
                </td>
                <td>{row.error ?? ""}</td>
                <td>
                  {row.output?.timings
                    ? row.output.timings.ort_session_time.toFixed(2)
                    : ""}
                </td>
                <td>
                  {row.output?.timings
                    ? row.output.timings.matting_time.toFixed(2)
                    : ""}
                </td>
                <td>
                  {row.output?.timings
                    ? row.output.timings.image_download_time.toFixed(2)
                    : ""}
                </td>
                <td>
                  {row.output?.timings
                    ? row.output.timings.main_operation_time.toFixed(2)
                    : ""}
                </td>
              </tr>
            ))}
        </tbody>
        <tfoot>
          <tr>
            <th></th>
            <td>File Name</td>
            <td>Status</td>
            <td>Error</td>
            <td>ORT Session Time [s]</td>
            <td>Matting Time [s]</td>
            <td>Image Download Time [s]</td>
            <td>Overall Operation Time [s]</td>
          </tr>
        </tfoot>
      </table>
    </div>
  );
};
