import express from "express";
import storiesRoutes from "./routes/stories.js";
import authRoutes from "./routes/auth.js";
import likesRoutes from "./routes/likes.js";
import dotenv from "dotenv";
import cors from "cors";
import cookieParser from "cookie-parser";

dotenv.config();

const app = express();
app.use(express.json());

app.use(
  cors({
    origin: "http://localhost:3000",
    credentials: true,
  })
);

app.use(cookieParser());

app.use("/stories", storiesRoutes);
app.use("/auth", authRoutes);
app.use("/likes", likesRoutes);

const PORT = process.env.PORT || 8000;
app.listen(PORT, () => console.log(`Backend running on port ${PORT}`));
