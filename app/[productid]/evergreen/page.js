"use client";
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

const PIPE_TO_RANK = 1; // or previously active rank as specified in user save

export default function EvergreenRootRedirect({ params }) {
  const router = useRouter();

  useEffect(() => {
    if (PIPE_TO_RANK) {
      router.replace(`/${params.productid}/evergreen/${PIPE_TO_RANK}`);
    }
  }, [PIPE_TO_RANK]);

  return (
    <div>Redirecting to previously active rank ...</div>
  );
}
