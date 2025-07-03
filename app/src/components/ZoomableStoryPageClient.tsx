"use client";

import React, { useState, useEffect } from "react";
import Page from "@/components/Page";
import { useAuthStore } from "@/store/authStore";
import { updateProfile } from "@/lib/api";
import debounce from "lodash.debounce";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";

type ZoomableStoryPageClientProps = {
  story: any;
};

export default function ZoomableStoryPageClient({
  story,
}: ZoomableStoryPageClientProps) {
  const { user, fetchProfile } = useAuthStore();
  const [zoom, setZoom] = useState(user?.preferences.zoom || 1);
  const increaseZoom = () => {
    const newZoom = Math.min(zoom + 0.1, 2);
    handleZoomChange(newZoom);
  };

  const decreaseZoom = () => {
    const newZoom = Math.max(zoom - 0.1, 0.5);
    handleZoomChange(newZoom);
  };
  useEffect(() => {
    if (user?.preferences?.zoom) {
      setZoom(user.preferences.zoom);
    }
  }, [user]);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && (e.key === "+" || e.key === "=")) {
        e.preventDefault();
        increaseZoom();
      } else if ((e.ctrlKey || e.metaKey) && e.key === "-") {
        e.preventDefault();
        decreaseZoom();
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  const saveZoomPreference = debounce(async (newZoom: number) => {
    if (!user) {
      console.error("User is not available");
      return;
    }

    try {
      await updateProfile({
        preferences: {
          ...user.preferences,
          zoom: newZoom,
        },
      });
    } catch (err) {
      console.error("Failed to save zoom preference", err);
    }
  }, 300); // 300ms delay

  const handleZoomChange = async (newZoom: number) => {
    setZoom(newZoom);
    saveZoomPreference(newZoom);
  };

  return (
    <main className="px-4 py-6">
      <div className="flex justify-between items-center mb-4 max-w-3xl mx-auto">
        <div>
          <div className="prose prose-invert text-3xl font-bold">
            <Markdown remarkPlugins={[remarkGfm]}>
              {story.metadata.title}
            </Markdown>
          </div>
          <div className="text-muted-foreground text-sm mb-4 max-w-3xl mx-auto">
            {story.metadata.genre} · {story.metadata.tone}
          </div>
        </div>
        <div className="flex items-center space-x-2 text-xs">
          <button
            onClick={decreaseZoom}
            className="px-2 py-1 border rounded hover:bg-gray-100 dark:hover:bg-[#222] cursor-pointer"
          >
            -
          </button>
          <span>{Math.round(zoom * 100)}%</span>
          <button
            onClick={increaseZoom}
            className="px-2 py-1 border rounded hover:bg-gray-100 dark:hover:bg-[#222] cursor-pointer"
          >
            +
          </button>
        </div>
      </div>
      <div className="flex flex-col gap-4">
        <div className="max-w-3xl mx-auto" style={{ zoom: zoom }}>
          {story.metadata.cover_image_url && (
            <img src={story.metadata.cover_image_url} />
          )}
        </div>
        <div className="max-w-3xl mx-auto" style={{ zoom: zoom }}>
          {story.pages
            .sort((a: any, b: any) => a.page_number - b.page_number)
            .map((page: any, idx: number) => (
              <Page
                key={idx}
                pageNumber={page.page_number}
                content={page.content}
              />
            ))}
        </div>
      </div>
    </main>
  );
}
