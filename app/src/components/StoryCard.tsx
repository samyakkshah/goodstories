import { Card, CardContent } from "@/components/ui/card";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Skeleton } from "./ui/skeleton";
import { useLikesStore } from "@/store/likeStore";
import { Heart } from "lucide-react";
import { motion } from "framer-motion";
import clsx from "clsx";

export function StoryCard({
  story_id,
  title,
  content,
  genre,
  tone,
  pages,
  likes_count,
  created_at,
  handleLike,
  cover_image_url,
}: StoryCardProps) {
  const { likedStoryIds } = useLikesStore();
  const isLiked = likedStoryIds.has(String(story_id));

  return (
    <Card className="min-h-64 h-full min-w-32 p-0 overflow-hidden rounded-lg hover:shadow-md transition bg-[#F8F8F8] dark:bg-[#151515]">
      <CardContent className="flex flex-col h-full mt-0 p-0 justify-between">
        {/* IMAGE / PLACEHOLDER */}
        <motion.div
          initial={{ opacity: 0.4 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8, ease: "easeInOut" }}
          className={clsx(
            "relative min-h-50 overflow-hidden",
            "bg-[#D9D9D9] dark:bg-[#222222]",
            "transition-colors duration-300 ease-in-out aspect-square"
          )}
        >
          <div className="w-full h-full overflow-hidden">
            {cover_image_url && (
              <img
                src={cover_image_url}
                alt={title}
                className="w-full h-full object-cover"
              />
            )}
          </div>
          <div className="absolute z-[999] w-full h-full top-0 p-3 flex flex-row justify-end">
            <div className="flex flex-col justify-between items-end gap-1">
              <div
                className={clsx(
                  "px-1 rounded-sm border text-[0.75rem]",
                  "bg-[#FBFBFB] dark:bg-[#1F1F1F]",
                  "border-[#D2D2D2] dark:border-[#414141]",
                  "text-[#8B8B8B] dark:text-[#C8C8C8]",
                  "transition-colors duration-300 ease-in-out"
                )}
              >
                {created_at &&
                  new Date(created_at).toLocaleString("en-US", {
                    month: "long",
                    day: "numeric",
                    year: "numeric",
                    hour12: true,
                  })}
              </div>
              <div
                className={clsx(
                  "px-2 w-fit rounded-sm border text-[0.75rem]",
                  "bg-[#FBFBFB] dark:bg-[#1F1F1F]",
                  "border-[#D2D2D2] dark:border-[#414141]",
                  "text-[#8B8B8B] dark:text-[#C8C8C8]",
                  "transition-colors duration-300 ease-in-out shadow-md"
                )}
              >
                Pages: {pages}
              </div>
            </div>
          </div>
        </motion.div>

        {/* CONTENT */}
        <div
          className={clsx(
            "p-3 max-h-[50%] flex flex-col justify-between",
            "",
            "transition-colors duration-300 ease-in-out"
          )}
        >
          <div
            className={clsx(
              "prose prose-invert text-lg font-semibold",
              "text-black dark:text-[#C0C0C0]",
              "transition-colors duration-300 ease-in-out"
            )}
          >
            <Markdown key={story_id} remarkPlugins={[remarkGfm]}>
              {title}
            </Markdown>
          </div>

          <div className="w-full flex justify-between gap-2 text-xs mt-2">
            {/* LIKE BUTTON */}
            <div className="flex flex-row gap-2 items-center justify-center">
              <button
                onClick={() => handleLike(story_id)}
                className={clsx(
                  "flex items-center gap-2 cursor-pointer",
                  "hover:text-red-500 transition-colors duration-300 ease-in-out"
                )}
              >
                <Heart
                  fill={isLiked ? "red" : "none"}
                  className={clsx(
                    isLiked ? "text-red-500" : "",
                    "hover:text-red-500 transition-colors duration-300 ease-in-out"
                  )}
                  width={"18px"}
                />
              </button>
              <span className="text-[#8B8B8B] dark:text-[#C8C8C8] transition-colors duration-300 ease-in-out">
                {likes_count}
              </span>
            </div>

            {/* GENRE + READ */}
            <div className="flex flex-row gap-2">
              <div
                className={clsx(
                  "p-1 rounded-sm border",
                  "bg-[#FBFBFB] dark:bg-[#1F1F1F]",
                  "border-[#D2D2D2] dark:border-[#414141]",
                  "text-[#8B8B8B] dark:text-[#C8C8C8]",
                  "transition-colors duration-300 ease-in-out"
                )}
              >
                {genre?.split(",")[0]}
              </div>
              <button
                onClick={() => (window.location.href = `/story/${story_id}`)}
                className={clsx(
                  "px-6 py-1 rounded-sm cursor-pointer border",
                  "bg-[#E3E3E3] dark:bg-[#2F2F2F]",
                  "border-[#DADADA] dark:border-[#414141]",
                  "text-[#5B5B5B] dark:text-[#C0C0C0]",
                  "hover:bg-[#D2D2D2] dark:hover:bg-[#1F1F1F]",
                  "transition-colors duration-300 ease-in-out"
                )}
              >
                Read
              </button>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
