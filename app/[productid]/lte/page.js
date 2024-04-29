import Link from "next/link";

export default function LteByType({ params }) {
  return (
    <main className="m-4">
      <div className="text-2xl dark:text-slate-100">You now must select an event</div>
      <div className="flex dark:text-slate-100 p-12">
        <Link href={`/${params.productid}/lte/balance`} className="flex-initial w-2/4">Direct Access</Link>
        <Link href={`/${params.productid}/lte/schedule`} className="flex-initial w-2/4">Schedule</Link>
      </div>
      <Link href="." className="mt-8 dark:text-slate-100">&uarr;&uarr;&uarr;&uarr;&uarr;</Link>
    </main>
  );
}
