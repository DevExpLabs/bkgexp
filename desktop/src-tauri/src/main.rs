// Copyright 2019-2021 Tauri Programme within The Commons Conservancy
// SPDX-License-Identifier: Apache-2.0
// SPDX-License-Identifier: MIT

#![cfg_attr(
  all(not(debug_assertions), target_os = "windows"),
  windows_subsystem = "windows"
)]

use tauri::{
  api::dialog::ask, RunEvent, WindowEvent, Manager
};

fn main() {

  #[allow(unused_mut)]
  let mut app = tauri::Builder::default()
    .plugin(tauri_plugin_fs_watch::init())
    .plugin(tauri_plugin_store::Builder::default().build())
    .build(tauri::generate_context!())
    .expect("error while building tauri application");

  #[cfg(target_os = "macos")]
  app.set_activation_policy(tauri::ActivationPolicy::Regular);

  app.run(|app_handle, e| match e {
    // Triggered when a window is trying to close
    RunEvent::WindowEvent {
      label,
      event: WindowEvent::CloseRequested { api, ..},
      ..
    } => {
      let app_handle = app_handle.clone();
      let window = app_handle.get_window(&label).unwrap();
      // use the exposed close api, and prevent the event loop to close
      api.prevent_close();
      // ask the user if he wants to quit
      ask(
        Some(&window),
        "Tauri API",
        "Are you sure that you want to close this window?",
        move |answer| {
          if answer {
            // .close() cannot be called on the main thread
            std::thread::spawn(move || {
              app_handle.get_window(&label).unwrap().close().unwrap();
            });
          }
        },
      );
    }
    _ => {}
  })
}
