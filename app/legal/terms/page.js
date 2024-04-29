import Link from "next/link";

export default function TermsOfService({ params }) {
  return (
    <main className="dark:text-white">
      <div className="text-2xl">You've reached an inaccessible area</div>
      <Link href='/'>Back to root</Link>
    </main>
  );
}
