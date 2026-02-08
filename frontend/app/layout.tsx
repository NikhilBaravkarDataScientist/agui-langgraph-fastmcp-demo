import "./globals.css";
import type { ReactNode } from "react";

export const metadata = {
  title: "AGUI LangGraph FastMCP",
  description: "Agentic AI with AGUI, LangGraph, and FastMCP",
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
