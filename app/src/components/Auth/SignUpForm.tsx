"use client";

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useModalStore } from "@/store/modalStore";
import { useAuthStore } from "@/store/authStore";
import { Mail, User, Lock, Eye, EyeOff } from "lucide-react";
import { signup } from "@/lib/api";

export default function SignUpForm() {
  const { closeModal } = useModalStore();
  const { setAuth } = useAuthStore();

  const [form, setForm] = useState({
    email: "",
    password: "",
    confirmPassword: "",
    username: "",
    name: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const togglePasswordVisibility = () => {
    setShowPassword((prev) => !prev);
  };

  const toggleConfirmPasswordVisibility = () => {
    setShowConfirmPassword((prev) => !prev);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (form.password !== form.confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    setLoading(true);

    try {
      const data = await signup({
        email: form.email,
        password: form.password,
        username: form.username,
        name: form.name,
      });

      setAuth(data.user, data.access_token, data.refresh_token);
      closeModal();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col md:flex-row max-w-3xl bg-white dark:bg-[#141414] overflow-hidden p-5">
      {/* Left Side - Illustration */}
      <div className="relative md:w-1/2 overflow-hidden rounded-lg md:h-auto bg-gray-50">
        <img
          src="https://images.unsplash.com/photo-1584448062058-0d13ba997eb0?q=80&w=1055&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
          alt="Sign Up Illustration"
          className="h-full object-cover"
        />
      </div>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4 w-md p-12">
        <h2 className="text-2xl font-bold text-center">Sign Up</h2>

        <div className="relative">
          <Mail
            className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
            size={16}
          />
          <Input
            name="email"
            type="email"
            placeholder="Email"
            value={form.email}
            onChange={handleChange}
            required
            className="pl-10"
          />
        </div>

        <div className="relative">
          <User
            className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
            size={16}
          />
          <Input
            name="username"
            placeholder="Username"
            value={form.username}
            onChange={handleChange}
            required
            className="pl-10"
          />
        </div>

        <div className="relative">
          <User
            className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
            size={16}
          />
          <Input
            name="name"
            placeholder="Full Name (optional)"
            value={form.name}
            onChange={handleChange}
            className="pl-10"
          />
        </div>

        <div className="relative">
          <Lock
            className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
            size={16}
          />
          <Input
            name="password"
            type={showPassword ? "text" : "password"}
            placeholder="Password"
            value={form.password}
            onChange={handleChange}
            required
            className="pl-10 pr-10"
          />
          <button
            type="button"
            onClick={togglePasswordVisibility}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 cursor-pointer"
          >
            {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
          </button>
        </div>

        <div className="relative">
          <Lock
            className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
            size={16}
          />
          <Input
            name="confirmPassword"
            type={showConfirmPassword ? "text" : "password"}
            placeholder="Confirm Password"
            value={form.confirmPassword}
            onChange={handleChange}
            required
            className="pl-10 pr-10"
          />
          <button
            type="button"
            onClick={toggleConfirmPasswordVisibility}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 cursor-pointer"
          >
            {showConfirmPassword ? <EyeOff size={16} /> : <Eye size={16} />}
          </button>
        </div>

        {error && <p className="text-red-500 text-sm">{error}</p>}

        <Button type="submit" disabled={loading} className="w-full">
          {loading ? "Signing up..." : "Sign Up"}
        </Button>
      </form>
    </div>
  );
}
