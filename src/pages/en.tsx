import Link from 'next/link';
import { FaGithub, FaTwitter } from 'react-icons/fa';

export default function English() {
    return (
        <div className="bg-gray-900 text-gray-300 min-h-screen py-2 px-4 font-sans">
            <div className="container mx-auto max-w-5xl">
                <div className="bg-gray-800 p-8 rounded-lg">
                    <h1 className="text-4xl font-bold mb-2 text-white">Naoki Shikoda</h1>
                    <p className="text-l">First-year master&apos;s student in the Information Science area, Advanced Science and Technology, Nara Institute of Science and Technology</p>
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
                    <h2 className="text-2xl font-bold mb-4">Interests</h2>
                    <p className="keep-all-break-word">
                        Based in Nara.
                        I am interested in machine learning, particularly in natural language processing, image processing, and graph neural networks.
                        I also have an interest in security. I&apos;m not very knowledgeable about the lower layers yet, but I&apos;m gradually learning.
                    </p>
                    <p>I mainly use Python, dabbling in various programming languages.</p>
                    <p>I occasionally try to learn foreign languages, but it seems I need to study English first.</p>
                    <p>I&apos;m not a big drinker, but I&apos;ve recently taken a liking to whiskey.</p>
                </section>

                <section className="p-8 border-t border-gray-700 mt-4">
                    <h2 className="text-2xl font-bold mb-4">Background</h2>
                    <div className="overflow-x-auto rounded-lg shadow-lg">
                        <table className="w-full text-left table-auto bg-gray-800">
                            <tbody>
                                <tr className="border-b border-gray-100">
                                    <td className="px-4 py-2 border-gray-700 text-center">Current</td>
                                    <td className="px-4 py-2 border-gray-700">
                                        Member of the Natural Language Processing Laboratory (Watanabe Lab)
                                        <Link href="https://nlp.naist.jp/en/" target="_blank" className="mx-2 text-blue-400 hover:text-blue-200">
                                            Nara Institute of Science and Technology
                                        </Link> First year of the master&apos;s program</td>
                                </tr>

                                <tr>
                                    <td className="px-4 py-2 border-gray-700 text-center">April 2024</td>
                                    <td className="px-4 py-2 border-gray-700">Enrolled in the Graduate School of Advanced Science and Technology, Nara Institute of Science and Technology</td>
                                </tr>

                                <tr>
                                    <td className="px-4 py-2 border-gray-700 text-center">March 2024</td>
                                    <td className="px-4 py-2 border-gray-700">Graduated from Tokyo City University, Faculty of Information Engineering, Department of Intelligent Information Engineering</td>
                                </tr>
                                <tr>
                                    <td className="text-center bold text-xl"> | </td>
                                    <td className="px-4 py-2 border-gray-700">Member of the
                                        <Link href="https://www.ke.tcu.ac.jp/labo/is07/en/" target="_blank" className="mx-2 text-blue-400 hover:text-blue-200">
                                            Jinno Laboratory
                                        </Link>
                                        at the same department</td>
                                </tr>
                                <tr>
                                    <td className="px-4 py-2 border-gray-700 text-center">April 2020</td>
                                    <td className="px-4 py-2 border-gray-700">Enrolled in Tokyo City University, Faculty of Information Engineering, Department of Intelligent Information Engineering</td>
                                </tr>

                            </tbody>
                        </table>
                    </div>
                </section>

                <

                    section className="p-8 border-t border-gray-700 mt-4">
                    <h2 className="text-2xl font-bold mb-4">Internships</h2>
                    <div className="overflow-x-auto rounded-lg shadow-lg">
                        <table className="w-full text-left table-auto bg-gray-800">
                            <tbody>
                                <tr>
                                    <td className="px-4 py-2 border-gray-700">April 2023 - Present</td>
                                    <td className="px-4 py-2 border-gray-700">
                                        <Link href="https://nnn.ed.jp/recruit/special/intern/" target="_blank" className="text-blue-400 hover:text-blue-200">
                                            Kadokawa Dwango Academy NCodeLabo
                                        </Link>
                                    </td>
                                    <td className="px-4 py-2 border-gray-700">Instructor</td>
                                </tr>
                                <tr>
                                    <td className="px-4 py-2 border-gray-700">October 2022 - April 2023</td>
                                    <td className="px-4 py-2 border-gray-700">
                                        <Link href="https://nnn.ed.jp/recruit/special/intern/" target="_blank" className="text-blue-400 hover:text-blue-200">
                                            Kadokawa Dwango Academy N/S High School
                                        </Link>
                                    </td>
                                    <td className="px-4 py-2 border-gray-700">Programming TA</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </section>

                <section className="p-8 border-t border-gray-700 mt-4">
                    <h2 className="text-2xl font-bold mb-4">Other Achievements</h2>
                    <ul className="list-disc pl-8 space-y-2 bg-gray-800 rounded-lg p-4">
                        <li>
                            <Link href="https://www.security-camp.or.jp/minicamp/online2021.html" target="_blank" className="mr-4 text-blue-400 hover:text-blue-200">Security Mini Camp Online 2021</Link> Completed
                        </li>
                        <li>
                            <Link href="https://www.ipa.go.jp/jinzai/security-camp/2022/zenkoku/index.html" target="_blank" className="mr-4 text-blue-400 hover:text-blue-200">
                                Security Camp National Convention Online 2022
                            </Link> Completed AI Security Course (D Course)
                        </li>
                    </ul>
                </section>

                <section className="p-8 border-t border-gray-700 mt-4">
                    <h2 className="text-2xl font-bold mb-4">Certifications</h2>
                    <table className="w-full text-center table-auto bg-gray-800 border-h">
                        <tbody>
                            <tr className="border-b border-gray-100">
                                <td>Currently Studying</td>
                                <td className="px-4 py-2">Information Processing Security Support Technician Examination</td>
                            </tr>
                            <tr>
                                <td>2024</td>
                                <td className="px-4 py-2">Degree in Engineering</td>
                            </tr>
                            <tr>
                                <td>2022</td>
                                <td className="px-4 py-2 border-gray-400">
                                    <Link href="https://www.ipa.go.jp/shiken/kubun/ap.html" target="_blank">
                                        Applied Information Technology Engineer
                                    </Link>
                                </td>
                            </tr>
                            <tr>
                                <td>2021</td>
                                <td className="px-4 py-2 border-gray-400">
                                    <Link href="https://www.ipa.go.jp/shiken/kubun/ip.html" target="_blank">
                                        IT Passport
                                    </Link>
                                </td>
                            </tr>
                            <tr className="bg-gray-700">
                                <td>Other</td>
                                <td className="px-4 py-2 border-gray-400">Kanji Proficiency Test, World Heritage Test, etc.</td>
                            </tr>
                        </tbody>
                    </table>
                </section>

                <p className="text-center text-sm mt-8 text-gray-500">Updated April 18, 2024</p>
            </div>
        </div>
    );
}