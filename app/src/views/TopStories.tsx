"use client";
import Loading from "@/components/Loading";
import { StoryCard } from "@/components/StoryCard";
import { fetchStoryFeed } from "@/lib/api";
import { useLikesStore } from "@/store/likeStore";
import { useEffect, useState } from "react";

function TopStories() {
  const [stories, setStories] = useState<Array<Record<string, any>>>([]);
  const [loading, setLoading] = useState<boolean>(false);
  useEffect(() => {
    setLoading(true);
    fetchStoryFeed(20)
      .then(setStories)
      .catch(console.error)
      .finally(() => {
        setLoading(false);
      });
  }, []);

  const { likedStoryIds, toggleLike } = useLikesStore();

  const handleLike = async (storyId: any) => {
    const newStories = [...stories];
    const index = newStories.findIndex((s) => s.metadata.story_id === storyId);
    console.log(index);
    if (index !== -1) {
      const story = newStories[index];
      if (likedStoryIds.has(storyId)) {
        story.metadata.likes_count--;
      } else {
        story.metadata.likes_count++;
      }
    }
    console.log(newStories);
    setStories(newStories);
    await toggleLike(storyId);
  };

  return (
    <div key={"top-stories"} className="">
      <h1 className="text-2xl font-bold mb-4">Story Feed</h1>
      {loading ? (
        <Loading />
      ) : (
        <div className="w-full h-full grid gap-5 grid-cols-1 sm:grid-cols-2 lg:grid-cols-4">
          {stories.map(
            (story, id) =>
              story.pages.length > 0 && (
                <div key={id} className="h-full">
                  <StoryCard
                    key={id}
                    story_id={story["metadata"].story_id}
                    title={story["metadata"].title}
                    content={story["pages"].content}
                    genre={story["metadata"].genre}
                    tone={story["metadata"].tone}
                    pages={story["metadata"].current_page_number}
                    likes_count={story["metadata"].likes_count}
                    created_at={story["metadata"].created_at}
                    handleLike={handleLike}
                    cover_image_url={story["metadata"].cover_image_url}
                  />
                </div>
              )
          )}
        </div>
      )}
    </div>
  );
}

export default TopStories;
