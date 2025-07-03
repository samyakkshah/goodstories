"use client";

import { useState, useEffect } from "react";
import { useAuthStore } from "@/store/authStore";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { getAvatarUploadUrl, updateProfile } from "@/lib/api";
import { toast } from "sonner";

export default function EditProfilePage() {
  const { user, fetchProfile } = useAuthStore();

  const [form, setForm] = useState({
    name: "",
    username: "",
    bio: "",
    avatar_url: "",
    preferences: "",
  });

  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (user) {
      setForm({
        name: user.name || "",
        username: user.username,
        bio: user.bio || "",
        avatar_url: user.avatar_url || "",
        preferences: user.preferences
          ? JSON.stringify(user.preferences, null, 2)
          : "",
      });
    }
  }, [user]);

  const handleChange = (e: { target: { name: any; value: any } }) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;
    const file = files[0];

    try {
      setLoading(true);

      // 1️⃣ Get signed upload URL from backend
      const { uploadUrl, path } = await getAvatarUploadUrl(file.name);

      // 2️⃣ Upload directly to Supabase Storage
      await fetch(uploadUrl, {
        method: "PUT",
        headers: { "Content-Type": file.type },
        body: file,
      });

      // 3️⃣ Update user's avatar_url in your DB
      await updateProfile({ avatar_url: path });
      await fetchProfile();
      toast.success("Profile picture updated!");
    } catch (err) {
      console.error(err);
      toast.error("Failed to update profile picture.");
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    setLoading(true);
    try {
      await updateProfile({
        name: form.name,
        bio: form.bio,
        avatar_url: form.avatar_url,
        preferences: form.preferences ? JSON.parse(form.preferences) : null,
      });
      await fetchProfile();
      toast.success("Profile updated successfully!");
    } catch (err) {
      console.error(err);
      toast.error("Failed to update profile.");
    } finally {
      setLoading(false);
    }
  };

  const handleDeletePicture = async () => {
    try {
      setLoading(true);
      console.log("Updating profile:", { avatar_url: null });
      await updateProfile({ avatar_url: null });
      await fetchProfile();
      toast.success("Profile picture removed!");
    } catch (err) {
      console.error(err);
      toast.error("Failed to remove picture.");
    } finally {
      setLoading(false);
    }
  };

  if (!user) {
    return (
      <div className="p-6 text-center text-muted-foreground">
        <p>You must be logged in to edit your profile.</p>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-6">Edit Profile</h2>
      <div className="flex flex-col items-center mb-6">
        <Avatar className="w-24 h-24 mb-3">
          {form.avatar_url ? (
            <AvatarImage
              src={form.avatar_url}
              alt={form.name}
              className="object-cover"
            />
          ) : (
            <AvatarFallback>
              {form.name ? form.name.slice(0, 2).toUpperCase() : "US"}
            </AvatarFallback>
          )}
        </Avatar>
        <div className="flex gap-2">
          <label htmlFor="avatar-upload">
            <input
              type="file"
              accept="image/jpeg, image/png, image/jpg, image/heic"
              className="hidden"
              id="avatar-upload"
              onChange={handleFileChange}
            />
            <div>Change Picture</div>
          </label>
          <Button onClick={handleDeletePicture} variant="destructive">
            Delete picture
          </Button>
        </div>
      </div>

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Profile name
          </label>
          <Input
            name="name"
            value={form.name}
            onChange={handleChange}
            placeholder="Your full name"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Username
          </label>
          <Input
            name="username"
            value={`@${form.username}`}
            disabled
            className="bg-gray-100"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            About me
          </label>
          <Textarea
            name="bio"
            value={form.bio}
            onChange={handleChange}
            placeholder="Tell us about yourself..."
          />
        </div>

        <Button onClick={handleSave} disabled={loading} className="w-full mt-4">
          {loading ? "Saving..." : "Save changes"}
        </Button>
      </div>
    </div>
  );
}
