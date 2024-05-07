import "@/app/globals.css";
import { Quicksand } from "next/font/google";
import Header from "@/app/component/header.js";

const defaultFont = Quicksand({ subsets: ["latin"], weight: ['400'] });

export const metadata = {
  title: "Mission Tracker",
  description: "The latest version of the Mission Tracker for the mobile idle games AdVenture Communist and AdVenture Ages.",
};

export default function Root({ children }) {
  return (
    <html lang="en">
      <body className={`${defaultFont.className} bg-neutral-100 dark:bg-neutral-900 dark:text-neutral-100`}>
        <Header />
        <main className="m-4">{children}</main>
      </body>
    </html>
  );
}
