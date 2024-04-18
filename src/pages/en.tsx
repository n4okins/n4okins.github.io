import Link from 'next/link';

export default function English() {
    return (
        <div className="bg-gray-900 text-gray-300 min-h-screen py-2 px-4 font-sans">
            <div className="container mx-auto max-w-5xl">
                <div className="bg-gray-900 text-gray-300 min-h-screen py-4 px-4 font-sans">
                    <div className="container mx-auto max-w-5xl">
                        <div className="bg-gray-800 p-8 rounded-lg">
                            <h1 className="text-4xl font-bold mb-2 text-white">Naoki Shikoda</h1>
                            <p className="text-l">First-year Master&apos;s student in Nara Institute of Science and Technology</p>
                        </div>

                        <section className="p-8 border-t border-gray-700 mt-4">
                            <h2 className="text-2xl font-bold mb-4">Interests</h2>
                            <p>
                                I live in Nara.
                                I have a strong interest in machine learning, especially in natural language processing, image processing, and graph neural networks.
                                I am also interested in security. While I&apos;m not very knowledgeable about low-level details yet, I am gradually learning more.
                            </p>
                            <p>I primarily use Python, but I enjoy dabbling in various programming languages.</p>
                            <p>I&apos;m not a heavy drinker, but lately, I&apos;ve developed a liking for whiskey.</p>
                        </section>

                        <section className="p-8 border-t border-gray-700 mt-4">
                            <h2 className="text-2xl font-bold mb-4">Education</h2>
                            <div className="overflow-x-auto rounded-lg shadow-lg">
                                <table className="w-full text-left table-auto bg-gray-800">
                                    <tbody>
                                        <tr>
                                            <td className="px-4 py-2 border-gray-700 text-center">Current</td>
                                            <td className="px-4 py-2 border-gray-700">
                                                Information Science
                                                <Link href="https://nlp.naist.jp/en/" target="_blank" className="mx-2 text-blue-400 hover:text-blue-200">
                                                    Natural Language Processing Laboratory (Watanabe Lab)
                                                </Link>Member</td>
                                        </tr>

                                        <tr>
                                            <td className="px-4 py-2 border-gray-700 text-center">April 2024</td>
                                            <td className="px-4 py-2 border-gray-700">Entered the Graduate School of Advanced Science and Technology, Nara Institute of Science and Technology</td>
                                        </tr>

                                        <tr>
                                            <td className="px-4 py-2 border-gray-700 text-center">March 2024</td>
                                            <td className="px-4 py-2 border-gray-700">Graduated from Tokyo City University, Faculty of Information Engineering, Department of Intelligent Information Engineering</td>
                                        </tr>
                                        <tr>
                                            <td className="text-center bold text-xl"> | </td>
                                            <td className="px-4 py-2 border-gray-700">Member of
                                                <Link href="https://www.ke.tcu.ac.jp/labo/is07/" target="_blank" className="mx-2 text-blue-400 hover:text-blue-200">
                                                    Jinno Laboratory
                                                </Link>
                                                at the same department</td>
                                        </tr>
                                        <tr>
                                            <td className="px-4 py-2 border-gray-700 text-center">April 2020</td>
                                            <td className="px-4 py-2 border-gray-700">Entered Tokyo City University, Faculty of Information Engineering, Department of Intelligent Information Engineering</td>
                                        </tr>

                                    </tbody>
                                </table>
                            </div>
                        </section>

                        <section className="p-8 border-t border-gray-700 mt-4">
                            <h2 className="text-2xl font-bold mb-4">Internships</h2>
                            <div className="overflow-x-auto rounded-lg shadow-lg">
                                <table className="w-full text-left table-auto bg-gray-800">
                                    <tbody>
                                        <tr>
                                            <td className="px-4 py-2 border-gray-700">April 2023 - Present</td>
                                            <td className="px-4 py-2 border-gray-700">
                                                <Link href="https://nnn.ed.jp/recruit/special/intern/" target="_blank" className="text-blue-400 hover:text-blue-200">
                                                    Kadokawa Dwango Educational Institute NCodeLabo
                                                </Link>
                                            </td>
                                            <td className="px-4 py-2 border-gray-700">Programming Instructor Intern</td>
                                        </tr>
                                        <tr>
                                            <td className="px-4 py-2 border-gray-700">October 2022 - April 2023</td>
                                            <td className="px-4 py-2 border-gray-700">
                                                <Link href="https://nnn.ed.jp/recruit/special/intern/" target="_blank" className="text-blue-400 hover:text-blue-200">
                                                    Kadokawa Dwango Educational Institute N/S High School
                                                </Link>
                                            </td>
                                            <td className="px-4 py-2 border-gray-700">Programming TA Intern</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </section>

                        <section className="p-8 border-t border-gray-700 mt-4">
                            <h2 className="text-2xl font-bold mb-4">Other Qualifications</h2>
                            <ul className="list-disc pl-8 space-y-2 bg-gray-800 rounded-lg p-4">
                                <li>
                                    <Link href="https://www.security-camp.or.jp/minicamp/online2021.html" target="_blank" className="text-blue-400 hover:text-blue-200">Security Mini Camp Online 2021</Link> Completed
                                </li>
                                <li>
                                    <Link href="https://www.ipa.go.jp/jinzai/security-camp/2022/zenkoku/index.html" target="_blank" className="text-blue-400 hover:text-blue-200">
                                        Security Camp Online 2022
                                    </Link> Completed AI Security Course (D Course)
                                </li>
                            </ul>
                        </section>

                        <section className="p-8 border-t border-gray-700 mt-4">
                            <h2 className="text-2xl font-bold mb-4">Certificates</h2>
                            <ul className="list-disc pl-8 space-y-2 bg-gray-800 rounded-lg p-4">
                                <li>IT Passport</li>
                                <li>Applied Information Technology Engineer Examination</li>
                            </ul>
                        </section>

                        <p className="text-center text-sm mt-8 text-gray-500">Updated April 2024</p>
                    </div>
                </div>
            </div>
        </div>
    );
}