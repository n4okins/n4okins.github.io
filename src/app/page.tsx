import Link from "next/link";

export default function Home() {
  return (
    <div className="bg-gray-100 text-gray-800 min-h-screen py-12 px-4 font-sans">
      <div className="container mx-auto max-w-4xl">
        <h1 className="text-4xl font-bold mb-8">自己紹介</h1>

        <section className="mb-12">
          <h2 className="text-2xl font-bold mb-4">興味関心</h2>
          <p>
            機械学習に興味があります。特に自然言語処理、画像処理、グラフニューラルネットワークに関心があります。
          </p>
          <p>
            セキュリティにも興味があります。低レイヤーにはあまり詳しくありませんが、将来的に学びたいと考えています。
          </p>
        </section>

        <section className="mb-12">
          <h2 className="text-2xl font-bold mb-4">略歴</h2>
          <ul className="list-disc pl-8">
            <li>
              <p><strong>2020.04:</strong> 東京都市大学 情報工学部 知能情報工学科 入学</p>
              <ul className="list-disc pl-8">
                <li>2022-2024: 同学科 神野研究室 所属</li>
              </ul>
            </li>
            <li>
              <p><strong>2024.03:</strong> 東京都市大学 情報工学部 知能情報工学科 卒業</p>
            </li>
            <li>
              <p><strong>2024.04:</strong> 奈良先端科学技術大学院大学 先端科学技術専攻 先端科学技術研究科 入学</p>
              <ul className="list-disc pl-8">
                <li>2024 - 現在: 情報科学領域 自然言語処理学研究室 （渡辺研究室） 所属</li>
              </ul>
            </li>
          </ul>
        </section>

        <section className="mb-12">
          <h2 className="text-2xl font-bold mb-4">インターン</h2>
          <ul className="list-disc pl-8">
            <li><strong>2022.10 - 2023.04:</strong> 学校法人角川ドワンゴ学園 N/S高等学校 プログラミングTA</li>
            <li><strong>2023.08 - 現在:</strong> 学校法人角川ドワンゴ学園 N Code Labo プログラミング講師</li>
          </ul>
        </section>

        <section className="mb-12">
          <h2 className="text-2xl font-bold mb-4">その他</h2>
          <ul className="list-disc pl-8">
            <li><strong>2022.10:</strong> セキュリティ・ミニキャンプ2022 修了</li>
            <li><strong>2023.08:</strong> セキュリティ・キャンプ全国大会2023（AIセキュリティコース） 修了</li>
          </ul>
        </section>

        <section>
          <h2 className="text-2xl font-bold mb-4">資格</h2>
          <ul className="list-disc pl-8">
            <li>ITパスポート</li>
            <li>応用情報技術者</li>
          </ul>
        </section>
        
        <p className="text-sm mt-8">2024.04 更新</p>
      </div>
    </div>
  );
}
