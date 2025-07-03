"use client";

import React, { useEffect, useState } from "react";
import { getUserLikes } from "@/lib/api";
import { StoryCard } from "@/components/StoryCard";
import Loading from "@/components/Loading";
import { useLikesStore } from "@/store/likeStore";
import { toast } from "sonner";
import { useAuthStore } from "@/store/authStore";

function Liked() {
  const [likedStories, setLikedStories] = useState<Array<any>>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const { user } = useAuthStore();
  const { likedStoryIds, toggleLike } = useLikesStore();

  useEffect(() => {
    const fetchLiked = async () => {
      try {
        setLoading(true);
        const data = await getUserLikes();
        setLikedStories(data);
      } catch (err) {
        console.error("Error fetching liked stories", err);
        toast.error("Failed to load liked stories.");
      } finally {
        setLoading(false);
      }
    };

    fetchLiked();
  }, []);

  useEffect(() => {
    if (user) {
      useLikesStore.getState().loadUserLikes();
    }
  }, [user]);

  const handleLike = async (storyId: string) => {
    const wasLiked = likedStoryIds.has(storyId);

    // Optimistic update
    setLikedStories((prev) =>
      prev
        .map((item) => {
          if (item.story.story_id === storyId) {
            return {
              ...item,
              story: {
                ...item.story,
                likes_count: wasLiked
                  ? Math.max(0, item.story.likes_count - 1)
                  : item.story.likes_count + 1,
              },
            };
          }
          return item;
        })
        // If unliked, optionally remove from list:
        .filter((item) => (wasLiked ? item.story.story_id !== storyId : true))
    );

    try {
      await toggleLike(storyId);
    } catch (err) {
      console.error("Error toggling like", err);
      toast.error("Failed to update like.");
    }
  };

  console.log(likedStories);

  return (
    <section className="p-5 max-w-7xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Liked Stories</h1>
      {loading ? (
        <Loading />
      ) : likedStories.length === 0 ? (
        <p className="text-muted-foreground">
          You haven't liked any stories yet.
        </p>
      ) : (
        <div className="w-full h-full grid gap-5 grid-cols-1 sm:grid-cols-2 lg:grid-cols-4">
          {likedStories.map((item) => (
            <StoryCard
              key={item.story.story_id}
              story_id={item.story.story_id}
              title={item.story.title}
              genre={item.story.genre}
              tone={item.story.tone}
              likes_count={item.story.likes_count}
              created_at={item.story.created_at}
              pages={item.story.current_page_number}
              handleLike={handleLike}
              cover_image_url={item.story.cover_image_url}
            />
          ))}
        </div>
      )}
    </section>
  );
}

export default Liked;
