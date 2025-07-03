const BASE_URL = process.env.NEXT_PUBLIC_BASE_URL;

import { useLikesStore } from "@/store/likeStore";

export async function fetchStoryFeed(count: number = 10) {
  const res = await fetch(`${BASE_URL}/stories`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ count }),
  });

  if (!res.ok) throw new Error("Failed to fetch stories");
  return res.json();
}

export async function fetchStory(story_id: string) {
  const res = await fetch(`${BASE_URL}/stories/${story_id}`);
  if (!res.ok) throw new Error(`Failed to fetch story: ${story_id}`);

  return await res.json();
}

export async function signup(formData: {
  email: string;
  password: string;
  username: string;
  name?: string;
}) {
  const res = await fetch(`${BASE_URL}/auth/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(formData),
    credentials: "include",
  });

  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.error || "Signup failed");
  }

  return data;
}

export async function signin(formData: { email: string; password: string }) {
  const res = await fetch(`${BASE_URL}/auth/signin`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(formData),
    credentials: "include",
  });

  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.error || "Signin failed");
  }

  return data;
}

export async function getProfile() {
  const res = await fetch(`${BASE_URL}/auth/profile`, {
    credentials: "include",
  });

  if (!res.ok) throw new Error("Not authenticated");

  const { user } = await res.json();
  return user;
}

export async function updateProfile(payload: {
  name?: string;
  bio?: string;
  avatar_url?: string | null;
  preferences?: any;
}) {
  const res = await fetch(`${BASE_URL}/auth/profile`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    body: JSON.stringify(payload),
  });

  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.error || "Failed to update profile");
  }

  return data;
}

export async function getAvatarUploadUrl(fileName: string) {
  const res = await fetch(`${BASE_URL}/auth/avatar-upload-url`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ fileName }),
  });

  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Failed to get upload URL");

  return data;
}

export async function likeStory(storyId: string) {
  const res = await fetch(`${BASE_URL}/likes`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ story_id: storyId }),
  });

  if (!res.ok) {
    const data = await res.json();
    throw new Error(data.error || "Failed to like story");
  }

  return true;
}

export async function unlikeStory(storyId: string) {
  const res = await fetch(`${BASE_URL}/likes/${storyId}`, {
    method: "DELETE",
    credentials: "include",
  });

  if (!res.ok) {
    const data = await res.json();
    throw new Error(data.error || "Failed to unlike story");
  }

  return true;
}

export async function getUserLikes() {
  const res = await fetch(`${BASE_URL}/likes`, {
    credentials: "include",
  });

  if (!res.ok) {
    const data = await res.json();
    throw new Error(data.error || "Failed to fetch likes");
  }

  const data = await res.json();
  return data; // array of { story_id, liked_at, story: {...} }
}
