import Link from "next/link";

const currentYear = (new Date()).getFullYear();

export default function Footer() {
  return (
    <div className="absolute inset-x-0 bottom-0 flex bg-black text-slate-100 p-2 border-solid border-t-2 dark:border-t-zinc-400">
      <div className="flex-1">&copy; {currentYear} Enigma Labs. All rights reserved.</div>
      <div className="flex-none space-x-4">
        <Link href="/legal/terms">Terms</Link>
        <Link href="/legal/privacy">Privacy</Link>
      </div>
    </div>
  );
}
