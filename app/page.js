import Image from "next/image";
import Link from "next/link";
import { PRODUCT_INFO_ADCOM, PRODUCT_INFO_AGES } from "@/app/constants";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center">
      <h1 className="global-title text-center">Welcome to the Mission Tracker!</h1>
      <span className="global-subtitle">Select a game to continue</span>
      <div className="flex flex-col lg:flex-row items-center w-full m-4">
        <Link href={`/${PRODUCT_INFO_ADCOM.COMMON_NAME}`} className="root-select">
          <Image src={`/assets/${PRODUCT_INFO_ADCOM.TITLE_ID}/icon.png`} width={64} height={80} className="w-16 h-20" alt={PRODUCT_INFO_ADCOM.COMMON_NAME} />
          <span className="font-bold">{PRODUCT_INFO_ADCOM.PRODUCT_NAME}</span>
        </Link>
        <Link href={`/${PRODUCT_INFO_AGES.COMMON_NAME}`} className="root-select">
          <Image src={`/assets/${PRODUCT_INFO_AGES.TITLE_ID}/icon.png`} width={64} height={80} className="w-16 h-20" alt={PRODUCT_INFO_AGES.COMMON_NAME} />
          <span className="font-bold">{PRODUCT_INFO_AGES.PRODUCT_NAME}</span>
        </Link>
      </div>
    </div>
  );
}
