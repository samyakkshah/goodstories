import { create } from "zustand";
import { persist } from "zustand/middleware";
import { getProfile } from "@/lib/api";

type UserProfile = {
  id: string;
  email: string;
  username: string;
  name: string;
  avatar_url: string;
  bio: string | null;
  preferences: any;
  created_at: string;
};

type AuthState = {
  user: UserProfile | null;
  loading: boolean;
  setAuth: (user: UserProfile) => void;
  logout: () => void;
  fetchProfile: () => Promise<void>;
};

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      loading: true,
      setAuth: (user) => set({ user }),
      logout: () => set({ user: null }),
      fetchProfile: async () => {
        try {
          set({ loading: true });
          const user = await getProfile();
          set({ user });
        } catch (err) {
          set({ user: null });
        } finally {
          set({ loading: false });
        }
      },
    }),
    {
      name: "auth-storage",
      partialize: (state) => ({ user: state.user }),
    }
  )
);
