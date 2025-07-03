import { create } from "zustand";
import { persist } from "zustand/middleware";

type Story = {
  id: string;
  title: string;
  genre: string;
  tone: string;
  content: string;
};

type StoryState = {
  stories: Story[];
  addStory: (story: Story) => void;
  removeStory: (id: string) => void;
  clearStories: () => void;
};

export const useStoryStore = create<StoryState>()(
  persist(
    (set) => ({
      stories: [],
      addStory: (story) =>
        set((state) => ({ stories: [...state.stories, story] })),
      removeStory: (id) =>
        set((state) => ({ stories: state.stories.filter((s) => s.id !== id) })),
      clearStories: () => set({ stories: [] }),
    }),
    {
      name: "goodstories-storage", // localStorage key
    }
  )
);
