import { notFound } from "next/navigation";
import { fetchStory } from "@/lib/api";
import ZoomableStoryPageClient from "@/components/ZoomableStoryPageClient";

export default async function StoryPage({ params }: StoryPageProps) {
  let story;
  try {
    story = await fetchStory(params.story_id);
  } catch (error) {
    console.error("Story fetch error:", error);
    notFound();
  }
  return <ZoomableStoryPageClient story={story} />;
}
