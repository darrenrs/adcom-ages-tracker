import Image from "next/image";
import Link from "next/link";
import { PRODUCT_INFO_ADCOM, PRODUCT_INFO_AGES } from "@/app/constants";

export default function Root() {
  return (
    <main className="m-4">
      <div className="text-2xl dark:text-slate-100">Welcome to the Mission Tracker!</div>
      <div className="italic dark:text-slate-400">Select your game</div>
      <div className="flex dark:text-slate-100 p-12">
        <Link href={`/${PRODUCT_INFO_ADCOM.COMMON_NAME}`} className="flex-initial w-2/4 bg-zinc-800 rounded-2xl text-2xl">
          <Image src={`/assets/${PRODUCT_INFO_ADCOM.TITLE_ID}/icon.png`} width={32} height={48} alt='Icon'></Image>
          {PRODUCT_INFO_ADCOM.PRODUCT_NAME}
        </Link>
        <Link href={`/${PRODUCT_INFO_AGES.COMMON_NAME}`} className="flex-initial w-2/4 bg-zinc-800 rounded-2xl text-2xl">
          <Image src={`/assets/${PRODUCT_INFO_AGES.TITLE_ID}/icon.png`} width={32} height={48} alt='Icon'></Image>
          {PRODUCT_INFO_AGES.PRODUCT_NAME}
        </Link>
      </div>
    </main>
  );
}
