import { create } from "zustand";
import { getUserLikes, likeStory, unlikeStory } from "@/lib/api";

type LikesStore = {
  likedStoryIds: Set<string>;
  loading: boolean;
  loadUserLikes: () => Promise<void>;
  toggleLike: (storyId: string) => Promise<boolean>;
};

export const useLikesStore = create<LikesStore>((set, get) => ({
  likedStoryIds: new Set(),
  loading: false,

  loadUserLikes: async () => {
    set({ loading: true });
    try {
      const data = await getUserLikes();
      const ids = new Set<string>(
        data.map((item: { story_id: string }) => item.story_id)
      );
      set({ likedStoryIds: ids });
    } catch (err) {
      console.error("Failed to load likes", err);
    } finally {
      set({ loading: false });
    }
  },

  toggleLike: async (storyId) => {
    const { likedStoryIds } = get();
    const isLiked = likedStoryIds.has(storyId);

    try {
      if (isLiked) {
        await unlikeStory(storyId);
        likedStoryIds.delete(storyId);
      } else {
        await likeStory(storyId);
        likedStoryIds.add(storyId);
      }
      set({ likedStoryIds: new Set(likedStoryIds) });
      return !isLiked;
    } catch (err) {
      console.error("Toggle like failed:", err);
      return isLiked;
    }
  },
}));
