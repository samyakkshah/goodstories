import { supabaseAdmin as supabase } from "../services/supabaseClient.js";

export const likeStory = async (req, res) => {
  const userId = req.user.id;
  const { story_id } = req.body;

  if (!story_id) {
    return res.status(400).json({
      error: "story_id is required",
    });
  }

  const { error } = await supabase
    .from("story_likes")
    .insert([{ user_id: userId, story_id }]);

  if (error) {
    console.error("Error liking story:", error);
    return res.status(500).json({ error: error.message });
  }

  await supabase.rpc("increment_likes_count", { sid: story_id });

  res.json({ success: true });
};

export const unlikeStory = async (req, res) => {
  const userId = req.user.id;
  const { id: story_id } = req.params;

  if (!story_id) {
    return res.status(400).json({ error: "story_id is required" });
  }

  const { error } = await supabase
    .from("story_likes")
    .delete()
    .eq("user_id", userId)
    .eq("story_id", story_id);

  if (error) {
    console.error("Error unliking story:", error);
    return res.status(500).json({ error: error.message });
  }

  await supabase.rpc("decrement_likes_count", { sid: story_id });

  res.json({ success: true });
};

export const getMyLikes = async (req, res) => {
  const userId = req.user.id;

  const { data, error } = await supabase
    .from("story_likes")
    .select("story_id, created_at, stories(*)")
    .eq("user_id", userId)
    .order("created_at", { ascending: false });

  if (error) {
    console.error("Error fetching likes:", error);
    return res.status(500).json({ error: error.message });
  }

  const result = data.map((like) => ({
    story_id: like.story_id,
    liked_at: like.created_at,
    story: like.stories,
  }));

  res.json(result);
};
