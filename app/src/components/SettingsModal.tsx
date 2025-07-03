"use client";
import { useState } from "react";
import Appearance from "./settings/appearance";
import Profile from "./settings/profile";

interface SettingsModalProps {
  mode?: "appearance" | "profile";
}

export default function SettingsModal({
  mode = "appearance",
}: SettingsModalProps) {
  const [settingsMode, setSettingsMode] = useState<"appearance" | "profile">(
    mode
  );

  return (
    <div className="min-w-xl min-h-[50vh] flex flex-row">
      <div className="w-[30%] border-r-1 border-[#DDD] p-2 dark:border-[#444]">
        <div className="text-md px-2 pb-4 w-full border-b-1 border-[#EEE] dark:border-[#444]">
          <strong>Settings</strong>
        </div>
        <div className="py-2 flex flex-col gap-1">
          <div
            onClick={() => setSettingsMode("appearance")}
            className="w-full rounded-sm hover:bg-[#F9F9F9] dark:hover:bg-[#222222] border border-[transparent] hover:border hover:border-[#F3F3F3] dark:hover:border-[#333] px-2 cursor-pointer"
          >
            Appearance
          </div>
          <div
            onClick={() => setSettingsMode("profile")}
            className="w-full rounded-sm hover:bg-[#F9F9F9] dark:hover:bg-[#222222] border border-[transparent] hover:border hover:border-[#F3F3F3] dark:hover:border-[#333] px-2 cursor-pointer"
          >
            Profile
          </div>
          <div className="w-full rounded-sm hover:bg-[#F9F9F9] dark:hover:bg-[#222222] border border-[transparent] hover:border hover:border-[#F3F3F3]  dark:hover:border-[#333] px-2 cursor-pointer">
            Data
          </div>
        </div>
      </div>
      <div className="w-full bg-[#F3F3F3] dark:bg-[#0d0d0d]">
        {settingsMode === "appearance" ? <Appearance /> : <Profile />}
      </div>
    </div>
  );
}
