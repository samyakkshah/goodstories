import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import SideBar from "@/components/SideBar";
import Modal from "@/components/ui/modal";
import { ThemeProvider } from "next-themes";
import Providers from "@/lib/Providers";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Good Stories",
  description: "Read new stories everyday.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <Providers>
          <div className="flex flex-row gap-2 bg-[#F9F9F9] dark:bg-[#141414]">
            <aside className="w-72 h-full">
              <SideBar />
            </aside>
            <div className="w-full min-h-screen overflow-y-auto">
              {children}
            </div>

            <Modal />
          </div>
        </Providers>
      </body>
    </html>
  );
}
