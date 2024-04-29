import Link from "next/link";

export default function EvergreenByRank({ params }) {
  return (
    <main className="m-4">
      <div className="text-2xl dark:text-slate-100">You are on rank {params.rank}</div>
      <Link href="../" className="mt-8 dark:text-slate-100">&uarr;&uarr;&uarr;&uarr;&uarr;</Link>
    </main>
  );
}
