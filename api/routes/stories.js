import express from "express";
import {
  getStories,
  getStoriesForToday,
  getFullStoryWithPages,
  getLastNPages,
} from "../controllers/storiesController.js";

const router = express.Router();

router.post("/", getStories);
router.get("/today", getStoriesForToday);
router.get("/:id", getFullStoryWithPages);
router.get("/:id/pages/recent", getLastNPages);

export default router;
