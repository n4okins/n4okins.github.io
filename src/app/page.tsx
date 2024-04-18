import Link from "next/link";

export default function Home() {
  return (
    <div className="bg-gray-900 text-white min-h-screen py-12 px-4">
      <div className="container mx-auto max-w-4xl">
        <h1 className="text-4xl font-bold mb-4">こんにちは！</h1>
        <p className="text-3xl font-bold mb-6">
          あなたの名前です。
        </p>
        <p className="text-lg mb-8 text-wrap">
          奈良先端科学技術大学院大学（NAIST）の
          <Link
            href="https://nlp.naist.jp/"
            rel="noopener noreferrer"
            target="_blank"
            className="text-blue-400 hover:underline"
          >
            自然言語処理学研究室
          </Link>に所属している修士1年です。
        </p>
      </div>
    </div>
  );
}