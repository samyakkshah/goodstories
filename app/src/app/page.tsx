"use client";
import { useAuthStore } from "@/store/authStore";
import { useLikesStore } from "@/store/likeStore";
import TopStories from "@/views/TopStories";
import { useTheme } from "next-themes";
import { useEffect } from "react";

export default function HomePage() {
  const { fetchProfile } = useAuthStore();
  const { user } = useAuthStore();
  const { theme, setTheme } = useTheme();

  useEffect(() => {
    fetchProfile();
  }, []);

  useEffect(() => {
    if (user?.preferences?.theme && user?.preferences?.theme !== theme) {
      setTheme(user.preferences.theme);
    }
  }, [user]);

  useEffect(() => {
    if (user) {
      useLikesStore.getState().loadUserLikes();
    }
  }, [user]);

  return (
    <main className="">
      <div className="flex flex-row gap-2 p-5 justify-center">
        <section className="w-full max-w-7xl">
          <TopStories />
        </section>
      </div>
    </main>
  );
}
