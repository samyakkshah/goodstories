import { Command, CommandInput } from "@/components/ui/command";
import React from "react";

function Search() {
  return (
    <div className="w-full h-full p-3 flex justify-center items-center">
      <div className="min-w-xl max-w-5xl">
        <Command className="bg-[#F3F3F3]">
          <CommandInput placeholder="Search" />
        </Command>
      </div>
    </div>
  );
}

export default Search;
