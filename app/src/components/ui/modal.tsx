"use client";
import { useModalStore } from "@/store/modalStore";
import { XCircleIcon } from "lucide-react";

export default function Modal() {
  const { isOpen, content, closeModal } = useModalStore();

  if (!isOpen || !content) return null;

  return (
    <div className="fixed inset-0 z-[999] backdrop-blur-xs flex items-center justify-center bg-black/50">
      <div className="fixed w-full h-full" onClick={closeModal} />
      <div className="bg-white dark:bg-[#111] overflow-hidden rounded-lg shadow-lg w-[fit-content] h-[fit-content] relative">
        <button
          className="absolute top-2 right-2 text-gray-500 hover:text-red-500 cursor-pointer"
          onClick={closeModal}
        >
          <XCircleIcon width={20} height={20} />
        </button>
        {content}
      </div>
    </div>
  );
}
