import React from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "./AuthProvider.jsx";

export const Protected = ({ children }: React.PropsWithChildren) => {
  const { apiKey } = useAuth();

  if (!apiKey) {
    return <Navigate to="/login" replace />;
  }

  return children;
};
