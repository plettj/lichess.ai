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
  description:
    "A machine learning analysis of the lichess.org public database. Built by Josiah Plett, Trevor Du, and Tonglei Liu.",
  openGraph: {
    type: "website",
    locale: "en_US",
    url: BASE_URL,
    siteName: "lichess.ai",
    title: "A machine learning analysis of the lichess.org public database.",
    description:
      "Josiah Plett, Trevor Du, and Tonglei Liu present unique insights into modern blitz chess statistics.",
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
