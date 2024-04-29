import "./globals.css";
import { Rubik } from "next/font/google";
import Footer from "@/app/component/footer.js";

const defaultFont = Rubik({ subsets: ["latin"], weight: ['400'] });

export const metadata = {
  title: "Mission Tracker",
  description: "The latest and greatest version of the Mission Tracker for AdVenture Communist and AdVenture Ages.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={`${defaultFont.className} dark:bg-zinc-900`}>
        {children}
        <Footer></Footer>
      </body>
    </html>
  );
}
