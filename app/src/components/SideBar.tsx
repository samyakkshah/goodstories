"use client";
import {
  Book,
  BookHeart,
  BookmarkCheck,
  Cog,
  Heart,
  Home,
  Library,
  Search,
  TextSearch,
  User,
} from "lucide-react";
import React, { use } from "react";
import { Avatar, AvatarFallback, AvatarImage } from "./ui/avatar";
import { useAuthStore } from "@/store/authStore";
import AuthModalComponent from "@/components/Auth/AuthModalComponent";
import {
  Tooltip,
  TooltipTrigger,
  TooltipContent,
} from "@/components/ui/tooltip";
import { useRouter } from "next/navigation";
import SettingsModal from "./SettingsModal";
import { useModalStore } from "@/store/modalStore";

function SideBar({ params }: { params?: any }) {
  const router = useRouter();
  const routerPush = (params: string) => {
    router.push(params);
  };
  const { openModal } = useModalStore();
  const { user } = useAuthStore();
  return (
    <div className="fixed w-60 h-screen flex flex-row bg-white dark:bg-[#0d0d0d]">
      <div className="h-full w-12 p-2 border-r-1 border-zinc-300 flex flex-col justify-between dark:border-zinc-800">
        <div className="group h-full btn-group w-full flex flex-col justify-between items-center">
          <button
            onClick={() => routerPush("/")}
            className="p-1 border-2 border-[#F2F2F2] dark:border-zinc-800 rounded-lg flex justify-center items-center aspect-square cursor-pointer hover:bg-[#EEE] hover:border-[#DDD] transition-all duration-300 ease"
          >
            <Home width={"20px"} height={"20px"} className="text-[#818181]" />
          </button>
        </div>
        <div className="relative cursor-pointer">
          <AvatarArea routerPush={routerPush} />
          {/*Green Dot*/}
          {user && (
            <div className="absolute bottom-1 right-0 w-2 h-2 bg-green-500 outline-2 outline-white rounded-full dark:outline-zinc-800"></div>
          )}
        </div>
      </div>
      <div className="w-full border-r-1 border-zinc-300 flex flex-col justify-between dark:border-zinc-800">
        <div>
          <div className="w-full px-2 py-6 text-xl bg-[#FDFDFD] text-center border-b-1 text-black dark:border-zinc-800 dark:bg-[#141414] dark:text-zinc-500">
            <div className="flex flex-row gap-2 items-center justify-center font-bold">
              <img src="/logo.png" width={"15px"} height={"15px"} />
              Good Stories
            </div>
          </div>
          <nav className="mt-3 p-2 flex flex-col gap-2 ">
            <button
              onClick={() => routerPush("/liked")}
              className="flex flex-row justify-start border border-[#fff] items-center gap-2 px-2 py-1 rounded-sm hover:bg-[#F9F9F9] hover:border hover:border-[#EEE] cursor-pointer text-[#818181] hover:text-[#222] transition-all duration-100 ease
              dark:border-[#0d0d0d] dark:hover:border-[#333] dark:hover:bg-[#222] dark:hover:text-white
              "
            >
              <div>
                <BookHeart width={16} height={16} />
              </div>
              <p>Liked</p>
            </button>
            <button
              className="flex flex-row justify-start border border-[#fff] items-center gap-2 px-2 py-1 rounded-sm hover:bg-[#F9F9F9] hover:border hover:border-[#EEE] cursor-pointer text-[#818181] hover:text-[#222] transition-all duration-100 ease
            dark:border-[#0d0d0d] dark:hover:border-[#333] dark:hover:bg-[#222] dark:hover:text-white
            "
            >
              <div>
                <BookmarkCheck width={16} height={16} />
              </div>
              <p>Followed</p>
            </button>
            <button
              className="flex flex-row justify-start border border-[#fff] items-center gap-2 px-2 py-1 rounded-sm hover:bg-[#F9F9F9] hover:border hover:border-[#EEE] cursor-pointer text-[#818181] hover:text-[#222] transition-all duration-100 ease
            dark:border-[#0d0d0d] dark:hover:border-[#333] dark:hover:bg-[#222] dark:hover:text-white
            "
            >
              <div>
                <Library width={16} height={16} />
              </div>
              <p>Explore</p>
            </button>
            <button
              onClick={() => routerPush("search")}
              className="flex flex-row justify-start border border-[#fff] items-center gap-2 px-2 py-1 rounded-sm hover:bg-[#F9F9F9] hover:border hover:border-[#EEE] cursor-pointer text-[#818181] hover:text-[#222] transition-all duration-100 ease
              dark:border-[#0d0d0d] dark:hover:border-[#333] dark:hover:bg-[#222] dark:hover:text-white
              "
            >
              <div>
                <Search width={16} height={16} />
              </div>
              <p>Search</p>
            </button>
          </nav>
        </div>
        <div className="p-2">
          <div
            onClick={() => openModal(<SettingsModal />)}
            className="flex flex-row justify-start border border-[#fff] items-center gap-2 px-2 py-1 rounded-sm hover:bg-[#F9F9F9] hover:border hover:border-[#EEE] cursor-pointer text-[#818181] hover:text-[#222] transition-all duration-100 ease
            dark:border-[#0d0d0d] dark:hover:border-[#333] dark:hover:bg-[#222] dark:hover:text-white
            "
          >
            <div>
              <Cog width={16} height={16} />
            </div>
            <p>Settings</p>
          </div>
        </div>
      </div>
    </div>
  );
}

function AvatarArea({ routerPush }: { routerPush: (params: string) => void }) {
  const { user } = useAuthStore();
  const { openModal } = useModalStore();
  console.log(user);
  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <button
          onClick={() => {
            if (user) {
              openModal(<SettingsModal mode="profile" />);
            } else {
              openModal(<AuthModalComponent />);
            }
          }}
          className="relative cursor-pointer rounded-full overflow-hidden border-2 border-[#F2F2F2] hover:border-[#DDD] transition-all dark:border-zinc-800 "
        >
          <Avatar className="">
            {user?.avatar_url ? (
              <AvatarImage
                src={user.avatar_url}
                alt={user.name || user.username}
                className="object-cover"
              />
            ) : (
              <AvatarFallback>
                {user ? (
                  (user.name || user.username || "U").slice(0, 2).toUpperCase()
                ) : (
                  <User width={"20px"} color="#D9D9D9" />
                )}
              </AvatarFallback>
            )}
          </Avatar>
        </button>
      </TooltipTrigger>
      <TooltipContent side="top">
        <p>
          {user ? (user.name ? `Profile: ${user.name}` : "Profile") : "Log in"}
        </p>
      </TooltipContent>
    </Tooltip>
  );
}

export default SideBar;
