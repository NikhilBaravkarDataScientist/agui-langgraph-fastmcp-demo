import "./globals.css";
import type { ReactNode } from "react";

export const metadata = {
  title: "NASA Space Explorer - Powered by NASA APIs",
  description: "Explore space with NASA's real-time data: APOD, Mars Rovers, Near Earth Objects, and more",
};

export default function RootLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
