import React from "react";
import { Main } from "./routes/Main.jsx";
import { Login } from "./routes/Login.jsx";
import { Routes, Route } from "react-router-dom";
import { Protected } from "./auth/Protected.jsx";
import { AuthProvider } from "./auth/AuthProvider.jsx";
import { Login as LoginProtect } from "./auth/Login.jsx";

function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route
          index
          element={
            <Protected>
              <Main />
            </Protected>
          }
        />
        <Route
          path="login"
          element={
            <LoginProtect>
              <Login />
            </LoginProtect>
          }
        />
      </Routes>
    </AuthProvider>
  );
}

export default App;
