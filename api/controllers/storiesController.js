import { supabasePublic as supabase } from "../services/supabaseClient.js";

export const getStories = async (req, res) => {
  const { count = 10 } = req.query;

  // Fetch top N stories
  const { data: stories, error } = await supabase
    .from("stories")
    .select("*")
    .order("created_at", { ascending: false });

  if (error) {
    return res.status(500).json({ error: error.message });
  }

  if (!stories) {
    return res.json([]);
  }

  const result = [];

  // For each story, fetch its pages
  for (const story of stories) {
    const { data: pages, error: pagesError } = await supabase
      .from("story_pages")
      .select("*")
      .eq("story_id", story.story_id)
      .order("page_number", { ascending: true });

    if (pagesError) {
      return res.status(500).json({ error: pagesError.message });
    }

    result.push({
      metadata: story,
      pages: pages ?? [],
    });
  }

  res.json(result);
};

export const getStoriesForToday = async (req, res) => {
  const startOfToday = new Date();
  startOfToday.setUTCHours(0, 0, 0, 0);

  const { data, error } = await supabase
    .from("stories")
    .select("*")
    .gte("created_at", startOfToday.toISOString())
    .order("created_at", { ascending: false });

  if (error) return res.status(500).json({ error: error.message });

  res.json(data);
};

export const getFullStoryWithPages = async (req, res) => {
  const { id } = req.params;

  // Fetch story metadata
  const { data: story, error: storyError } = await supabase
    .from("stories")
    .select("*")
    .eq("story_id", id)
    .single();

  if (storyError || !story) {
    return res.status(404).json({ error: "Story not found" });
  }

  // Fetch all pages
  const { data: pages, error: pagesError } = await supabase
    .from("story_pages")
    .select("*")
    .eq("story_id", id)
    .order("page_number", { ascending: true });

  if (pagesError) {
    return res.status(500).json({ error: pagesError.message });
  }

  // Return combined structure
  res.json({
    metadata: story,
    pages: pages,
  });
};
export const getLastNPages = async (req, res) => {
  const { id } = req.params;
  const { n = 2 } = req.query;

  const { data, error } = await supabase
    .from("story_pages")
    .select("*")
    .eq("story_id", id)
    .order("page_number", { ascending: false })
    .limit(parseInt(n));

  if (error) return res.status(500).json({ error: error.message });

  // Reverse to get oldest-to-newest order
  res.json(data.reverse());
};
