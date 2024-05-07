"use client";
import Link from "next/link";
import { usePathname } from 'next/navigation';
import { PRODUCT_INFO_ADCOM, PRODUCT_INFO_AGES } from "@/app/constants";
import { FaHome, FaQuestionCircle, FaUser } from "react-icons/fa";

export default function Header() {
  const pathname = usePathname();
  const pathnameSplit = pathname.split('/');
  const productNameTitle = (() => {
    if (pathnameSplit.length > 0) {
      switch (pathnameSplit[1]) {
        case "adcom":
          return PRODUCT_INFO_ADCOM.ABBR_NAME;
        case "ages":
          return PRODUCT_INFO_AGES.ABBR_NAME;
      }
    }
    return "";
  })();
  
  return (
    <div className="sticky inset-x-0 top-0 flex bg-neutral-200 dark:bg-neutral-950 p-2 border-solid border-b border-b-neutral-400">
      <div className="flex-1">{productNameTitle}</div>
      <div className="flex justify-center space-x-4">
        <Link href="/">
          <FaHome className="header-icon" size={24} />
        </Link>
        <Link href="/help">
          <FaQuestionCircle className="header-icon" size={24} />
        </Link>
        <Link href="/user">
          <FaUser className="header-icon" size={24} />
        </Link>
      </div>
    </div>
  )
}