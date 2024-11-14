import TopLoader from "@/components/layouts/TopLoader";
import { BASE_URL } from "@/lib/constants";
import { type Metadata } from "next";
import { JetBrains_Mono } from "next/font/google";
import "./globals.css";

const fontSans = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-sans",
});

// OPG compliant metadata (https://ogp.me/)
export const metadata: Metadata = {
  title: "Lichess.ai",
  description: "ML and AI Data Analysis on the Lichess Public Database",
  openGraph: {
    type: "website",
    locale: "en_US",
    url: BASE_URL,
    siteName: "Lichess.ai",
    title: "The most comprehensive Lichess Database analysis site",
    description:
      "Lichess.ai contains everything from machine learning analysis on the elo system, to AI models predicting the most human moves.",
    images: [
      {
        url: `${BASE_URL}/static/assets/preview.png`,
        alt: "Lichess.org's preview tile",
      },
    ],
  },
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={fontSans.variable} suppressHydrationWarning>
      <body className="flex flex-col h-screen overflow-hidden bg-background font-sans antialiased">
        <TopLoader />
        {children}
      </body>
    </html>
  );
}
