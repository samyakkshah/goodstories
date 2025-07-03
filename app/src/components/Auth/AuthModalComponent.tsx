"use client";

import { useState } from "react";
import LoginForm from "./LoginForm";
import SignUpForm from "./SignUpForm";
import { Button } from "@/components/ui/button";

export default function AuthModalComponent() {
  const [mode, setMode] = useState<"login" | "signup">("login");

  return (
    <div className="flex flex-col items-center min-w-48 h-[60%] space-y-4">
      {mode === "login" ? <LoginForm /> : <SignUpForm />}

      <div className="text-sm text-gray-600 p-5">
        {mode === "login" ? (
          <>
            Don&apos;t have an account?{" "}
            <Button
              variant="link"
              className="px-1 py-0 h-auto text-sblue-600 cursor-pointer"
              onClick={() => setMode("signup")}
            >
              Sign up
            </Button>
          </>
        ) : (
          <>
            Already have an account?{" "}
            <Button
              variant="link"
              className="px-1 py-0 h-auto text-blue-600 cursor-pointer"
              onClick={() => setMode("login")}
            >
              Log in
            </Button>
          </>
        )}
      </div>
    </div>
  );
}
