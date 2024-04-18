import Link from 'next/link';
import { FaGithub, FaTwitter } from 'react-icons/fa';

export default function Japanese() {
    return (
        <div className="bg-gray-900 text-gray-300 min-h-screen py-2 px-4 font-sans">
            <div className="container mx-auto max-w-5xl">
                <div className="bg-gray-900 text-gray-300 min-h-screen py-4 px-4 font-sans">
                    <div className="container mx-auto max-w-5xl">
                        <div className="bg-gray-800 p-8 rounded-lg">
                            <h1 className="text-4xl font-bold mb-2 text-white">志子田直輝（しこだなおき）</h1>
                            <p className="text-l">奈良先端科学技術大学院大学 先端科学技術研究科 先端科学技術専攻 情報科学領域 博士前期課程 1年</p>
                            <div className="flex space-x-4 mt-4 align-center">
                                <a href="https://github.com/n4okins" target="_blank" className="text-white hover:text-gray-300">
                                    <FaGithub size={30} />
                                </a>
                                <a href="https://twitter.com/n4okins" target="_blank" className="text-white hover:text-gray-300">
                                    <FaTwitter size={30} />
                                </a>
                            </div>
                        </div>


                        <section className="p-8 border-t border-gray-700 mt-4">
                            <h2 className="text-2xl font-bold mb-4">興味関心</h2>
                            <p className="keep-all-break-word">
                                奈良にいます。
                                機械学習に興味があります。特に自然言語処理、画像処理、グラフニューラルネットワークに関心があります。
                                セキュリティにも興味があります。低レイヤーはあまり詳しくないですが、少しずつ学んでいます。
                            </p>
                            <p>Pythonをメインに、いろんなプログラミング言語をかじりながら過ごしています。</p>
                            <p>たまに外国語に手を出しますが、まずは英語の勉強をしなければならなさそうです。</p>
                            <p>お酒は量は飲めませんが、最近はウイスキーが好きです。</p>
                        </section>

                        <section className="p-8 border-t border-gray-700 mt-4">
                            <h2 className="text-2xl font-bold mb-4">略歴</h2>
                            <div className="overflow-x-auto rounded-lg shadow-lg">
                                <table className="w-full text-left table-auto bg-gray-800">
                                    <tbody>
                                        <tr className="border-b border-gray-100">
                                            <td className="px-4 py-2 border-gray-700 text-center">現在</td>
                                            <td className="px-4 py-2 border-gray-700">
                                                情報科学領域
                                                <Link href="https://nlp.naist.jp/ja/" target="_blank" className="mx-2 text-blue-400 hover:text-blue-200">
                                                    自然言語処理学研究室（渡辺研究室）
                                                </Link>所属 博士前期課程 1年</td>
                                        </tr>

                                        <tr>
                                            <td className="px-4 py-2 border-gray-700 text-center">2024.04</td>
                                            <td className="px-4 py-2 border-gray-700">奈良先端科学技術大学院大学 先端科学技術研究科 先端科学技術専攻 入学</td>
                                        </tr>

                                        <tr>
                                            <td className="px-4 py-2 border-gray-700 text-center">2024.03</td>
                                            <td className="px-4 py-2 border-gray-700">東京都市大学 情報工学部 知能情報工学科 卒業</td>
                                        </tr>
                                        <tr>
                                            <td className="text-center bold text-xl"> | </td>
                                            <td className="px-4 py-2 border-gray-700">同学科
                                                <Link href="https://www.ke.tcu.ac.jp/labo/is07/" target="_blank" className="mx-2 text-blue-400 hover:text-blue-200">
                                                    神野研究室
                                                </Link>
                                                所属</td>
                                        </tr>
                                        <tr>
                                            <td className="px-4 py-2 border-gray-700 text-center">2020.04</td>
                                            <td className="px-4 py-2 border-gray-700">東京都市大学 情報工学部 知能情報工学科 入学</td>
                                        </tr>

                                    </tbody>
                                </table>
                            </div>
                        </section>

                        <section className="p-8 border-t border-gray-700 mt-4">
                            <h2 className="text-2xl font-bold mb-4">インターン</h2>
                            <div className="overflow-x-auto rounded-lg shadow-lg">
                                <table className="w-full text-left table-auto bg-gray-800">
                                    <tbody>
                                        <tr>
                                            <td className="px-4 py-2 border-gray-700">2023.04 - 現在</td>
                                            <td className="px-4 py-2 border-gray-700">
                                                <Link href="https://nnn.ed.jp/recruit/special/intern/" target="_blank" className="text-blue-400 hover:text-blue-200">
                                                    角川ドワンゴ学園 NCodeLabo
                                                </Link>
                                            </td>
                                            <td className="px-4 py-2 border-gray-700">講師</td>
                                        </tr>
                                        <tr>
                                            <td className="px-4 py-2 border-gray-700">2022.10 - 2023.04</td>
                                            <td className="px-4 py-2 border-gray-700">
                                                <Link href="https://nnn.ed.jp/recruit/special/intern/" target="_blank" className="text-blue-400 hover:text-blue-200">
                                                    角川ドワンゴ学園 N/S高校
                                                </Link>
                                            </td>
                                            <td className="px-4 py-2 border-gray-700">プログラミングTA</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </section>

                        <section className="p-8 border-t border-gray-700 mt-4">
                            <h2 className="text-2xl font-bold mb-4">その他</h2>
                            <ul className="list-disc pl-8 space-y-2 bg-gray-800 rounded-lg p-4">
                                <li>
                                    <Link href="https://www.security-camp.or.jp/minicamp/online2021.html" target="_blank" className="mr-4 text-blue-400 hover:text-blue-200">セキュリティ・ミニキャンプ オンライン 2021</Link>修了
                                </li>
                                <li>
                                    <Link href="https://www.ipa.go.jp/jinzai/security-camp/2022/zenkoku/index.html" target="_blank" className="mr-4 text-blue-400 hover:text-blue-200">
                                        セキュリティ・キャンプ全国大会 オンライン 2022
                                    </Link> AIセキュリティコース（Dコース）修了
                                </li>
                            </ul>
                        </section>

                        <section className="p-8 border-t border-gray-700 mt-4">
                            <h2 className="text-2xl font-bold mb-4">保有資格</h2>
                            <table className="w-full text-center table-auto bg-gray-800 border-h">
                                <tbody>
                                    <tr className="border-b border-gray-100">
                                        <td>現在勉強中</td>
                                        <td className="px-4 py-2">情報処理安全確保支援士試験</td>
                                    </tr>
                                    <tr>
                                        <td>2024</td>
                                        <td className="px-4 py-2">学位（工学）</td>
                                    </tr>
                                    <tr>
                                        <td>2022</td>
                                        <td className="px-4 py-2 border-gray-400">
                                            <Link href="https://www.ipa.go.jp/shiken/kubun/ap.html" target="_blank">
                                                応用情報技術者
                                            </Link>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>2021</td>
                                        <td className="px-4 py-2 border-gray-400">
                                            <Link href="https://www.ipa.go.jp/shiken/kubun/ip.html" target="_blank">
                                                ITパスポート
                                            </Link>
                                        </td>
                                    </tr>
                                    <tr className="bg-gray-700">
                                        <td>その他</td>
                                        <td className="px-4 py-2 border-gray-400">漢字検定とか世界遺産検定とか</td>
                                    </tr>
                                </tbody>
                            </table>
                        </section>

                        <p className="text-center text-sm mt-8 text-gray-500">2024.04.18 更新</p>
                    </div>
                </div>
            </div>
        </div>
    );
}