import { FaGithub, FaTwitter } from 'react-icons/fa';
import Content from '@/pages/content';

export default function ContentPage({ lang }: { lang: string }) {
    const content: any = Content(lang);
    return (
        <div className="bg-gray-200 dark:bg-gray-800 dark:text-gray-300 min-h-screen py-2 px-4 font-sans">
            <div className="container mx-auto max-w-7xl">
                <div className="dark:bg-gray-900 dark:text-gray-300 min-h-screen py-4 px-4 font-sans">
                    <div className="container mx-auto max-w-6xl">
                        <div className="dark:bg-gray-700 p-8 rounded-lg">
                            <h1 className="text-4xl font-bold mb-2 dark:text-white">{content?.name}</h1>
                            <p className="text-l">
                                {content?.affiliation}
                            </p>
                            <div className="flex space-x-4 mt-4 align-center">
                                <a href="https://github.com/n4okins" target="_blank" className="dark:text-white hover:text-gray-300">
                                    <FaGithub size={30} />
                                </a>
                                <a href="https://twitter.com/n4okins" target="_blank" className="dark:text-white hover:text-gray-300">
                                    <FaTwitter size={30} />
                                </a>
                            </div>
                        </div>


                        <section className="p-8 border-t border-gray-700 mt-4">
                            <h2 className="text-2xl font-bold mb-4">
                                {content?.interested_in?.title}
                            </h2>
                            <div className="keep-all-break-word">
                                {content?.interested_in?.content}
                            </div>
                        </section>

                        <section className="p-8 border-t border-gray-700 mt-4">
                            <h2 className="text-2xl font-bold mb-4">{content?.background?.title}</h2>
                            <div className="overflow-x-auto rounded-lg shadow-lg">
                                <table className="w-full text-left table-auto dark:bg-gray-800 bg-gray-100">
                                    <tbody>
                                        <tr className="border-b dark:border-gray-100 border-gray-300">
                                            <td className="px-4 py-2 text-center">
                                                {content?.background?.content[0].td}
                                            </td>
                                            <td className="px-4 py-2">
                                                {content?.background?.content[0].content}
                                            </td>
                                        </tr>
                                        <tr>
                                            <td className="px-4 py-2 text-center">
                                                {content?.background?.content[1].td}
                                            </td>
                                            <td className="px-4 py-2">
                                                {content?.background?.content[1].content}
                                            </td>
                                        </tr>

                                        <tr>
                                            <td className="px-4 py-2 text-center">
                                                {content?.background?.content[2].td}
                                            </td>
                                            <td className="px-4 py-2">
                                                {content?.background?.content[2].content}
                                            </td>
                                        </tr>
                                        <tr>
                                            <td className="text-center bold text-xl">
                                                {content?.background?.content[3].td}
                                            </td>
                                            <td className="px-4 py-2">
                                                {content?.background?.content[3].content}
                                            </td>
                                        </tr>
                                        <tr>
                                            <td className="px-4 py-2 border-gray-700 text-center">
                                                {content?.background?.content[4].td}
                                            </td>
                                            <td className="px-4 py-2 border-gray-700">
                                                {content?.background?.content[4].content}
                                            </td>
                                        </tr>

                                    </tbody>
                                </table>
                            </div>
                        </section>

                        <section className="p-8 border-t border-gray-700 mt-4">
                            <h2 className="text-2xl font-bold mb-4">{content?.internship?.title}</h2>
                            <div className="overflow-x-auto rounded-lg shadow-lg">
                                <table className="w-full text-left table-auto dark:bg-gray-800 bg-gray-100">
                                    <tbody>
                                        {content?.internship?.content?.map((item: any, index: number) => (
                                            <tr key={index}>
                                                <td className="px-4 py-2 border-gray-700">{item.td}</td>
                                                <td className="px-4 py-2 border-gray-700">
                                                    {item.content[0]}
                                                </td>
                                                <td className="-px-4 py-2 border-gray-700">
                                                    {item.content[1]}
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </section>

                        <section className="p-8 border-t border-gray-700 mt-4">
                            <h2 className="text-2xl font-bold mb-4">{content?.other?.title}</h2>
                            <ul className="list-disc pl-8 space-y-2 dark:bg-gray-800 bg-gray-100 rounded-lg p-4">
                                {content?.other?.content?.map((item: any, index: number) => (
                                    <li key={index}>{item}</li>
                                ))}
                            </ul>
                        </section>

                        <section className="p-8 border-t border-gray-700 mt-4">
                            <h2 className="text-2xl font-bold mb-4">{content?.publication?.title}</h2>
                            <table className="w-full text-left table-auto dark:bg-gray-800 bg-gray-100">
                                <tbody>
                                    {content?.publication?.content?.map((item: any, index: number) => (
                                        <tr key={index}>
                                            <td className="px-4 py-2 border-gray-700">{item.td}</td>
                                            <td className="px-4 py-2 border-gray-700">
                                                {item.content[0]}
                                            </td>
                                            <td className="px-4 py-2 border-gray-700">
                                                {item.content[1]}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </section>

                        <section className="p-8 border-t border-gray-700 mt-4">
                            <h2 className="text-2xl font-bold mb-4">{content?.certification?.title}</h2>
                            <table className="w-full text-center table-auto dark:bg-gray-800 bg-gray-100 border-h">
                                <tbody>
                                    {content?.certification?.content?.map((item: any, index: number) => (
                                        <tr key={index} className={item.className}>
                                            <td className="px-4 py-2 border-gray-400">{item.td}</td>
                                            <td className="px-4 py-2 border-gray-400">
                                                {item.content}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </section>

                        <p className="text-center text-sm mt-8 text-gray-500">{content?.updated}</p>
                    </div>
                </div>
            </div>
        </div>
    );
}