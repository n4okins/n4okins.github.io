import Link from "next/link";

export default function Home() {
  return (
    <div className="bg-gray-100 text-gray-800 min-h-screen py-12 px-4 font-serif">
      <div className="container mx-auto max-w-4xl">
        <h1 className="text-4xl font-bold mb-8">こんにちは！</h1>
        <section className="mb-12 border-b-2 border-gray-300 pb-6">
          <h2 className="text-2xl font-bold mb-4">興味関心</h2>
          <p className="mb-2">
            機械学習 (特に自然言語処理, 画像処理, グラフニューラルネットワーク)
          </p>
          <p>
            セキュリティ（低レイヤーにはあまり詳しくないけど興味はあります）
          </p>
        </section>
        <section className="mb-12 border-b-2 border-gray-300 pb-6">
          <h2 className="text-2xl font-bold mb-4">略歴</h2>
          <ul>
            <li className="mb-4">
              <div className="font-bold mb-1">2020.04</div>
              <div>東京都市大学 情報工学部 知能情報工学科 入学</div>
              <ul className="list-disc pl-8 mb-1">
                <li>2022-2024 同学科 神野研究室 所属</li>
              </ul>
            </li>
            <li className="mb-4">
              <div className="font-bold mb-1">2024.03</div>
              <div>東京都市大学 情報工学部 知能情報工学科 卒業</div>
            </li>
            <li className="mb-4">
              <div className="font-bold mb-1">2024.04</div>
              <div>奈良先端科学技術大学院大学 先端科学技術専攻 先端科学技術研究科 入学</div>
              <ul className="list-disc pl-8 mb-1">
                <li>2024 - 現在 情報科学領域 自然言語処理学研究室 （渡辺研究室） 所属</li>
              </ul>
            </li>
          </ul>
        </section>
        <section className="mb-12 border-b-2 border-gray-300 pb-6">
          <h2 className="text-2xl font-bold mb-4">インターン</h2>
          <ul>
            <li className="mb-4">
              <div className="font-bold mb-1">2022.10 - 2023.04</div>
              <div>学校法人角川ドワンゴ学園 N/S高等学校 プログラミングTA</div>
            </li>
            <li className="mb-4">
              <div className="font-bold mb-1">2023.08 - 現在</div>
              <div>学校法人角川ドワンゴ学園 N Code Labo プログラミング講師</div>
            </li>
          </ul>
        </section>
        <section className="mb-12 border-b-2 border-gray-300 pb-6">
          <h2 className="text-2xl font-bold mb-4">他</h2>
          <ul>
            <li className="mb-4">
              <div className="font-bold mb-1">2022.10</div>
              <div>セキュリティ・ミニキャンプ2022 修了</div>
            </li>
            <li className="mb-4">
              <div className="font-bold mb-1">2023.08</div>
              <div>セキュリティ・キャンプ全国大会2023（AIセキュリティコース） 修了</div>
            </li>
          </ul>
        </section>
        <section>
          <h2 className="text-2xl font-bold mb-4">資格</h2>
          <ul>
            <li>ITパスポート</li>
            <li>応用情報技術者</li>
          </ul>
        </section>
      </div>
    </div>
  );
}
