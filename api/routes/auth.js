import express from "express";
import { authenticateUser } from "../middlewares/authMiddleware.js";
import {
  signUpWithPassword,
  signInWithPassword,
  getProfile,
  updateProfile,
  createAvatarUploadUrl,
} from "../controllers/authController.js";

const router = express.Router();

router.post("/signup", signUpWithPassword);
router.post("/signin", signInWithPassword);
router.get("/profile", authenticateUser, getProfile);
router.patch("/profile", authenticateUser, updateProfile);
router.post("/avatar-upload-url", authenticateUser, createAvatarUploadUrl);

export default router;
