import React, { useState } from "react";
import { useAuth } from "../auth/AuthProvider.jsx";

export const Login = () => {
  const { login } = useAuth();
  const [apiKey, setApiKey] = useState("");
  const [error, setError] = useState<string | null>(null);

  const handleLogin = async () => {
    setError(null);
    if (!(await login(apiKey))) {
      setError("Wrong key");
    }
  };

  return (
    <div className="flex h-screen items-center justify-center">
      <div className="card w-96 bg-base-100 shadow-xl">
        <div className="card-body gap-10">
          <h2 className="card-title justify-center">Login</h2>
          <div className="form-control w-full max-w-xs">
            <input
              type="text"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="Your API key"
              className={`input input-bordered input-primary w-full max-w-xs ${
                error && "input-error"
              }`}
            />
            {error && (
              <label className="label">
                <span className="label-text-alt">{error}</span>
              </label>
            )}
          </div>
          <div className="card-actions justify-center">
            <button className="btn btn-primary w-full" onClick={handleLogin}>
              Login
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
