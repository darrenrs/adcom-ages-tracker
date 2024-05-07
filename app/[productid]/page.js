"use client";
import Link from "next/link";
import { notFound } from 'next/navigation';
import checkValidProductId from '@/app/[productid]/checkValidProductId';
import { OTHER_RESOURCES } from "@/app/constants";

export default function ProductContents({ params }) {
  if (!checkValidProductId(params.productid)) {
    notFound();
  }

  return (
    <div className="flex flex-col items-center justify-center">
      <h1 className="global-title">Select a Mode</h1>
      <div className="flex flex-col lg:flex-row items-center w-full m-2">
        <Link href={`/${params.productid}/evergreen`} className="root-select">Evergreen</Link>
        <Link href={`/${params.productid}/lte`} className="root-select">Events</Link>
      </div>
      <h1 className="global-title">Other Resources</h1>
      <div className="grid grid-cols-3 gap-4 justify-between">
        {OTHER_RESOURCES[params.productid].map(resource => (
          <a key={resource.title} href={resource.path} className="product-select">
            {resource.title}
          </a>
        ))}
      </div>
    </div>
  );
}
