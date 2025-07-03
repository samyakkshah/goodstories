type StoryCardProps = {
  story_id: number;
  title: string;
  content?: string;
  genre?: string;
  tone?: string;
  pages?: number;
  likes_count?: number;
  created_at?: Date;
  handleLike: (story_id: any) => void;
  cover_image_url?: string;
};
