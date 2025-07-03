import { supabasePublic } from "../services/supabaseClient.js";

export const authenticateUser = async (req, res, next) => {
  try {
    const token = req.cookies.token;

    if (!token) {
      return res.status(401).json({ error: "Missing auth token cookie" });
    }

    const { data, error } = await supabasePublic.auth.getUser(token);

    if (error || !data?.user) {
      return res.status(401).json({ error: "Invalid or expired token" });
    }

    req.user = data.user;
    next();
  } catch (err) {
    console.error("Auth middleware error:", err);
    return res.status(500).json({ error: "Internal server error" });
  }
};
