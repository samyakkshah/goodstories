"use client";

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useModalStore } from "@/store/modalStore";
import { useAuthStore } from "@/store/authStore";
import { signin } from "@/lib/api";

export default function LoginForm() {
  const { closeModal } = useModalStore();
  const { setAuth } = useAuthStore();

  const [form, setForm] = useState({ email: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const data = await signin(form);

      setAuth(data.user, data.access_token, data.refresh_token);
      closeModal();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="p-6 min-w-md flex flex-col gap-2">
      <h2 className="text-xl font-bold">Log In</h2>
      <Input
        name="email"
        type="email"
        placeholder="Email"
        onChange={handleChange}
        required
        className="dark:bg-[#141414]"
      />
      <Input
        name="password"
        type="password"
        placeholder="Password"
        onChange={handleChange}
        required
        className="dark:bg-[#141414]"
      />

      {error && <p className="text-red-500 text-sm">{error}</p>}

      <Button type="submit" disabled={loading} className="w-full">
        {loading ? "Logging in..." : "Log In"}
      </Button>
    </form>
  );
}
