import Link from "next/link";

export default function TitleId({ params }) {
  return (
    <main className="m-4">
      <div className="text-2xl dark:text-slate-100">Which are you playing?</div>
      <div className="flex dark:text-slate-100 p-12">
        <Link href={`/${params.productid}/evergreen`} className="flex-initial w-2/4">Evergreen</Link>
        <Link href={`/${params.productid}/lte`} className="flex-initial w-2/4">Event</Link>
      </div>
      <Link href="../" className="mt-8 dark:text-slate-100">&uarr;&uarr;&uarr;&uarr;&uarr;</Link>
    </main>
  );
}
