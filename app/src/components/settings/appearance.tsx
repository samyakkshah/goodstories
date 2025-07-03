import React, { useState } from "react";
import { Skeleton } from "../ui/skeleton";
import { useTheme } from "next-themes";
import { useAuthStore } from "@/store/authStore";

import { updateProfile } from "@/lib/api";
function Appearance() {
  const { theme, setTheme } = useTheme();
  const { user, fetchProfile } = useAuthStore();

  const handleThemeChange = async (newTheme: React.SetStateAction<string>) => {
    setTheme(newTheme);
    try {
      if (!user) {
        console.error("User is not available");
        return;
      }
      await updateProfile({
        preferences: {
          ...user.preferences,
          theme: newTheme,
        },
      });
    } catch (err) {
      console.error("Failed to save theme preference", err);
    } finally {
      await fetchProfile();
    }
  };

  return (
    <div className="p-3 flex flex-col gap-3">
      <div className="font-bold ">Appearance</div>
      <div className="h-full">
        <div>Theme</div>
        <div className="mt-2 flex flex-row gap-2">
          <div className="flex flex-col gap-2">
            <div
              onClick={() => handleThemeChange("system")}
              className={`grid grid-cols-2 w-36 h-full rounded-md overflow-hidden cursor-pointer ${
                theme === "system" && "ring-2 ring-blue-500"
              }`}
            >
              <div className="relative bg-[#ddd] pt-2 overflow-hidden">
                <div className="absolute left-1/8">
                  <ThemePreviewLightSkeleton className="rounded-tl-sm" />
                </div>
              </div>
              <div className="relative overflow-hidden flex-1 bg-[#000] pr-2 pt-2">
                <div className="absolute right-1/8 ">
                  <ThemePreviewDarkSkeleton className="rounded-tr-sm" />
                </div>
              </div>
            </div>
            <div className="px-2">
              <div>System</div>
            </div>
          </div>
          <div className="flex flex-col gap-2">
            <div
              onClick={() => handleThemeChange("light")}
              className={`bg-[#ddd] px-2 pt-2 rounded-md cursor-pointer ${
                theme === "light" && "ring-2 ring-blue-500"
              }`}
            >
              <ThemePreviewLightSkeleton />
            </div>
            <div className="px-2">Light</div>
          </div>
          <div className="flex flex-col gap-2">
            <div
              onClick={() => handleThemeChange("dark")}
              className={`bg-[#000] px-2 pt-2 rounded-md cursor-pointer ${
                theme === "dark" && "ring-2 ring-blue-500"
              }`}
            >
              <ThemePreviewDarkSkeleton />
            </div>
            <div className="px-2">Dark</div>
          </div>
        </div>
      </div>
    </div>
  );
}
function ThemePreviewLightSkeleton({ className }: { className?: string }) {
  return (
    <div
      className={`w-30 h-20 ${
        className ? className : "rounded-tl-sm rounded-tr-sm"
      } overflow-hidden bg-white flex flex-row gap-0`}
    >
      <div className="w-[30%] h-full">
        <div className="w-full h-full border-r-[0.5px] border-[#D9D9D9]">
          <div className="w-full h-full rounded-none" />
        </div>
      </div>
      <div className="w-full bg-[#F9F9F9] p-2">
        <div className="w-full h-full grid grid-cols-3 gap-2 overflow-hidden">
          <Skeleton className="bg-white rounded-xs h-8" />
          <Skeleton className="bg-white rounded-xs h-8" />
          <Skeleton className="bg-white rounded-xs h-8" />
          <Skeleton className="bg-white rounded-xs h-8" />
          <Skeleton className="bg-white rounded-xs h-8" />
          <Skeleton className="bg-white rounded-xs h-8" />
          <Skeleton className="bg-white rounded-xs h-8" />
          <Skeleton className="bg-white rounded-xs h-8" />
        </div>
      </div>
    </div>
  );
}

function ThemePreviewDarkSkeleton({ className }: { className?: string }) {
  return (
    <div
      className={`w-30 h-20 ${
        className ? className : "rounded-tl-sm rounded-tr-sm"
      } overflow-hidden bg-[#222] flex flex-row gap-0`}
    >
      <div className="w-[30%] h-full">
        <div className="w-full h-full border-r-[0.5px] border-[#252525]">
          <div className="w-full h-full rounded-none" />
        </div>
      </div>
      <div className="w-full bg-[#141414] p-2">
        <div className="w-full h-full grid grid-cols-3 gap-2 overflow-hidden">
          <Skeleton className="bg-[#232323] rounded-xs h-8" />
          <Skeleton className="bg-[#232323] rounded-xs h-8" />
          <Skeleton className="bg-[#232323] rounded-xs h-8" />
          <Skeleton className="bg-[#232323] rounded-xs h-8" />
          <Skeleton className="bg-[#232323] rounded-xs h-8" />
          <Skeleton className="bg-[#232323] rounded-xs h-8" />
          <Skeleton className="bg-[#232323] rounded-xs h-8" />
          <Skeleton className="bg-[#232323] rounded-xs h-8" />
        </div>
      </div>
    </div>
  );
}

export default Appearance;
