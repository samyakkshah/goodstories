import Lottie from "lottie-react";
import loadingAnimation from "@/assets/animation/loading.json";

function Loading() {
  return (
    <div className=" w-100 h-100 flex justify-center items-center text-sm">
      <Lottie animationData={loadingAnimation} loop />
    </div>
  );
}

export default Loading;
