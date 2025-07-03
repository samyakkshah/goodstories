import express from "express";
import { authenticateUser } from "../middlewares/authMiddleware.js";
import {
  likeStory,
  unlikeStory,
  getMyLikes,
} from "../controllers/likesController.js";

const router = express.Router();

router.use(authenticateUser);

router.post("/", likeStory);
router.delete("/:id", unlikeStory);
router.get("/", getMyLikes);

export default router;
