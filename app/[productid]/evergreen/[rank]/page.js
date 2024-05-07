import Link from "next/link";

export default function EvergreenByRank({ params }) {
  return (
    <div>You are on rank {params.rank}</div>
  );
}
