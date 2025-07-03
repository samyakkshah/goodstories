import { supabaseAdmin, supabasePublic } from "../services/supabaseClient.js";
import crypto from "crypto";
export const signUpWithPassword = async (req, res) => {
  try {
    const { email, password, username, name, avatar_url } = req.body;

    if (!email || !password || !username) {
      return res
        .status(400)
        .json({ error: "Email, password, and username are required" });
    }

    if (!email.includes("@")) {
      return res.status(400).json({ error: "Invalid email format" });
    }

    const { data: existingUser } = await supabaseAdmin
      .from("users")
      .select("id")
      .eq("username", username)
      .single();

    if (existingUser) {
      return res.status(400).json({ error: "Username already taken" });
    }

    const { data: createdUser, error: createError } =
      await supabaseAdmin.auth.admin.createUser({
        email,
        password,
        email_confirm: true,
        user_metadata: { name, avatar_url },
      });

    if (createError) {
      console.error("Error creating Supabase Auth user:", createError);
      return res.status(400).json({ error: createError.message });
    }

    const userId = createdUser.user.id;

    const { error: dbError } = await supabaseAdmin.from("users").insert([
      {
        id: userId,
        email,
        username,
        name,
        avatar_url,
        created_at: new Date(),
      },
    ]);

    if (dbError) {
      console.error("Error inserting user profile:", dbError);
      return res.status(500).json({ error: dbError.message });
    }

    const { data: signInData, error: signInError } =
      await supabasePublic.auth.signInWithPassword({
        email,
        password,
      });

    if (signInError) {
      console.error("Error signing in after signup:", signInError);
      return res.status(500).json({ error: signInError.message });
    }

    res.cookie("token", signInData.session.access_token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "strict",
      maxAge: 1000 * 60 * 60 * 24 * 7, // 7 days
    });

    res.status(201).json({
      success: true,
      user: {
        id: userId,
        email,
        username,
        name,
        avatar_url,
      },
    });
  } catch (err) {
    console.error("Signup error:", err);
    res.status(500).json({ error: "Internal server error" });
  }
};

export const signInWithPassword = async (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ error: "Email and password are required" });
    }

    const { data: signInData, error: signInError } =
      await supabasePublic.auth.signInWithPassword({
        email,
        password,
      });

    if (signInError) {
      console.error("Sign-in error:", signInError);
      return res.status(401).json({ error: "Invalid email or password" });
    }

    const userId = signInData.user.id;

    await supabaseAdmin
      .from("users")
      .update({ last_login: new Date() })
      .eq("id", userId);

    const { data: userProfile, error: profileError } = await supabaseAdmin
      .from("users")
      .select("*")
      .eq("id", userId)
      .single();

    if (profileError || !userProfile) {
      console.error("Profile fetch error:", profileError);
      return res.status(404).json({ error: "User profile not found" });
    }

    res.cookie("token", signInData.session.access_token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "strict",
      maxAge: 1000 * 60 * 60 * 24 * 7, // 7 days
    });

    // 4️⃣ Return complete user info
    res.json({
      success: true,
      user: {
        id: userProfile.id,
        email: userProfile.email,
        username: userProfile.username,
        name: userProfile.name,
        avatar_url: userProfile.avatar_url,
        bio: userProfile.bio,
        preferences: userProfile.preferences,
        created_at: userProfile.created_at,
      },
    });
  } catch (err) {
    console.error("Sign-in controller error:", err);
    res.status(500).json({ error: "Internal server error" });
  }
};

export const getProfile = async (req, res) => {
  try {
    const token = req.cookies.token;

    if (!token) {
      return res.status(401).json({ error: "Unauthorized" });
    }
    const { data, error } = await supabasePublic.auth.getUser(token);

    if (error || !data.user) {
      return res.status(401).json({ error: "Invalid token" });
    }
    const userId = data.user.id;
    const { data: userProfile } = await supabaseAdmin
      .from("users")
      .select("*")
      .eq("id", userId)
      .single();

    if (userProfile.avatar_url) {
      const { data: signedUrlData, error } = await supabaseAdmin.storage
        .from("avatars")
        .createSignedUrl(userProfile.avatar_url, 60 * 60); // 1 hour

      if (!error) {
        userProfile.avatar_signed_url = signedUrlData.signedUrl;
      }
    }

    res.json({
      success: true,
      user: {
        id: userProfile.id,
        email: userProfile.email,
        username: userProfile.username,
        name: userProfile.name,
        avatar_url: userProfile.avatar_signed_url,
        bio: userProfile.bio,
        preferences: userProfile.preferences,
        created_at: userProfile.created_at,
      },
    });
  } catch (err) {
    console.error("Get profile error:", err);
    res.status(500).json({ error: "Internal server error" });
  }
};

export const updateProfile = async (req, res) => {
  try {
    const userId = req.user.id;

    const { data: currentUser, error: fetchError } = await supabaseAdmin
      .from("users")
      .select("avatar_url")
      .eq("id", userId)
      .single();

    if (fetchError) {
      console.error("Error fetching current user:", fetchError);
      return res.status(500).json({ error: "Could not fetch current user." });
    }

    if (!userId) {
      return res.status(401).json({ error: "Unauthorized" });
    }

    const { name, username, avatar_url, bio, preferences } = req.body;

    if (avatar_url === null && currentUser?.avatar_url) {
      const { error: deleteError } = await supabaseAdmin.storage
        .from("avatars")
        .remove([currentUser.avatar_url]);

      if (deleteError) {
        console.error("Error deleting old avatar from storage:", deleteError);
        // Optional: don't block request, just log
      }
    }

    // Nothing to update?
    if (
      name === undefined &&
      username === undefined &&
      avatar_url === undefined &&
      bio === undefined &&
      preferences === undefined
    ) {
      return res.status(400).json({ error: "Nothing to update" });
    }

    // Validate username
    if (username && username.trim() === "") {
      return res.status(400).json({ error: "Username cannot be empty" });
    }

    // Check if username is changing and is unique
    if (username) {
      const { data: existingUser } = await supabaseAdmin
        .from("users")
        .select("id")
        .eq("username", username)
        .neq("id", userId)
        .single();

      if (existingUser) {
        return res.status(400).json({ error: "Username already taken" });
      }
    }

    // Validate preferences if provided
    if (preferences && typeof preferences !== "object") {
      return res
        .status(400)
        .json({ error: "Preferences must be a JSON object" });
    }

    // Build update object
    const updates = {};
    if (name !== undefined) updates.name = name;
    if (username !== undefined) updates.username = username;
    if (avatar_url !== undefined) updates.avatar_url = avatar_url;
    if (bio !== undefined) updates.bio = bio;
    if (preferences !== undefined) updates.preferences = preferences;
    // Update user
    const { data: updatedUser, error } = await supabaseAdmin
      .from("users")
      .update(updates)
      .eq("id", userId)
      .select("*")
      .single();

    if (error) {
      console.error("Error updating profile:", error);
      return res.status(500).json({ error: error.message });
    }

    res.json({
      success: true,
      user: {
        id: updatedUser.id,
        email: updatedUser.email,
        username: updatedUser.username,
        name: updatedUser.name,
        avatar_url: updatedUser.avatar_url,
        bio: updatedUser.bio,
        preferences: updatedUser.preferences,
        created_at: updatedUser.created_at,
      },
    });
  } catch (err) {
    console.error("Update profile error:", err);
    res.status(500).json({ error: "Internal server error" });
  }
};

export const createAvatarUploadUrl = async (req, res) => {
  try {
    const userId = req.user.id;
    const { fileName } = req.body;

    if (!fileName || typeof fileName !== "string") {
      return res.status(400).json({ error: "Missing or invalid fileName" });
    }

    // Extract extension
    const ext = fileName.split(".").pop();

    // Create unique file name
    const uniqueId = crypto.randomBytes(8).toString("hex");
    const newFileName = `avatar-${uniqueId}.${ext}`;

    // Build storage path
    const path = `avatars/${userId}/${newFileName}`;

    // Create signed upload URL
    const { data, error } = await supabaseAdmin.storage
      .from("avatars")
      .createSignedUploadUrl(path, 60);

    if (error) {
      console.error("Error creating signed upload URL:", error);
      return res.status(500).json({ error: error.message });
    }

    res.json({
      success: true,
      uploadUrl: data.signedUrl,
      path,
    });
  } catch (err) {
    console.error("Avatar upload URL error:", err);
    res.status(500).json({ error: "Internal server error" });
  }
};

export const logout = (req, res) => {
  res.clearCookie("token", {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "strict",
  });
  res.json({ success: true });
};
